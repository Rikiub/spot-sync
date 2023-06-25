from pathlib import Path
import subprocess
import json

class SpotDLError(Exception):
    pass

class JSONFileNotCreated(Exception):
    pass

def check_spotify_url(url: str) -> str:
	if url.startswith((
		"https://open.spotify.com/playlist/"
	)):
		return url
	else:
		raise ValueError

def check_playlist_changes(target_file: Path, playlist_name: str) -> str:
	if target_file.parent.name != playlist_name:
		return True
	else:
		return False

def createPlaylist(target_dir: Path, url: str):
	try:
		if check_spotify_url(url):
			subprocess.run([
				"spotdl", "--log-level", "INFO",
				"sync", url,
				"--save-file", "data.spotdl"
			], cwd=target_dir).check_returncode()
			return True
	except subprocess.CalledProcessError:
		print('[bold red]ERROR:[/] SpotDL threw an error. Check the traceback for more information')
		raise SpotDLError
	except ValueError:
		print(f'[bold red]ERROR:[/] [green]"{url}"[/] is not a valid Spotify URL')
		raise
	except KeyboardInterrupt:
		print("[bold red]Canceling...")
		raise

def extract_playlist_name(target_file: Path) -> str:
	try:
		with target_file.open("r", encoding="utf8") as file:
			data = json.load(file)

			url = data["songs"][0]["list_url"]
			if check_spotify_url(url):
				return data["songs"][0]["list_name"]
	except json.JSONDecodeError:
		print(f'[bold red]ERROR:[/] [green]"{target_file}"[/] file was not created')
		raise JSONFileNotCreated