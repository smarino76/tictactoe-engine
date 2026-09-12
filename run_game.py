# Proyecto: Tic-Tac-Toe Engine
# Autor: Santiago Marino
# Email: santiago.mmarino@gmail.com
# Año de desarrollo: 2026

from tictactoe_engine import TicTacToe
from agent_human import Player as HumanPlayer
from expert_ai_agent import ExpertAIAgent
import numpy as np



player_1 = HumanPlayer(playerID=0, name="Humano")
player_2 = ExpertAIAgent(name="AI Player 2")




game = TicTacToe(player_1, player_2)

def validate_action(action):
    """Comprueba que la accion esta dentro del tablero y apunta a una casilla libre."""
    if action >= 0 and action < 9:
        if game.state[action] is None:
            return True
    return False

def players_sync_broadcast(msg):
    """Envia el mismo mensaje a los dos agentes de la partida."""
    for pl in range(2):
        game.sync(game.players.get(pl), msg)


players_sync_broadcast("start% inizializing game")
state = game.reset()

state_matrix = np.array(state).reshape(3,3)

print("Cargando el juego...")
print("########## TicTacToe #########")

print(state_matrix)



status = None
while not game.done:
    player = game.players.get(game.current_player)
    game.sync(game.players.get(game.current_player), f"move% {game.state}")
    action = player.act(game.state)
    

    if validate_action(action):
        status = game.step(action)
        #print(f"\n{np.array(game.state).reshape(3,3)}")
        #game.sync(game.players.get(game.current_player), f"status% {status}")
    else:
        game.sync(game.players.get(game.current_player), "canceled% game canceled")
        print(f"Casilla no valida.. el player {game.current_player} perdio la partida")
        exit(0)

players_sync_broadcast(("end", status))