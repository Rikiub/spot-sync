from argparse import ArgumentParser, Namespace

from funcs.sync import Sync, SYNC_OPS
from funcs.new import New
from funcs.tui import TUI
from utils.spotdl import check_spotify_url, VALID_URLS
from utils.downloader import (
    check_dir,
    get_cwd
)

OPERATIONS = {
	"sync": Sync,
	"new": New,
	"tui": TUI
}

def parseArguments() -> Namespace:
	"""
	CLI: argparse initizalizer
	"""

	parser = ArgumentParser(
		prog="SpotDL-Syncer",
		description="a extension of SpotDL to create and maintain Spotify Playlists"
	)
	parser.add_argument(
		"operation",
		help="what you want do?",
		choices=OPERATIONS.keys(), type=str
	)
	parser.add_argument(
		"query",
		help=(
			'SYNC: "all", "select" - To sync your current playlists | NEW: "url" - To create a new playlist the url must follow this format: "https://open.spotify.com/playlist/" | TUI: "start" - A friendly interface to use the commands'
		),
		nargs="+", type=str
	)
	parser.add_argument(
		"-o", "--output",
		help="directory where the playlists will be stored",
		default=get_cwd(), type=check_dir
	)

	return parser.parse_args()