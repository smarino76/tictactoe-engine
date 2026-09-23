# Proyecto: Tic-Tac-Toe Engine
# Autor: Santiago Marino
# Email: santiago.mmarino@gmail.com
# Año de desarrollo: 2026
# Descripción: Motor principal del juego y contrato base para agentes.

"""Motor principal del juego y contrato base para los agentes del proyecto."""

import random
from abc import ABC, abstractmethod


class PlayerAgent(ABC):
    @abstractmethod
    def act(self, state):
        """Elige y devuelve una accion valida para el estado recibido."""
        pass

    @abstractmethod
    def event(self, message):
        """Procesa una notificacion enviada por el motor de juego."""
        pass
 

class TicTacToe:

    def __init__(self, player_0, player_1):
        """Crea una partida y registra los dos agentes participantes."""
        player_0.playerID = 0
        player_1.playerID = 1
        # Players participating in the game
        self.players = {
            0: player_0,
            1: player_1
        }

        self.board = None
        self.current_player = None
        self.player_markers = None
        self.done = False
        self.winner = None

    def sync(self, player, message):
        """Entrega un mensaje a un agente para mantenerlo sincronizado."""
        player.event(message)


    def reset(self):
        """Reinicia la partida, los marcadores y el jugador que comienza."""

        # Empty board
        self.board = [None] * 9

        self.done = False
        self.winner = None

        # Randomly assign X and O
        markers = ["X", "O"]
        random.shuffle(markers)

        self.player_markers = {
            0: markers[0],
            1: markers[1]
        }

        for player_id, marker in self.player_markers.items():
            self.players[player_id].marker = marker

        # Randomly choose who starts
        self.current_player = random.choice([0, 1])

        return self.state


    @property
    def state(self):
        """Devuelve una copia del tablero para evitar cambios externos."""

        return self.board.copy()


    def valid_actions(self):
        """Devuelve los indices de las casillas que aun estan disponibles."""

        return [
            i
            for i, cell in enumerate(self.board)
            if cell is None
        ]


    def step(self, action):
        """Ejecuta una jugada y devuelve estado, recompensas, fin e informacion.

        La recompensa es positiva para el ganador, negativa para el perdedor y
        cero en caso de empate o mientras la partida continua.
        """

        if self.done:
            raise ValueError(
                "The game is already finished."
            )

        if action not in range(9):
            raise ValueError(
                "Action must be an integer between 0 and 8."
            )

        if self.board[action] is not None:
            raise ValueError(
                "The selected cell is already occupied."
            )

        # Current player
        player = self.current_player

        # Player's marker
        marker = self.player_markers[player]

        # Place marker
        self.board[action] = marker


        # ====================================================
        # CHECK WINNER
        # ====================================================

        if self._check_winner(marker):

            self.done = True
            self.winner = player

            reward = {
                0: 1 if player == 0 else -1,
                1: 1 if player == 1 else -1
            }

            return (
                self.state,
                reward,
                self.done,
                {
                    "winner": self.winner
                }
            )


        # ====================================================
        # CHECK DRAW
        # ====================================================

        if not self.valid_actions():

            self.done = True
            self.winner = None

            return (
                self.state,
                {
                    0: 0,
                    1: 0
                },
                self.done,
                {
                    "winner": None
                }
            )


        # ====================================================
        # NEXT PLAYER
        # ====================================================

        #add event to the player that made the move
        self.players.get(player).event(f"status% {player}, {self.state}, None, {self.done}, {self.winner}")

        self.current_player = 1 - player

        return (
            self.state,
            {
                0: 0,
                1: 0
            },
            self.done,
            {}
        )


    def _check_winner(self, marker):
        """Comprueba si el marcador indicado ocupa una combinacion ganadora."""

        winning_combinations = [

            # Rows
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),

            # Columns
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),

            # Diagonals
            (0, 4, 8),
            (2, 4, 6)
        ]

        for a, b, c in winning_combinations:

            if (
                self.board[a] == marker
                and
                self.board[b] == marker
                and
                self.board[c] == marker
            ):
                return True

        return False