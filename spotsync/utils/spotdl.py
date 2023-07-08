from typing import List
import sys

from spotipy import Spotify, SpotifyException, CacheFileHandler
from spotipy.oauth2 import SpotifyClientCredentials

from spotdl import Downloader
from spotdl.utils.logging import init_logging
from spotdl.utils.config import create_settings, get_config, get_cache_path
from spotdl.utils.arguments import parse_arguments
from spotdl.utils.spotify import SpotifyClient, save_spotify_cache
from spotdl.console.entry_point import generate_initial_config, OPERATIONS

VALID_URLS = ("https://open.spotify.com/playlist/")

def check_spotify_url(url: str) -> str:
	sp = getSpotifyClient()

	if sp.playlist(url):
		return url
	else:
		raise ValueError

def user_config():
	generate_initial_config()
	return get_config()

def getSpotifyClient():
	config = user_config()

	auth_manager = SpotifyClientCredentials(
		client_id=config["client_id"],
		client_secret=config["client_secret"],
		cache_handler=CacheFileHandler(cache_path=get_cache_path())
	)
	return Spotify(auth_manager=auth_manager)

instance = None

def spotDLDownloader(args: List[str]):
	global instance

	try:
		sys.argv = [sys.argv[0], *args]
		arguments = parse_arguments()

		spotify_settings, downloader_settings, web_settings = create_settings(arguments)

		if not instance:
			user_config()
			SpotifyClient.init(**spotify_settings)
			init_logging("INFO")
			instance = True

		downloader = Downloader(downloader_settings)

		OPERATIONS[arguments.operation] (
			arguments.query,
			downloader
		)

	except:
		raise
	finally:
		downloader.progress_handler.close()
		if spotify_settings["use_cache_file"]:
			save_spotify_cache(spotify_client.cache)