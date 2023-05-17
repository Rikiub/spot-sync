from pathlib import Path
from time import sleep
import subprocess
import sys
from rich.console import Console

console = Console()

def search_files(query):
	cwd = Path(__file__).resolve().parent

	for path_object in cwd.rglob(query):
		execute_file(path_object)

def execute_file(dir):
	dir_name = dir.parent.name
	dir = dir.parent

	console.print("\n[bold yellow]Updating playlist:[/]", dir_name)

	try:
		subprocess.run([
			"spotdl",
			"sync", "data.spotdl", "--preload"
		], cwd=dir)
	except (subprocess.CalledProcessError, KeyboardInterrupt):
		console.print("\n[bold red]Canceling...[/]")
		sleep(2.0)
		sys.exit()

if __name__ == '__main__':
	search_files("data.spotdl")

	print("\nSync completed!")
	sleep(2.0)