from funcs.sync import Sync
from funcs.new import New
from funcs.tui import TUI

from utils.arguments import parseArguments

if __name__ == '__main__':
	try:
		TARGET_FILE = "data.spotdl"

		# start CLI
		args = parseArguments()

		if args.command == "sync":
			Sync(args.selection, args.directory, TARGET_FILE)
		elif args.command == "new":
			New(args.url, args.directory, TARGET_FILE)
		elif args.command == "tui":
			TUI(args.selection, args.directory, TARGET_FILE)
	except KeyboardInterrupt:
		pass