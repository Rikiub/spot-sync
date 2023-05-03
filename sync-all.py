from pathlib import Path
from time import sleep
import subprocess

START_DIR = Path(__file__).resolve().parent

def search_files(query):
    for path_object in START_DIR.rglob(query):
        execute_file(path_object)

def execute_file(file_path):
    FILE_DIR = Path(file_path).parent

    print("\nUpdating playlist:", FILE_DIR)
    subprocess.run(["python", file_path], cwd=FILE_DIR)

try:
    search_files("sync-playlist.py")
    
    print("\nSync completed!")
    sleep(2.0)
except:
    print("\nERROR")
    sleep(2.0)