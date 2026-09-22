<!--
Proyecto: Tic-Tac-Toe Engine
Autor: Santiago Marino
Email: santiago.mmarino@gmail.com
Año de desarrollo: 2026
-->

# Tic-Tac-Toe Engine

A small, extensible Tic-Tac-Toe environment for playing games between human, random, rule-based, and machine-learning agents. The project is intended both as a simple agent-integration example and as a compact research playground for reinforcement-learning ideas.

## Features

- A nine-cell Tic-Tac-Toe environment with a Gym-like `reset`, `state`, `valid_actions`, and `step` flow.
- A small abstract agent interface that custom players can implement.
- Human and neural-network agents included.
- Self-play comparison between two propagation strategies using `MLPRegressor`.
- Model persistence through `joblib`.
- Strategic reward propagation from the final game result to earlier moves.

## Requirements

- Python 3.9 or newer
- `numpy`
- `scikit-learn`
- `joblib`

Install the runtime dependencies with:

```bash
python -m pip install numpy scikit-learn joblib
```

There is currently no `requirements.txt`; the command above lists the packages used by the project.

## Run A Game

`run_game.py` starts a human-versus-trained-agent game and redraws the board in a fixed terminal position:

```bash
python run_game.py
```

The human player enters a cell from `1` to `9`. Empty cells remain numbered on screen. The board indexes used by the engine and by custom agents are zero-based:

```text
0 | 1 | 2
--+---+--
3 | 4 | 5
--+---+--
6 | 7 | 8
```

Before playing against the expert agent, train its model:

```bash
python train.py 4000
```

The argument is the number of self-play games and defaults to `4000` when omitted. Training writes `AI Player 1_model.pkl` and `AI Player 2_model.pkl` in the current directory. `run_game.py` uses `AI Player 1_model.pkl`.

## Engine API

The main environment is `TicTacToe` in `tictactoe_engine.py`:

```python
from tictactoe_engine import TicTacToe

game = TicTacToe(player_0, player_1)
board = game.reset()

while not game.done:
    player = game.players[game.current_player]
    action = player.act(game.state)
    transition = game.step(action)
```

### `reset()`

`reset()` starts a new game and returns a copy of the empty board:

```python
[None, None, None, None, None, None, None, None, None]
```

It also:

- randomly assigns `X` and `O` to player IDs `0` and `1`;
- assigns the marker to each agent's `marker` attribute;
- randomly chooses the first player;
- clears the winner and terminal state.

### `state`

`game.state` returns a copy of the current nine-cell board. Empty cells are `None`; occupied cells contain either `"X"` or `"O"`.

### `valid_actions()`

Returns the zero-based indexes of empty cells. A valid action is an integer from `0` through `8` that is present in this list.

### `step(action)`

Applies one action for the current player and returns:

```python
(state, reward, done, info)
```

The values are:

- `state`: a copy of the board after the move;
- `reward`: `{0: reward_for_player_0, 1: reward_for_player_1}`;
- `done`: `True` when somebody wins or the board is full;
- `info`: `{"winner": 0}`, `{"winner": 1}`, or `{"winner": None}` when the game ends.

Non-terminal moves return zero rewards and an empty `info` dictionary. Invalid moves raise `ValueError`.

## Connecting A Custom Agent

Agents implement `PlayerAgent` from `tictactoe_engine.py`:

```python
from tictactoe_engine import PlayerAgent


class RandomAgent(PlayerAgent):
    def __init__(self, name="Random agent"):
        self.player_name = name
        self.playerID = None
        self.marker = None

    def act(self, state):
        available = [index for index, cell in enumerate(state) if cell is None]
        return available[0]

    def event(self, message):
        pass
```

Run it against another agent:

```python
from tictactoe_engine import TicTacToe

agent_0 = RandomAgent("Agent 0")
agent_1 = RandomAgent("Agent 1")
game = TicTacToe(agent_0, agent_1)
game.reset()

while not game.done:
    player = game.players[game.current_player]
    action = player.act(game.state)
    if action not in game.valid_actions():
        raise ValueError("The agent returned an invalid action")
    state, rewards, done, info = game.step(action)

print(info["winner"])
```

### Agent contract

`act(state)` must:

- receive a nine-element board list;
- return one zero-based action index from `0` to `8`;
- choose an empty cell;
- avoid modifying the `state` list in place.

The engine sets these attributes on each agent during initialization and reset:

- `playerID`: `0` or `1`;
- `marker`: `"X"` or `"O"`.

`event(message)` is optional for agents that do not need notifications. The engine currently sends a few different message shapes:

- During a non-terminal move, the engine sends the moving agent a string beginning with `status%`.
- The example runner can send strings beginning with `start%`, `move%`, or `canceled%`.
- At the end of a game, the runner sends a tuple:

  ```python
  ("end", (final_state, rewards, done, {"winner": winner_id_or_None}))
  ```

An agent that only needs `act` can implement `event` as `pass`. A learning agent can use the `end` tuple to assign a final reward and train after the complete game.

## How The Included Learning Agents Work

The project includes two online value-learning agents based on `sklearn.neural_network.MLPRegressor`:

- `agents/ai/inverse_propagation_agent.py`: the original strategy, which propagates the final result backward with a penalty exponent.
- `agents/ai/critical_move_propagation_agent.py`: the experimental strategy, which gives greater credit to strategically critical moves near the end of a winning sequence and greater blame to the earlier decisive move in a losing sequence.

The current training script pits the critical-move agent (`AI Player 1`) against the inverse-propagation agent (`AI Player 2`).

### State-action features

For its own marker, the board is encoded as:

```text
empty cell       ->  0
agent's marker   ->  1
opponent marker  -> -1
```

The nine board values are concatenated with a nine-value one-hot action encoding. Each training input therefore has 18 values: nine for the board and nine for the action being evaluated.

### Choosing actions

When no model exists, or when exploration is selected, the agent chooses a random valid action. Otherwise it evaluates every valid action and chooses the action with the largest predicted value.

The `epsilon` parameter controls exploration:

- `epsilon = 1.0`: always random;
- `epsilon = 0.2`: approximately 20% random actions;
- `epsilon = 0.0`: always use the model.

After each game, epsilon decays but never goes below `0.05`.

### End-of-game targets: inverse propagation

During a game, every selected action is stored in `features` and receives a temporary target of `0.0`. The final move is then assigned:

- `1.0` for a win;
- `-1.0` for a loss;
- `0.0` for a draw.

In the inverse-propagation agent, `update_targets` propagates credit backward through earlier moves. The penalty exponent depends on the selected `soft` or `hard` mode. This gives the regressor continuous targets rather than only three categorical labels.

### End-of-game targets: critical-move propagation

The critical-move agent uses a different heuristic:

- win: the penultimate action receives `+1.0`, the final action receives `+0.9`, and earlier actions receive decreasing values;
- loss: the antepenultimate action receives `-1.0`, the penultimate action receives `-0.9`, and the final action receives `-0.81`;
- draw after starting first: every action receives `0.0`;
- draw after starting second: every action receives `+0.25`.

The agent stores only its own actions, so `penultimate` and `antepenultimate` refer to the agent's action history, not all moves made on the board.

### `partial_fit` and replay lists

At the end of a game:

```python
self.replay_features.extend(self.features)
self.replay_targets.extend(self.target)
self.model.partial_fit(
    self.replay_features,
    self.replay_targets,
)
```

`features` and `target` contain the current game's moves and targets. `replay_features` and `replay_targets` are longer-lived in-memory lists that accumulate examples while the same agent object remains alive. `extend` adds each item from the source list individually, preserving the one-input/one-target correspondence. With `--no-replay`, `partial_fit` receives only `features` and `target` from the current game.

The lists are not serialized. When the Python process exits, the replay history is lost. Only the fitted model is saved with `joblib.dump`. The training script keeps both agents alive and reuses them across all requested games, so replay data accumulates during one training run.

## Training Workflow

`train.py` creates two learning agents with model loading disabled and plays the requested number of self-play games:

```bash
python train.py 10000
```

By default, each update replays all examples collected during the current run. To use online training with only the current game in each `partial_fit` call, run:

```bash
python train.py 10000 --no-replay
```

For each game:

1. The board, markers, and starting player are reset.
2. The current agent receives `game.state` through `act`.
3. The returned action is validated and applied with `game.step`.
4. The final transition is sent to both agents through `event(("end", result))`.
5. Each agent propagates targets, calls `partial_fit`, and saves its model.

The training command suppresses per-move output and displays a progress bar. Increase the game count for more experience, but remember that replay mode retains all replay examples in memory for the duration of the run. Model files are overwritten after each completed game.

## Research Notes And Limitations

This is a deliberately small educational environment, not a complete reinforcement-learning framework.

- The included learner uses a supervised regressor with end-of-game target propagation, not a full Q-learning implementation.
- The model predicts values for state-action pairs; it does not directly predict a class or a move.
- Markers and the starting player are randomized on reset, which helps reduce first-player bias.
- The fitted model is persisted, but replay examples are not persisted between processes.
- In replay mode, `partial_fit` is called with the accumulated in-memory examples each time a game ends; `--no-replay` uses only the current game's examples.
- The engine trusts agents to return a valid action; callers should validate actions before calling `step` or handle the `ValueError` raised by the engine.
- The current example stores model files in the working directory. Use an explicit `model_path` when integrating an agent into another application.

Useful files for experiments:

- `tictactoe_engine.py`: environment and agent base class;
- `agents/ai/inverse_propagation_agent.py`: original trainable agent and propagation strategy;
- `agents/ai/critical_move_propagation_agent.py`: critical-move trainable agent and propagation strategy;
- `expert_ai_agent.py`: model-only inference agent;
- `agents/agent_human.py`: console human agent;
- `train.py`: self-play training loop;
- `run_game.py`: human-versus-agent example.

## License

This project is released under the GNU General Public License v3.0. See [LICENSE](LICENSE).