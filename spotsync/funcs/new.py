from pathlib import Path

from utils.spotdl import spotDLSyncer, getSpotifyClient, check_spotify_url, SpotifyException, ConnectionError
from utils.extractors import extract_local_playlist_name

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
			playlist_data = sp.playlist(url_item)
			playlist_path = output_path / playlist_data["name"]

			# create playlist dir
			playlist_path.mkdir(parents=True, exist_ok=True)

			# if playlist dir is not empty, error got
			if any(playlist_path.iterdir()):
				raise FileExistsError

			# spotdl process
			spotDLSyncer(
				query=url_item,
				output_path=playlist_path,
				save_file=target_file
			)
			counter -= 1

		print("[success]Sync successful")

	except FileExistsError:
		print(f'[warning]The directory [object]"{playlist_path}"[/] already exists and is not empty. Please change the name in the remote Spotify Playlist or delete the duplicated folder')
	except (ValueError, KeyboardInterrupt, ConnectionError):
		pass