# Proyecto: Tic-Tac-Toe Engine
# Autor: Santiago Marino
# Email: santiago.mmarino@gmail.com
# Año de desarrollo: 2026
# Descripción: Implementación de un jugador humano para la partida en terminal.

"""Jugador humano para interactuar con la partida desde la consola."""

from tictactoe_engine import PlayerAgent



class Player(PlayerAgent):
    def __init__(self, playerID, name="Player"):
        """Inicializa un jugador humano con su identificador y nombre visible."""
        self.playerID = playerID
        self.player_name = name
        

    def act(self, state):
        """Solicita al usuario una casilla valida y devuelve su indice interno."""
        self.state = state

        while True:
            try:
                selected_cell = int(
                    input(
                        f"{self.player_name} ({self.marker}) elija una casilla "
                        "entre 1 y 9:> "
                    )
                )
            except ValueError:
                print("Entrada invalida: escribe un numero del 1 al 9.")
                continue

            action = selected_cell - 1
            if action in range(9) and state[action] is None:
                return action

            print("Casilla no valida u ocupada. Elige otra.")


    def event(self, message):
        """Muestra al usuario los cambios de estado y el resultado de la partida."""
        if isinstance(message, tuple) and message[0] == "end":
            print(f"{self.player_name} recibe el resultado: {message[1]}")
            return

        m = message.split("%")
        if m[0] == "end":
            print(f"{self.player_name} recibe el estado: {m[1]}\n\n\n\n")
        

