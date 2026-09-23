# Proyecto: Tic-Tac-Toe Engine
# Autor: Santiago Marino
# Email: santiago.mmarino@gmail.com
# Año de desarrollo: 2026
# Descripción: Utilidades para obtener acciones válidas y evaluar el estado inicial del tablero.

"""Helpers para elegir acciones, validar turnos y detectar el primer movimiento."""

import numpy as np


def get_random_action(state):
    """Elige al azar una de las acciones disponibles del tablero."""
    available_actions = get_available_actions(state)
    return np.random.choice(available_actions)


def get_available_actions(state):
    """Devuelve los índices de las casillas vacías del estado."""
    return [i for i, x in enumerate(state) if x is None]


def is_first_move(state):
    """Indica si el tablero no contiene ningún movimiento."""
    return all(x is None for x in state)