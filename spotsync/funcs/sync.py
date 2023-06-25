from pathlib import Path
import subprocess

from rich import print
from rich.prompt import IntPrompt

from utils.spotdl import check_playlist_changes, extract_playlist_name

def Sync(option: str, target_dir: Path, target_file: str):
	"""
	Sync current Playlists
	"""

	try:
		if target_dir.exists():
			if option == "all":
				directories = search_dirs(target_dir, target_file)

				counter = len(directories)
				for path_object in directories:
					print(f'\n[bold cyan]-> [blue]{counter}[/]')
					execute_file(path_object)
					counter -= 1
			elif option == "select":
				directories = search_dirs(target_dir, target_file)
				selected_dir = select_directory_TUI(directories)

				print(f'\n[bold cyan]-> Selected')
				execute_file(selected_dir)

			print("\n[bold cyan]Sync successful")
		else:
			print(f'[bold red]ERROR:[/] The directory [green]"{target_dir}"[/] not exist')
	except (KeyboardInterrupt, AttributeError, FileNotFoundError, ValueError, subprocess.CalledProcessError):
		pass

def search_dirs(target_dir: Path, target_file: str) -> list:
	directories = [path for path in target_dir.glob('**/' + target_file)]

	if not directories:
		print(f'[bold red]ERROR:[/] No directories found with [green]"{target_file}"[/] file')
		raise FileNotFoundError

	return directories

def execute_file(target_file: Path):
	try:
		print(f'[bold italic yellow]Syncing playlist:[/] [blue]{target_file.parent.name}[/]')

		# execute spotdl
		subprocess.run([
			"spotdl", "--log-level", "INFO",
			"sync", target_file.name, "--preload"
		], cwd=target_file.parent).check_returncode()

		# rename directory if remote playlist was change
		playlist_name = extract_playlist_name(target_file)
		if check_playlist_changes(target_file, playlist_name):
			print('[green]Detected changes in remote Playlist. Renaming directory...')
			target_file.parent.rename(playlist_name)

	except subprocess.CalledProcessError:
		print('[bold red]ERROR:[/] SpotDL threw an error. Check the traceback for more information')
		raise
	except AttributeError:
		print('[bold red]ERROR:[/] Directory not specified')
		raise
	except KeyboardInterrupt:
		print('[bold red]Canceling...')
		raise

def select_directory_TUI(directories: Path) -> Path:
	for index, directory in enumerate(directories, start=1):
		print(f'[bold magenta]{index}.[/] [bright_blue]{directory.parent.name}[/]')

	choice = IntPrompt.ask('\n[bold italic cyan]Choose a directory to sync [blue](1-' + str(len(directories)) + ')[/]')

	if 1 <= choice <= len(directories):
		dirs = directories[choice - 1]
		return dirs
	else:
		print('[red]Please enter a valid index number')
		raise ValueError