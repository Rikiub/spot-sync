from pathlib import Path
from time import sleep
import subprocess
import shutil
import json
import sys

class DIR:
    start_path = Path(__file__).resolve().parent
    temp_path = Path(start_path, "__TEMP__")

    sync_script = "sync-playlist.py"
    json_file = "data.spotdl"

    @classmethod
    def create_temp_dir(cls):
        if cls.temp_path.exists():
            cleanup()
        cls.temp_path.mkdir(parents=True, exist_ok=True)

    @classmethod
    def delete_dir(cls, directory: Path):
        shutil.rmtree(directory)

    @classmethod
    def create_sync_script(cls):
        with open(Path(DIR.temp_path, DIR.sync_script), "w") as file:
            file.write(
"""from pathlib import Path
from time import sleep
import subprocess

DIR = Path(__file__).resolve().parent
JSON_FILE = "data.spotdl"

if Path(DIR, JSON_FILE).exists():
    subprocess.run([
        "spotdl",
        "sync", "data.spotdl", "--preload"
    ], cwd=DIR)
else:
    print("ERROR: 'data.spodl' file not found! Sync failed.")
    sleep(2.0)
"""
            )

    @classmethod
    def rename_temp_dir(cls, name):
        cls.temp_path.rename(name)

class SpotDL:
    type = ""

    def start_spotdl(url):
        try:
            if url.startswith((
                "https://open.spotify.com/playlist/",
                "https://open.spotify.com/album/"
            )):
                subprocess.run([
                    "spotdl",
                    "sync", url, "--save-file", "data.spotdl"
                ], cwd=DIR.temp_path)
                if "playlist" in url:
                    SpotDL.type = "playlist"
                elif "album" in url:
                    SpotDL.type = "album"
                return True
            else:
                error()
        except:
            return False

    def extract_playlist_name():
        with open(Path(DIR.temp_path, DIR.json_file), "r", encoding="utf8") as file:
            data = json.load(file)
            if "playlist" in SpotDL.type:
                return data["songs"][0]["list_name"]
            elif "album" in SpotDL.type:
                return data["songs"][0]["album_name"]

def cleanup():
    DIR.delete_dir(DIR.temp_path)

def main():
    print("Insert Spotify Playlist/Album URL")
    url = input(">> ")

    DIR.create_temp_dir()
    if not SpotDL.start_spotdl(url):
        print("\nERROR: The URL not is a valid Spotify Playlist/Album!")
        sleep(2.0)
        cleanup()
        sys.exit()

    type_name = SpotDL.extract_playlist_name()
    new_dir = Path(DIR.temp_path.parent, type_name)

    if new_dir.exists():
        print("\nERROR: The folder/playlist already exists")
        sleep(2.0)
        cleanup()
        sys.exit()
    else:
        DIR.create_sync_script()
        DIR.rename_temp_dir(new_dir)

        print("\nSync completed!")
        sleep(2.0)

if __name__ == "__main__":
    main()