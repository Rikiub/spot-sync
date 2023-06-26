from pathlib import Path

from utils.spotdl import (
	syncPlaylist,
	check_playlist_changes,
	extract_playlist_name,
	subprocess
)
from utils.theme import print, input

def Sync(operation: str, target_dir: Path, target_file: str):
	"""
	Sync current Playlists
	"""

	try:
		# getting directories path
		directories = search_dirs(target_dir, target_file)

		if operation == "all":
			counter = len(directories)
			for path_object in directories:
				print(f'\n[low]-> [enumerate]{counter}[/]')
				execute_file(path_object)
				counter -= 1
		elif operation == "select":
			selected_dir = select_directory_TUI(directories)

			print(f'\n[low]-> Selected')
			execute_file(selected_dir)
		else:
			raise ValueError('Not specified operation type. Expected "all" or "select"')

		print("\n[success]Sync successful")

	except (ValueError, subprocess.CalledProcessError):
		pass
	except Exception as e:
		print(e)

def search_dirs(target_dir: Path, target_file: str) -> list:
	directories = [path for path in target_dir.glob('**/' + target_file)]

	if not directories:
		print(f'[error]ERROR:[/] No directories found with [object]"{target_file}"[/] file')
		raise FileNotFoundError

	return directories

def execute_file(target_file: Path):
	print(f'[high]Syncing playlist:[/] [item]{target_file.parent.name}[/]')

	# execute spotdl
	if syncPlaylist(target_file):

		# rename directory if remote playlist was change
		playlist_name = extract_playlist_name(target_file)
		if check_playlist_changes(target_file, playlist_name):
			print('[spotdl_log]Detected changes in remote Playlist. Renaming directory...')
			target_file.parent.rename(playlist_name)

def select_directory_TUI(directories: list) -> Path:
	print()
	for index, directory in enumerate(directories, start=1):
		print(f'[enumerate]{index}.[/] [item]{directory.parent.name}[/]')

	try:
		choice = int(input('\n[low]Choose a directory to sync[/] [enumerate][1-' + str(len(directories)) + '][/]: '))

		if 1 <= choice <= len(directories):
			dirs = directories[choice - 1]
			return dirs
		else:
			raise ValueError
	except ValueError:
		print('[warning]Please enter a valid index number')
		raise