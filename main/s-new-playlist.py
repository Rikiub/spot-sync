from pathlib import Path
from time import sleep
import subprocess
import shutil
import json
import sys

class DIR:
	start_dir = Path(__file__).resolve().parent
	temp_dir = Path(start_dir, "__TEMP__")

	sync_script = "sync-playlist.py"
	json_file = "data.spotdl"

	@classmethod
	def create_temp_dir(cls):
		dir = cls.temp_dir

		if dir.exists():
			cls.delete_temp()
		dir.mkdir(parents=True)

	@classmethod
	def delete_temp(cls):
		dir = cls.temp_dir
		shutil.rmtree(dir)

	@classmethod
	def rename_temp_dir(cls, name):
		cls.temp_dir.rename(name)

class SpotDL:
	type = ""

	def start_spotdl(url):
		try:
			if url.startswith((
				"https://open.spotify.com/playlist/",
				"https://open.spotify.com/album/"
			)):
				subprocess.run([
					"spotdl", "--log-level", "ERROR",
					"sync", url, "--save-file", "data.spotdl"
				], cwd=DIR.temp_dir)

				if "playlist" in url:
					SpotDL.type = "playlist"
				elif "album" in url:
					SpotDL.type = "album"

				return True
			else:
				error()
		except (NameError, subprocess.CalledProcessError):
			return False
		except KeyboardInterrupt:
			print("\nCanceling...")
			exit()

	def extract_playlist_name():
		file = Path(DIR.temp_dir, DIR.json_file)

		if file.exists():
			open(file, "r", encoding="utf8")
			data = json.load(file)

			if "playlist" in SpotDL.type:
				return data["songs"][0]["list_name"]
			elif "album" in SpotDL.type:
				return data["songs"][0]["album_name"]
		else:
			print("\nERROR: 'data.spotdl' file was not created!")
			exit()

def exit():
	DIR.delete_temp()
	sleep(2.0)
	sys.exit()

def main():
	d = DIR()

	print("Insert a valid Spotify Playlist/Album URL")
	url = input(">> ")

	d.create_temp_dir()
	if not SpotDL.start_spotdl(url):
		print("\nERROR: It's not a valid Spotify URL!")
		exit()

	type_name = SpotDL.extract_playlist_name()
	new_dir = Path(d.temp_dir.parent, type_name)

	if new_dir.exists():
		print("\nERROR: The folder/playlist already exists")
		exit()
	else:
		d.rename_temp_dir(new_dir)

		print("\nSync completed!")
		exit()

if __name__ == "__main__":
	main()