from utils.arguments import parseArguments, OPERATIONS

if __name__ == '__main__':
	TARGET_FILE = ".spotdl"

	# start CLI
	args = parseArguments()

	OPERATIONS[args.operation] (
		args.query,
		args.output,
		TARGET_FILE
	)