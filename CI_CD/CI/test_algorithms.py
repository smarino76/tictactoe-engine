import numpy as np
from agents.algorithm.reward_functions import algorithm_critical_move_propagation, algorithm_simple_inverse_propagation

def test_algorithm_critical_move_propagation():
  targets_0 = [.6,.23,.3,.55,.14]
  targets_1 = [0,0,0,0]
  
  algorithm_critical_move_propagation(0,targets_0)
  algorithm_critical_move_propagation(1,targets_1)
  
  assert targets_0[3] == 0 and targets_1[2] == 1 and targets_1[3] == np.power((1 * 0.9),2)
