from pathlib import Path
import shutil

from rich import print
from rich.prompt import Prompt

from utils.spotdl import createPlaylist, extract_playlist_name, SpotDLError, JSONFileNotCreated

def New(url: str, target_dir: Path, target_file: str, tui=False):
	"""
	Create a new playlist
	"""

	temp_dir = Path(target_dir, "__TEMP__")
	json_file = Path(temp_dir, target_file)

	try:
		# check if TUI is True
		if tui:
			url = input_url_tui()

		# loop to process the URLs
		counter = len(url)
		for url in url:
			print(f'[bold cyan]-> [blue]{counter}[/]')

			# create temp_dir
			if temp_dir.exists():
				shutil.rmtree(temp_dir)
			temp_dir.mkdir(parents=True)

			# spotdl process
			if createPlaylist(temp_dir, url):
				playlist_name = extract_playlist_name(json_file)
				new_dir = Path(target_dir, playlist_name)

				if new_dir.exists():
					print("[bold red]ERROR:[/] The directory already exists")
					raise FileExistsError
				else:
					temp_dir.rename(new_dir)
					counter -= 1
		print("\n[bold cyan]Sync successful")
	except (FileExistsError, ValueError, KeyboardInterrupt, SpotDLError, JSONFileNotCreated):
		shutil.rmtree(temp_dir)

def input_url_tui() -> list:
	url_list = [item for item in Prompt.ask('\n[bold italic cyan]Insert a valid Spotify URL').split()]
	print()

	for url in url_list:
		try:
			if SpotDLDownloader.check_url(url):
				pass
		except ValueError:
			print(f'[bold red]ERROR:[/] [green]"{url}"[/] is not a valid Spotify URL')
			raise

	if url_list[0] == "q":
		raise SystemExit

	return url_list