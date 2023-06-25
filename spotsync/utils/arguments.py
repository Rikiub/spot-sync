from argparse import ArgumentParser, _ArgumentGroup, Namespace
from pathlib import Path

from utils.spotdl import check_spotify_url

CWD = Path.cwd()

def check_dir(path) -> Path:
	"""
	Validation function to check if argparse "directory" is valid
	"""

	path = Path(path)
	if path.exists():
		return path
	else:
		raise ValueError

def parse_sync(parser: _ArgumentGroup):
	parser = parser.add_parser(
		"sync",
		help='synchronizes the directories created with "new" command. Uses a directory as a base'
	)
	parser.add_argument(
		"selection",
		help="use 'select' to show the TUI selector, use 'all' to synchronize every available directory",
		choices=["all", "select"], default="all", type=str
	)
	parser.add_argument(
		"-d", "--directory",
		help="directory where the playlists will be stored",
		default=CWD, type=check_dir
	)

def parse_new(parser: _ArgumentGroup):
	parser = parser.add_parser(
		"new",
		help='create a new playlist with Spotify URLs. Accepted formats: "http://open.spotify.com/playlist/", "http://open.spotify.com/album/"'
	)
	parser.add_argument(
		"url",
		help="Spotify URL to process",
		nargs="+", type=check_spotify_url
	)
	parser.add_argument(
		"-d", "--directory",
		help="directory where the playlists will be stored",
		default=CWD, type=check_dir
	)

def parse_tui(parser: _ArgumentGroup):
	parser = parser.add_parser(
		"tui",
		help='A friendly interactive TUI to uses the "sync" and "new" commands'
	)
	parser.add_argument(
		"selection",
		help='"Start the TUI in a point"',
		choices=["sync", "new"],
		nargs="?", type=str
	)
	parser.add_argument(
		"-d", "--directory",
		help="directory where the playlists will be stored",
		default=CWD, type=check_dir
	)

def parseArguments() -> Namespace:
	"""
	CLI: argparse initizalizer
	"""

	parser = ArgumentParser(
		prog="SpotDL-Syncer",
		description="a extension of SpotDL to create and maintain Spotify Playlists"
	)
	subparsers = parser.add_subparsers(
		dest="command",
		help="sub-command help"
	)

	parse_sync(subparsers)
	parse_new(subparsers)
	parse_tui(subparsers)

	return parser.parse_args()