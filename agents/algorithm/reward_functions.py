# Proyecto: Tic-Tac-Toe Engine
# Autor: Santiago Marino
# Email: santiago.mmarino@gmail.com
# Año de desarrollo: 2026
# Descripción: Funciones de propagación de recompensas para asignar crédito a jugadas previas.

"""Estrategias de propagación de recompensas para el entrenamiento de agentes."""

import numpy as np


def algorithm_critical_move_propagation(
    value,
    targets,
    target_rate=0.9,
    penalty='soft',
    started_first=True,
):
    """Asigna crédito dando prioridad a las acciones estratégicamente críticas."""
    if not targets:
        return

    if value == 0:
        draw_target = 0.0 if started_first else 0.25
        targets[:] = [draw_target] * len(targets)
        print(f"Empate en la partida {len(targets)}:{targets}")
        return

    sign = 1 if value > 0 else -1

    if sign > 0:
        targets[-1] = sign * target_rate
        if len(targets) >= 2:
            targets[-2] = sign
        start = len(targets) - 3
        exponent = 2 if penalty == 'soft' else 4
    else:
        targets[-1] = sign * target_rate ** 2
        if len(targets) >= 2:
            targets[-2] = sign * target_rate
        if len(targets) >= 3:
            targets[-3] = sign
        start = len(targets) - 4
        exponent = 3 if penalty == 'soft' else 5

    for index in range(start, -1, -1):
        next_target = targets[index + 1]
        targets[index] = sign * np.power(
            abs(next_target) * target_rate,
            exponent,
        )

    result = "Ganaste" if sign > 0 else "Perdiste"
    print(f"{result} la partida {len(targets)}:{targets}")


def algorithm_simple_inverse_propagation(value, targets, target_rate=0.9, penalty='soft'):
    """Propaga hacia atrás el resultado de una partida sobre sus jugadas.

    Los valores intermedios se reducen con target_rate y una penalización
    distinta para victorias y derrotas, para entrenar al modelo con el contexto
    completo de la secuencia.
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

