from agents.helpers.actions_extract import get_random_action, get_available_actions


def test_get_random_action():
  state = [1,1,1,1,1,1,1,None,1]
  result = get_random_action(state)
  assert result == 7
