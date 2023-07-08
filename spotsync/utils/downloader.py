from pathlib import Path
import json

from requests import ConnectionError

from utils.spotdl import spotDLDownloader
from utils.theme import print

def get_cwd() -> Path:
	return Path.cwd()

def check_dir(path) -> Path:
	path = Path(path)
	if path.exists():
		return path
	else:
		raise ValueError

def check_playlist_changes(target_file: Path, playlist_name: str) -> bool:
	if target_file.parent.name != playlist_name:
		return True

def extract_local_playlist_name(target_file: Path) -> str:
	try:
		with target_file.open("r", encoding="utf8") as file:
			data = json.load(file)
			return data["songs"][0]["list_name"]
	except json.JSONDecodeError:
		raise json.JSONDecodeError(f'"{target_file}" file was not created')

def execute_spotdl(arguments: list, directory):
	try:
		arguments = [
			*arguments,
			"--output", str(f"{directory}" + "/{artists} - {title}.{output-ext}")
		]
		spotDLDownloader(arguments)

	except KeyboardInterrupt:
		print("[warning]Canceling...")
		raise
	except ConnectionError:
		print('[warning]Failed to connect to the internet')
		raise

def syncPlaylist(target_file: Path) -> bool:
	arguments = [
		"sync", str(target_file), "--preload",
	]
	execute_spotdl(arguments, target_file.parent)
	return True

def createPlaylist(output_path: Path, target_file: Path, url: str) -> bool:
	arguments = [
		"sync", url,
		"--save-file", str(target_file),
	]
	execute_spotdl(arguments, output_path)
	return True