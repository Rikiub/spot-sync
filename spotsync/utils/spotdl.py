from pathlib import Path
from typing import Union
import sys

from requests import ConnectionError

from spotipy import Spotify, SpotifyException, CacheFileHandler
from spotipy.oauth2 import SpotifyClientCredentials

from spotdl import Downloader
from spotdl.utils.logging import init_logging
from spotdl.utils.config import create_settings, get_config, get_cache_path, DEFAULT_CONFIG
from spotdl.utils.arguments import parse_arguments
from spotdl.utils.spotify import SpotifyClient, save_spotify_cache
from spotdl.console.entry_point import generate_initial_config, OPERATIONS

from utils.theme import print

VALID_URLS = ("https://open.spotify.com/playlist/")

def check_spotify_url(url: str) -> str:
	"""Check URL with Spotipy."""
	sp = getSpotifyClient()

	if sp.playlist(url):
		return url
	else:
		raise ValueError

def getSpotifyClient() -> Spotify:
	"""A Spotipy instance using the SpotDL cache path."""

	config = user_config()

	auth_manager = SpotifyClientCredentials(
		client_id=config["client_id"],
		client_secret=config["client_secret"],
		cache_handler=CacheFileHandler(cache_path=get_cache_path())
	)
	return Spotify(auth_manager=auth_manager)

def user_config() -> dict:
	"""
	Return SpotDL user config file.
	In Linux and Darwin the path is '~/.spotdl/config.json'
	"""

	generate_initial_config()
	return get_config()

instance = None
default_settings = {}

def spotDLSyncer(
	query: Union[Path, str],
	output_path: Path,
	save_file: str = None
) -> None:
	"""
	A little "hack" to uses SpotDL on Python scripts without errors.
	Adapted to just uses "sync" command.

	## Arguments
	query:
	  can be a "str(URL)" to Spotify playlist. That run the creation of an new Playlist folder.
	  can be a "pathlib.Path" to .spotdl file. That run the sync of an current Playlist folder.
	output_path:
	  where the files will be stored.
	save_file:
	  name of the '.spotdl' file.
	"""

	# persistent instance options
	global instance, default_settings
	downloader = None

	try:
		sys.argv = [
			sys.argv[0],
			"sync", str(query),
			"--output", str(output_path)
		]

		# if "query" is a string, run playlist creation mode
		if type(query) == str:
			if save_file:
				sys.argv.append(
					"--save-file", str(f"{output_path}/{save_file}")
				)
			else:
				raise ValueError("For playlist creation mode you need provide a 'save_file' name.")
		# else, run the sync mode

		# parse "sys.argv" to argparse
		arguments = parse_arguments()

		# init SpotDL
		spotify_settings, downloader_settings, web_settings = create_settings(arguments)

		# if instance not exist, init a "singleton" instance
		if not instance:
			# set spotsync defaults
			default_settings = DEFAULT_CONFIG
			default_settings["audio_providers"] = ["soundcloud", "bandcamp", "youtube-music"]
			default_settings["lyrics_providers"] = ["synced", "musixmatch", "genius", "azlyrics"]
			default_settings["preload"] = True
			default_settings["bitrate"] = "auto"

			# read user config from '~/.spotdl/config.json' (Linux and Darwin)
			custom_settings = user_config()
			default_settings["format"] = custom_settings["format"]
			default_settings["detect_formats"] = custom_settings["detect_formats"]

			# init SpotDL Singleton
			SpotifyClient.init(**spotify_settings)
			init_logging("INFO")
			instance = True

		# parse custom settings
		downloader = Downloader(default_settings)

		# Init Functions
		OPERATIONS[arguments.operation] (
			arguments.query,
			downloader
		)

	except (ConnectionError, SpotifyException):
		print("[warning]Failed to connect to internet.")
		raise
	finally:
		if downloader:
			downloader.progress_handler.close()