# OpenSpiel Research

## Quick Facts

| Item | Value |
|------|-------|
| **GitHub** | https://github.com/google-deepmind/open_spiel |
| **PyPI** | `pip install open_spiel` (v1.6.15, May 22 2026) |
| **License** | **Apache-2.0** |
| **Stars** | 5.3k |
| **Python** | >= 3.11 (wheels for 3.11, 3.12, 3.13, 3.14) |
| **Platforms** | Linux x86_64/ARM64, Windows x86_64, macOS ARM64 |
| **C++/Python** | Core C++, Python bindings via `pyspiel` |

## Games (~80 supported)

| Category | Examples |
|----------|---------|
| Classic board | Chess, Go, Backgammon, Checkers, Shogi, Xiangqi, Oware, Havannah, Hex, Hive, Connect Four, Tic-Tac-Toe |
| Card games | Poker (Hold'em), Bridge, Leduc/Kuhn poker, Gin Rummy, Hearts, Spades, Euchre, Cribbage, Crazy Eights, Blackjack, Solitaire |
| Imperfect info | Liar's Dice, Phantom Go, Kriegspiel, Battleship, Negotiation |
| Multiplayer | Dou Dizhu (3p), Skat (3p), Chinese Checkers (2-6p), Oh Hell (3-7p) |
| RL sandboxes | Catch, Cliff Walking, Deep Sea, Snake, Laser Tag, Markov Soccer |
| Social dilemmas | Prisoner's Dilemma, Coin Game, Colored Trails |
| Auctions/bidding | First-price Auction, Matching Pennies, Goofspiel, Oshi-Zumo |
| Mean field games | Crowd modelling, Predator-Prey, Routing game |

## AI Engine Usage

OpenSpiel is a **research library** (not a standalone server). Use it as a Python library:

```python
import pyspiel

# List all registered games
games = pyspiel.registered_games()
game = pyspiel.load_game("tic_tac_toe")

# Create a game and run episodes
state = game.new_initial_state()
while not state.is_terminal():
    legal_actions = state.legal_actions()
    action = legal_actions[0]  # pick first legal action
    state.apply_action(action)
```

To run as a server, wrap it yourself (e.g., FastAPI):

```python
from fastapi import FastAPI
import pyspiel

app = FastAPI()

@app.post("/step")
def step(game_name: str, state_str: str, action: int):
    game = pyspiel.load_game(game_name)
    state = game.deserialize_state(state_str)
    state.apply_action(action)
    return {"state": state.serialize(), "legal_actions": state.legal_actions()}
```

## Dockerfile

```dockerfile
FROM python:3.12-slim AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake \
    clang \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir open_spiel

RUN python -c "import pyspiel; print(f'OpenSpiel OK — {len(pyspiel.registered_games())} games registered')"

COPY server.py /app/server.py
WORKDIR /app
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
```
