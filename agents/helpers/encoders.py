# Proyecto: Tic-Tac-Toe Engine
# Autor: Santiago Marino
# Email: santiago.mmarino@gmail.com
# Año de desarrollo: 2026
# Descripción: Utilidades para codificar estados y pares estado-acción del tablero.

"""Funciones para transformar estados del tablero en representaciones numéricas."""


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