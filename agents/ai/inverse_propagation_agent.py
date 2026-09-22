# Proyecto: Tic-Tac-Toe Engine
# Autor: Santiago Marino
# Email: santiago.mmarino@gmail.com
# Año de desarrollo: 2026

import os

import joblib
import numpy as np
from tictactoe_engine import PlayerAgent
from sklearn.neural_network import MLPRegressor

GAME = 0
REWARD = 1
STATE = 2
WINNER = 3


def get_random_action(state):
    """Elige al azar una de las acciones disponibles del tablero."""
    available_actions = get_available_actions(state)
    return np.random.choice(available_actions)

def get_available_actions(state):
    """Devuelve los indices de las casillas vacias del estado."""
    return [i for i, x in enumerate(state) if x is None]

def is_first_move(state):
    """Indica si el tablero no contiene ningun movimiento."""
    return all(x is None for x in state)


def encode_state(state, own_marker):
    """Convierte el tablero en valores numericos desde la perspectiva del agente."""
    return [
        0 if cell is None else 1 if cell == own_marker else -1
        for cell in state
    ]


def encode_state_action(state, own_marker, action):
    """Representa un estado junto con la accion que se esta evaluando."""
    action_encoding = [0] * 9
    action_encoding[action] = 1
    return encode_state(state, own_marker) + action_encoding


def update_targets(value, targets, target_rate=0.9, penalty='soft'):
    """Propaga hacia atras el resultado de una partida sobre sus jugadas.

    Los valores intermedios se reducen con ``target_rate`` y una penalizacion
    distinta para victorias y derrotas, para entrenar al modelo con el contexto
    de toda la secuencia.
    """
    if value == 1:
        n = len(targets) - 1
        for i in range(n - 1, -1, -1):
            if targets[i] == 0:
                if penalty == 'soft':
                    targets[i] = np.power(targets[i + 1] * target_rate, 2)
                elif penalty == 'hard': 
                    targets[i] = np.power(targets[i + 1] * target_rate, 4)
            else:
                break
        print(f"Ganaste la partida {len(targets)}:{targets}")

    elif value == -1:
        n = len(targets) - 1
        for i in range(n - 1, -1, -1):
            if targets[i] == 0:
                if penalty == 'soft':
                    targets[i] = np.power(targets[i + 1] * target_rate, 3)
                elif penalty == 'hard': 
                    targets[i] = np.power(targets[i + 1] * target_rate, 5)
            else:
                break
        print(f"Perdiste la partida {len(targets)}:{targets}")

    else:
        print(f"Empate en la partida {len(targets)}:{targets}")



class InversePorpagationAgent(PlayerAgent):

    def __init__(
        self,
        playerID=0,
        name="AI Player",
        target_rate=0.9,
        penalty='soft',
        load_model=True,
        epsilon=0.2,
        use_replay=True,
    ):
        """Inicializa un agente, su modelo opcional y sus datos de entrenamiento."""
        self.playerID = playerID
        self.player_name = name
        self.features = []
        self.target = []
        self.target_rate = target_rate
        self.penalty = penalty
        self.epsilon = epsilon
        self.use_replay = use_replay
        self.replay_features = []
        self.replay_targets = []
        self.marker = None
        self.load_model = load_model
        self.model_path = f"{self.player_name}_model.pkl"
        self.model = joblib.load(self.model_path) if load_model and os.path.exists(self.model_path) else None


    def act(self, state):
        """Selecciona una jugada mediante exploracion aleatoria o el modelo."""
        self.state = state

        available_actions = get_available_actions(self.state)
        if self.model is None or np.random.random() < self.epsilon:
            action = np.random.choice(available_actions)
        else:
            candidate_states = []
            for action in available_actions:
                candidate_states.append(
                    encode_state_action(self.state, self.marker, action)
                )

            predictions = self.model.predict(candidate_states)
            best_index = max(
                range(len(available_actions)), key=predictions.__getitem__
            )
            action = available_actions[best_index]

        # Guardamos el estado previo y la accion; el valor se conoce al final.
        self.features.append(
            encode_state_action(self.state, self.marker, action)
        )
        self.target.append(0.0)
        next_state = self.state.copy()
        next_state[action] = self.marker
        self.state = next_state

        if is_first_move(self.state):
            print(f"{self.player_name} es el primer jugador.")

        print(f"{self.player_name} el tablero es \n{np.array(self.state).reshape(3,3)}")
        print(f"{self.player_name} elige la casilla {action + 1}")
        return (action)


    def event(self, message):
        """Recibe eventos del motor y entrena el modelo al terminar la partida."""
        if isinstance(message, tuple) and message[0] == "end":
            m = message
        else:
            m = message.split("%")

        if m[0] not in ("status", "end"):
            return

        if m[0] == "status":
            print(f"{self.player_name} recibe el estado: {m[1]}\n\n\n\n")

        if m[0] == "end":
            print(f"{self.player_name} Fin partida: {m[1]}\n\n\n\n")
            msg_winner = m[1][3]["winner"]


            if msg_winner is None:
                self.target[-1] = 0.0
                update_targets(0, self.target, self.target_rate, self.penalty)
            elif msg_winner == self.playerID:
                self.target[-1] = 1.0
                update_targets(1, self.target, self.target_rate, self.penalty)
            else:
                self.target[-1] = -1.0
                update_targets(-1, self.target, self.target_rate, self.penalty)

            if self.model is None and self.load_model and os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)

            if not isinstance(self.model, MLPRegressor):
                self.model = MLPRegressor(
                    hidden_layer_sizes=(256, 128, 64, 32, 16),
                    activation="relu",
                    solver="adam",
                    learning_rate_init=0.01,
                    max_iter=1,
                    shuffle=False,
                    random_state=42,
                )

            if self.use_replay:
                self.replay_features.extend(self.features)
                self.replay_targets.extend(self.target)
                training_features = self.replay_features
                training_targets = self.replay_targets
            else:
                training_features = self.features
                training_targets = self.target

            self.model.partial_fit(training_features, training_targets)
            joblib.dump(self.model, self.model_path)
            self.features.clear()
            self.target.clear()
            self.epsilon = max(0.05, self.epsilon * 0.999)