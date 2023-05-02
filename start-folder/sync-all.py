from pathlib import Path
import subprocess

START_DIR = Path(__file__).resolve().parent

def search_files(query):
    for path_object in START_DIR.rglob(query):
        execute_file(path_object)

def execute_file(file_path):
    DIR = Path(file_path).parent

    print("\nUpdating playlist:", DIR)
    subprocess.run(["python", file_path], cwd=DIR)

search_files("sync-playlist.py")