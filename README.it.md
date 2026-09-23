# Tic-Tac-Toe Engine

Un motore leggero per tris pensato per esplorare agenti intelligenti, apprendimento per rinforzo e strategie di propagazione del reward in un ambiente compatto e facilmente estendibile.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white" alt="Python 3.9+" />
  <img src="https://img.shields.io/badge/MLPRegressor-Scikit%20Learn-F7931E?logo=scikit-learn&logoColor=white" alt="Scikit Learn" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License" />
</p>

## Lingue

- English: [README.md](README.md)
- Español: [README.es.md](README.es.md)
- Italiano: [README.it.md](README.it.md)

## Cosa fa questo progetto?

Questo repository combina:

- un motore del gioco del tris;
- un'interfaccia base per giocatori umani e automatici;
- agenti addestrabili con piccoli modelli neurali;
- strategie di allocazione del reward per mosse precedenti;
- un modo semplice per addestrare e giocare dal terminale.

## Funzionalità

- Tabellone 3x3 con loop di gioco completo.
- Contratto base per agenti personalizzati.
- Due approcci di apprendimento:
  - propagazione inversa;
  - propagazione dei movimenti critici.
- Persistenza dei modelli con `joblib`.
- Addestramento con auto-partite e partita interattiva da terminale.

## Struttura del progetto

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

## Requisiti

- Python 3.9 o superiore
- `numpy`
- `scikit-learn`
- `joblib`

Installazione:

```bash
python -m pip install -r requirements.txt
```

## Avvio rapido

### Addestrare gli agenti

```bash
python train.py 4000
```

Questo esegue partite di auto-gioco e salva i modelli addestrati nella radice del progetto.

### Giocare contro l'agente esperto

```bash
python run_game.py
```

## Docker

```bash
docker build -t tictactoe-ai .
docker run --rm -it tictactoe-ai
```

## API del motore

```python
from tictactoe_engine import TicTacToe

game = TicTacToe(player_0, player_1)
board = game.reset()

while not game.done:
    player = game.players[game.current_player]
    action = player.act(game.state)
    state, reward, done, info = game.step(action)
```

### Metodi principali

- `reset()`: crea una nuova scacchiera vuota.
- `state`: restituisce lo stato corrente.
- `valid_actions()`: restituisce le celle vuote disponibili.
- `step(action)`: applica una mossa e restituisce `(state, reward, done, info)`.

## Contratto dell'agente

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

Un agente deve implementare:

- `act(state)`: restituisce una mossa valida.
- `event(message)`: opzionale per messaggi del motore e fine partita.

## Agenti di apprendimento

### Agente di propagazione inversa

File: `agents/ai/inverse_propagation_agent.py`

Questo agente assegna il credito a ritroso dal risultato finale, riducendo il valore delle mosse precedenti in base alla modalità di penalizzazione.

### Agente di propagazione dei movimenti critici

File: `agents/ai/critical_move_propagation_agent.py`

Questo agente dà più peso ai movimenti decisivi verso la fine della sequenza, soprattutto quando cambiano il corso della partita.

## Note

- Il progetto è pensato per sperimentazione e ricerca.
- È leggero, comprensibile e facilmente estendibile.
- I modelli addestrati vengono salvati nella radice del progetto e riutilizzati dall'agente esperto.

## Licenza

Questo progetto è distribuito sotto la licenza MIT. Consulta [LICENSE](LICENSE).

