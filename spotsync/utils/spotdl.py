from pathlib import Path
import subprocess
import json

from utils.theme import print

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

def extract_playlist_name(target_file: Path) -> str:
	try:
		with target_file.open("r", encoding="utf8") as file:
			data = json.load(file)

			url = data["songs"][0]["list_url"]
			if check_spotify_url(url):
				return data["songs"][0]["list_name"]
	except json.JSONDecodeError:
		print(f'[error]ERROR:[/] [object]"{target_file}"[/] file was not created')
		raise

def execute_spotdl(target_dir: Path, args: list):
	try:
		subprocess.run(
			["spotdl", "--log-level", "INFO", *args],
			cwd=target_dir
		).check_returncode()
	except subprocess.CalledProcessError:
		print('[error]ERROR:[/] SpotDL threw an error. Check the traceback for more information')
		raise
	except KeyboardInterrupt:
		print("[warning]Canceling...")
		raise

def syncPlaylist(target_file: Path) -> bool:
	ARGS = ["sync", target_file.name, "--preload"]
	execute_spotdl(target_file.parent, ARGS)
	return True

def createPlaylist(target_dir: Path, target_file: str, url: str) -> bool:
	if check_spotify_url(url):
		ARGS = ["sync", url, "--save-file", target_file]
		execute_spotdl(target_dir, ARGS)
		return True