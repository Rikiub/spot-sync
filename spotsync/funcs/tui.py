from pathlib import Path

from rich import print
from rich.prompt import Prompt

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
		print(f'\n[bold yellow1]Actual directory: [pink1]"{TARGET_DIR}"[/]\n')

		print("[magenta]1.[/] [blue]Sync my current playlists[/]")
		print("[magenta]2.[/] [blue]Create a new playlist[/]")
		print("[magenta]3.[/] [blue]Change directory[/]")
		print("[magenta]4.[/] [blue]Exit[/]")
		opc = Prompt.ask("\n[bold cyan]What you want do?")

		if opc == "1":
			sync()
		elif opc == "2":
			new()
		elif opc == "3":
			change_dir()
		elif opc == "4" or opc == "q":
			raise SystemExit
		else:
			raise ValueError
	except ValueError:
		print("\n[red]Please enter a valid number")
	except KeyboardInterrupt:
		pass

def sync():
	while True:
		selection = Prompt.ask('\n[bold cyan]You want sync all [red]OR[/] select one directory?', choices=["all", "select"])
		if selection == "all" or selection == "select":
			print()
			break
	Sync(selection, TARGET_DIR, TARGET_FILE)

def new():
	try:
		url = input_url_tui()
		New(url, TARGET_DIR, TARGET_FILE)
	except:
		pass

def change_dir():
	new_dir = Prompt.ask('\n[bold cyan]Insert the new directory')

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
		print(f'\n[bold red]ERROR:[/] The directory [green]"{TARGET_DIR}"[/] not exist')
		raise ValueError