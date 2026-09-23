# Tic-Tac-Toe Engine

A lightweight Tic-Tac-Toe engine for exploring intelligent agents, reinforcement learning, and reward-propagation strategies in a compact and extensible environment.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white" alt="Python 3.9+" />
  <img src="https://img.shields.io/badge/MLPRegressor-Scikit%20Learn-F7931E?logo=scikit-learn&logoColor=white" alt="Scikit Learn" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License" />
</p>

## Languages

- Español: [README.md](README.md)
- English: [README.en.md](README.en.md)
- Italiano: [README.it.md](README.it.md)

## What this project does

This repository combines:

- a Tic-Tac-Toe game engine;
- a base interface for human and automated players;
- trainable agents based on small neural models;
- reward-allocation strategies for earlier moves;
- a quick way to train and play from the terminal.

## Features

- 3x3 board with a complete game loop.
- Base contract for custom agents.
- Two learning strategies:
  - inverse propagation;
  - critical-move propagation.
- Model persistence via `joblib`.
- Self-play training and terminal gameplay.

## Project structure

```text
.
├── agents/
│   ├── ai/
│   │   ├── critical_move_propagation_agent.py
│   │   └── inverse_propagation_agent.py
│   ├── algorithm/
│   │   └── reward_functions.py
│   └── helpers/
│       ├── actions_extract.py
│       └── encoders.py
├── expert_ai_agent.py
├── run_game.py
├── train.py
├── tictactoe_engine.py
├── requirements.txt
├── Dockerfile
├── README.md
├── README.en.md
├── README.it.md
├── LICENSE
├── AI Player 1_model.pkl
├── AI Player 2_model.pkl
└── .gitignore
```

## Requirements

- Python 3.9+
- `numpy`
- `scikit-learn`
- `joblib`

Install:

```bash
python -m pip install -r requirements.txt
```

## Quick start

### Train the agents

```bash
python train.py 4000
```

This runs self-play games and saves the trained models in the project root.

### Play against the expert agent

```bash
python run_game.py
```

## Docker

```bash
docker build -t tictactoe-ai .
docker run --rm -it tictactoe-ai
```

## Engine API

```python
from tictactoe_engine import TicTacToe

game = TicTacToe(player_0, player_1)
board = game.reset()

while not game.done:
    player = game.players[game.current_player]
    action = player.act(game.state)
    state, reward, done, info = game.step(action)
```

### Core methods

- `reset()`: creates a new empty board.
- `state`: returns the current state.
- `valid_actions()`: returns available empty positions.
- `step(action)`: applies a move and returns `(state, reward, done, info)`.

## Agent contract

```python
from tictactoe_engine import PlayerAgent

class RandomAgent(PlayerAgent):
    def __init__(self, name="Random agent"):
        self.player_name = name
        self.playerID = None
        self.marker = None

    def act(self, state):
        available = [i for i, cell in enumerate(state) if cell is None]
        return available[0]

    def event(self, message):
        pass
```

An agent must implement:

- `act(state)`: returns a valid action.
- `event(message)`: optional callback for game updates and end-of-match messages.

## Learning agents

### Inverse propagation agent

File: `agents/ai/inverse_propagation_agent.py`

This agent assigns credit backward from the final outcome, reducing the value of earlier moves according to the chosen penalty mode.

### Critical-move propagation agent

File: `agents/ai/critical_move_propagation_agent.py`

This agent prioritizes strategically important moves near the end of the game, especially when they determine the final outcome.

## Notes

- The project is designed for experimentation and research.
- It is intentionally lightweight and easy to extend.
- Trained model files are stored in the project root and reused by the expert agent.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE).
