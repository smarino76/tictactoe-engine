# Tic-Tac-Toe Engine

Un motor ligero de tres en raya para explorar agentes inteligentes, aprendizaje por refuerzo y estrategias de propagación de recompensas en un entorno compacto y fácilmente extensible.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white" alt="Python 3.9+" />
  <img src="https://img.shields.io/badge/MLPRegressor-Scikit%20Learn-F7931E?logo=scikit-learn&logoColor=white" alt="Scikit Learn" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License" />
</p>

## Idiomas

- English: [README.md](README.md)
- Español: [README.es.md](README.es.md)
- Italiano: [README.it.md](README.it.md)

## ¿Qué hace este proyecto?

Este repositorio combina:

- un motor del juego del tres en raya;
- una interfaz base para jugadores humanos y automáticos;
- agentes entrenables con pequeños modelos neurales;
- estrategias de asignación de recompensas para jugadas anteriores;
- una forma sencilla de entrenar y jugar desde terminal.

## Características

- Tablero 3x3 con flujo completo de juego.
- Contrato base para agentes personalizados.
- Dos enfoques de aprendizaje:
  - propagación inversa;
  - propagación por movimientos críticos.
- Persistencia de modelos con `joblib`.
- Entrenamiento por autojuego y juego interactivo desde consola.

## Estructura del proyecto

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
├── README.es.md
├── README.it.md
├── LICENSE
├── AI Player 1_model.pkl
├── AI Player 2_model.pkl
└── .gitignore
```

## Requisitos

- Python 3.9 o superior
- `numpy`
- `scikit-learn`
- `joblib`

Instalación:

```bash
python -m pip install -r requirements.txt
```

## Inicio rápido

### Entrenar los agentes

```bash
python train.py 4000
```

Esto ejecuta partidas de autojuego y guarda los modelos entrenados en la raíz del proyecto.

### Jugar contra el agente experto

```bash
python run_game.py
```

## Docker

```bash
docker build -t tictactoe-ai .
docker run --rm -it tictactoe-ai
```

## API del motor

```python
from tictactoe_engine import TicTacToe

game = TicTacToe(player_0, player_1)
board = game.reset()

while not game.done:
    player = game.players[game.current_player]
    action = player.act(game.state)
    state, reward, done, info = game.step(action)
```

### Funciones principales

- `reset()`: crea un nuevo tablero vacío.
- `state`: devuelve una copia del estado actual.
- `valid_actions()`: devuelve los índices vacíos disponibles.
- `step(action)`: aplica una jugada y devuelve `(state, reward, done, info)`.

## Contrato de agente

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

Un agente debe implementar:

- `act(state)`: devuelve una acción válida.
- `event(message)`: opcional para mensajes del motor o fin de partida.

## Agentes de aprendizaje

### Propagación inversa

Archivo: `agents/ai/inverse_propagation_agent.py`

Se asigna crédito hacia atrás desde el resultado final del juego y se penaliza el valor de jugadas previas según el tipo de propagación.

### Propagación por movimientos críticos

Archivo: `agents/ai/critical_move_propagation_agent.py`

Da más peso a los movimientos decisivos al final de la secuencia, especialmente cuando cambian el rumbo de la partida.

## Notas

- El proyecto está pensado como entorno de investigación y experimentación.
- Es ligero, comprensible y fácil de extender.
- Los modelos entrenados se guardan en la raíz del proyecto y son reutilizados por el agente experto.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta [LICENSE](LICENSE).
