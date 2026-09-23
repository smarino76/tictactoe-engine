import numpy as np
from agents.algorithm.reward_functions import algorithm_critical_move_propagation


def test_algorithm_critical_move_propagation():
    targets_draw = [0.6, 0.23, 0.3, 0.55, 0.14]
    targets_win = [0, 0, 0, 0]

    algorithm_critical_move_propagation(0, targets_draw)
    algorithm_critical_move_propagation(1, targets_win)

    assert targets_draw[3] == 0
    assert targets_win[2] == 1
    assert targets_win[3] == np.power(1 * 0.9, 1)
    assert targets_win[1] == np.power(targets_win[2] * 0.9, 2)