# Proyecto: Tic-Tac-Toe Engine
# Autor: Santiago Marino
# Email: santiago.mmarino@gmail.com
# Año de desarrollo: 2026
# Descripción: Entrenamiento por autojuego de los agentes de aprendizaje.

"""Bucle de entrenamiento de los agentes IA mediante partidas de autojuego."""

import argparse
import contextlib
import io
import sys

import agents.ai.critical_move_propagation_agent as cma
import agents.ai.inverse_propagation_agent as ipa
from tictactoe_engine import TicTacToe


def play_game(game):
	"""Ejecuta una partida completa y comunica el resultado a cada agente."""
	game.reset()
	starting_player = game.current_player
	for player_id, player in game.players.items():
		player.started_first = player_id == starting_player

	while not game.done:
		player = game.players[game.current_player]
		action = player.act(game.state)

		if action not in game.valid_actions():
			raise RuntimeError(
				f"{player.player_name} eligio una accion invalida: {action}"
			)

		game.step(action)

	final_state = game.state
	for player in game.players.values():
		player.state = final_state

	result = (
		final_state,
		{
			0: 1 if game.winner == 0 else -1 if game.winner == 1 else 0,
			1: 1 if game.winner == 1 else -1 if game.winner == 0 else 0,
		},
		game.done,
		{"winner": game.winner},
	)

	for player in game.players.values():
		player.event(("end", result))


def train(number_of_games, use_replay=True):
	"""Entrena dos agentes mediante el numero de partidas indicado."""
	player_1 = cma.CriticalMovePropagationAgent(
		name="AI Player 1",
		load_model=False,
		penalty="hard",
		epsilon=0.3,
		use_replay=use_replay,
	)
 
	player_2 = ipa.InversePropagationAgent(
		name="AI Player 2",
		load_model=False,
		penalty="hard",
		epsilon=0.15,
		use_replay=use_replay,
	)
	game = TicTacToe(player_1, player_2)

	progress_width = 40
	for game_number in range(1, number_of_games + 1):
		with contextlib.redirect_stdout(io.StringIO()):
			play_game(game)

		completed = int(progress_width * game_number / number_of_games)
		progress = "#" * completed + "-" * (progress_width - completed)
		print(
			f"\rEntrenando [{progress}] {game_number}/{number_of_games}",
			end="",
			flush=True,
			file=sys.stdout,
		)

	print(f"\nEntrenamiento completado: {number_of_games} partidas.")


def main():
	"""Lee los argumentos de consola y pone en marcha el entrenamiento."""
	parser = argparse.ArgumentParser(
		description="Entrena los agentes de tres en raya."
	)
	parser.add_argument(
		"number_of_games",
		nargs="?",
		type=int,
		default=4000,
		help="Numero de partidas a ejecutar (por defecto: 4000).",
	)
	parser.add_argument(
		"--no-replay",
		dest="use_replay",
		action="store_false",
		default=True,
		help="Entrena cada partida solo con sus propios datos.",
	)
	args = parser.parse_args()

	if args.number_of_games < 1:
		parser.error("number_of_games debe ser mayor que cero")

	train(args.number_of_games, use_replay=args.use_replay)


if __name__ == "__main__":
	main()
