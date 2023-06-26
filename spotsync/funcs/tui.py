from pathlib import Path

from utils.theme import print, input

from .sync import Sync
from .new import New, input_url_tui

def TUI(selection: str, target_dir: Path, target_file: str):
	"""
	Friendly interactive TUI
	"""

	global TARGET_DIR, TARGET_FILE
	TARGET_DIR = target_dir
	TARGET_FILE = target_file

	if selection == "sync":
		sync()
	elif selection == "new":
		new()
	else:
		start()

def start():
	try:
		print(f'\n[high]Actual directory: [path]"{TARGET_DIR}"[/]\n')

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
		selection = input('\n[low]You want sync all [high]OR[/] select one directory?[/] [choices]\[all/select][/]: ')
		if selection == "all" or selection == "select":
			break
		else:
			print("[warning]Please enter a valid option")
	Sync(selection, TARGET_DIR, TARGET_FILE)

def new():
	try:
		url = input_url_tui()
		New(url, TARGET_DIR, TARGET_FILE)
	except:
		pass

def change_dir():
	new_dir = input('\n[low]Insert the new directory')

	try:
		if check_dir(new_dir):
			global TARGET_DIR
			TARGET_DIR = new_dir
			start()
	except ValueError:
		start()

def check_dir(path):
	path = Path(path)
	if path.exists():
		return path
	else:
		print(f'\n[error]ERROR:[/] The directory [object]"{TARGET_DIR}"[/] not exist')
		raise ValueError