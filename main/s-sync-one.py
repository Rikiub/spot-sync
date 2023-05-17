from pathlib import Path
from time import sleep
import subprocess
import sys
from rich.console import Console

console = Console()

def get_directories_with_file(file_name):
	cwd = Path(__file__).resolve().parent
	directories = [path.parent.name for path in cwd.glob('**/' + file_name)]
	return directories

def list_directories(directories):
	for index, directory in enumerate(directories, start=1):
		print(f'{index}. "{directory}"')

def select_directory(directories):
	print('\nChoose a directory to sync (1-' + str(len(directories)) + ') or enter "q" to quit.')
	choice = input(">> ")

	if choice.lower() == 'q':
		sys.exit()

	try:
		index = int(choice)
		if 1 <= index <= len(directories):
			dir = directories[index - 1]
			execute_file(dir)
		else:
			error()
	except (ValueError, ModuleNotFoundError):
		print('Invalid choice. Please enter a valid number.')
		sys.exit()

	print("\nSync completed!")
	sleep(2.0)

def execute_file(dir):
	console.print("\n[bold yellow]Updating playlist:[/]", dir)

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
	directories = get_directories_with_file('data.spotdl')
	list_directories(directories)
	select_directory(directories)
