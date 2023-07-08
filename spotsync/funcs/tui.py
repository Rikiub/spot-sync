from pathlib import Path

from utils.downloader import check_dir
from utils.spotdl import check_spotify_url, VALID_URLS
from utils.theme import print, input

from .sync import Sync, SYNC_OPS
from .new import New

OPERATIONS = ("start", "sync", "new")

def TUI(operation: str, output_path: Path, target_file: str):
	"""
	Friendly interactive TUI
	"""

	global OUTPUT_PATH, TARGET_FILE
	OUTPUT_PATH = output_path
	TARGET_FILE = target_file

	if operation[0] == OPERATIONS[0]:
		start()
	elif operation[0] == OPERATIONS[1]:
		sync()
	elif operation[0] == OPERATIONS[2]:
		new()
	else:
		print(f'error: Invalid operation because is expected:', *OPERATIONS)

def start():
	try:
		print(f'\n[high]Actual directory: [object]"{OUTPUT_PATH}"[/]\n')

		print("[enumerate]1.[/] [item]Sync my current playlists[/]")
		print("[enumerate]2.[/] [item]Create a new playlist[/]")
		print("[enumerate]3.[/] [item]Change directory[/]")
		print("[enumerate]4.[/] [item]Exit[/]")
		opc = int(input("\n[low]What you want do?[/]: "))

		if opc == 1:
			sync()
		elif opc == 2:
			new()
		elif opc == 3:
			change_dir()
		elif opc == 4:
			raise SystemExit
		else:
			raise ValueError
	except ValueError:
		print("[warning]Please enter a valid number")
	except KeyboardInterrupt:
		pass

def sync():
	while True:
		selection = input(f'\n[low]You want sync all [high]OR[/] select one directory?[/] [choices]\[all/select][/]: ')
		if selection in SYNC_OPS:
			break
		else:
			print("[warning]Please enter a valid option")
	Sync(selection, OUTPUT_PATH, TARGET_FILE)

def new():
	try:
		url = input_url()
		print()
		New(url, OUTPUT_PATH, TARGET_FILE)
	except ValueError:
		pass

def change_dir():
	new_dir = input('\n[low]Insert the new directory[/]: ')

	try:
		if check_dir(new_dir):
			global OUTPUT_PATH
			OUTPUT_PATH = new_dir
			start()
	except ValueError:
		print(f'[warning]The directory [object]"{OUTPUT_PATH}"[/] not exist')
		start()

def input_url() -> list:
	url_list = [item for item in input('\n[low]Insert a valid Spotify URL[/]: ').split()]

	for url in url_list:
		try:
			check_spotify_url(url)
		except ValueError:
			print(f'[warning][object]"{url}"[/] is not a valid Spotify URL. Its must follow this format: [object]{VALID_URLS}[/]')
			raise

	if url_list[0] == "q":
		raise SystemExit

	return url_list