from game import ChessGame, Launcher


def main():
	"""Start the app."""
	launcher = Launcher()
	launcher.start_launcher()

	game = ChessGame()
	game.start()


if __name__ == '__main__':
	main()
