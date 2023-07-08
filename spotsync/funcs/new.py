from pathlib import Path

from utils.spotdl import getSpotifyClient, check_spotify_url, SpotifyException, VALID_URLS
from utils.downloader import (
	ConnectionError,
	createPlaylist,
	extract_local_playlist_name
)
from utils.theme import print, input

def New(url: str, output_path: Path, target_file: str):
	"""
	Create a new playlist
	"""

	try:
		# check Spotify URLs
		for url_item in url:
			if check_spotify_url(url_item):
				pass

		sp = getSpotifyClient()

		# loop to process the URLs
		counter = len(url)
		for url_item in url:
			print(f'\n[low]-> [enumerate]{counter}[/]')

			# declare the paths
			p_info = sp.playlist(url_item)
			playlist_path = output_path / p_info["name"]
			spotdl_file = playlist_path / target_file

			# create playlist dir
			playlist_path.mkdir(parents=True, exist_ok=True)

			# if playlist dir is not empty == ERROR
			if any(playlist_path.iterdir()):
				raise FileExistsError

			# spotdl process
			createPlaylist(playlist_path, spotdl_file, url_item)
			counter -= 1

		print("[success]Sync successful")

	except FileExistsError:
		print(f'[warning]The directory [object]"{playlist_path}"[/] already exists and is not empty. Please change the name in the remote Spotify Playlist or delete the duplicated folder')
	except (ValueError, SpotifyException):
		print(url ,'[warning]is not a valid Spotify URL. It must starts with this format:[/]', VALID_URLS)
	except (KeyboardInterrupt, ConnectionError):
		pass