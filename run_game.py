# Proyecto: Tic-Tac-Toe Engine
# Autor: Santiago Marino
# Email: santiago.mmarino@gmail.com
# Año de desarrollo: 2026
# Descripción: Punto de entrada para ejecutar una partida humana contra el agente experto.

"""Ejecuta una partida interactiva en terminal contra el agente experto."""

from agents.agent_human import Player as HumanPlayer
from expert_ai_agent import ExpertAIAgent
from tictactoe_engine import TicTacToe



player_1 = HumanPlayer(playerID=0, name="Humano")
player_2 = ExpertAIAgent(name="AI Player 1")

game = TicTacToe(player_1, player_2)


def validate_action(action):
    """Comprueba que la accion esta dentro del tablero y apunta a una casilla libre."""
    return 0 <= action < 9 and game.state[action] is None

def players_sync_broadcast(msg):
    """Envia el mismo mensaje a los dos agentes de la partida."""
    for pl in range(2):
        game.sync(game.players.get(pl), msg)


def draw_board(state):
    """Redibuja el tablero en una posicion fija de la terminal."""
    print("\033[2J\033[H", end="")
    print("########## TicTacToe #########")
    print()
    for row in range(3):
        cells = []
        for column in range(3):
            index = row * 3 + column
            cells.append(state[index] or str(index + 1))
        print(f" {cells[0]} | {cells[1]} | {cells[2]} ")
        if row < 2:
            print("---+---+---")
    print()


state = game.reset()

draw_board(state)



while not game.done:
    player = game.players.get(game.current_player)
    game.sync(game.players.get(game.current_player), f"move% {game.state}")
    action = player.act(game.state)
    

    if validate_action(action):
        status = game.step(action)
        draw_board(game.state)
    else:
        game.sync(game.players.get(game.current_player), "canceled% game canceled")
        print(f"Casilla no valida.. el player {game.current_player} perdio la partida")
        raise SystemExit(1)

players_sync_broadcast(("end", status))