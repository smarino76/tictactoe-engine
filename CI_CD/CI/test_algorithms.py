
from agents.algorithm.reward_functions import algorithm_critical_move_propagation, algorithm_simple_inverse_propagation

def test_algorithm_critical_move_propagation():
  targets = [.6,.23,.3,.55,.14]
  algorithm_critical_move_propagation(0,targets)
  assert targets[3] == 0
