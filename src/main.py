from game import ChessGame, Launcher, LAUNCHER_FEN_KEY


def main():
	"""Start the app."""
	launcher = Launcher()
	launcher.start_launcher()

	game = ChessGame(launcher.get(LAUNCHER_FEN_KEY))
	game.start()


if __name__ == '__main__':
	main()
