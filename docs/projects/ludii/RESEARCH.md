# Ludii General Game System -- Research Assessment

**Status**: Evaluated, deferred | **Date**: 2026-07-03 | **Lead**: Sandra Schipal

---

## What It Is

Ludii is a **general game system** developed at **Maastricht University** (Department of Advanced Computing Sciences) as part of the ERC-funded **Digital Ludeme Project** (ERC Consolidator Grant #771292, ~2M EUR). It provides a unified framework for playing, evaluating, and designing games across a wide range of categories: board games, card games, dice games, mathematical games, and traditional strategy games from around the world.

Games in Ludii are described as structured sets of **ludemes** -- atomic units of game-related information. This ludemic approach allows the full range of traditional strategy games to be modelled in a single playable database for the first time. The framework supports general game playing (GGP), AI agent evaluation, game design, and computational historical analysis.

**Key publication**: Piette et al., "Ludii -- The Ludemic General Game System", ECAI 2020.
- arXiv: https://arxiv.org/abs/1905.05013
- DOI: 10.3233/FAIA200186

---

## Links

| Resource | URL |
|----------|-----|
| Website | https://ludii.games |
| GitHub org | https://github.com/Ludeme |
| Main repo | https://github.com/Ludeme/Ludii |
| Example AI (Java) | https://github.com/Ludeme/LudiiExampleAI |
| Python AI bridge | https://github.com/Ludeme/LudiiPythonAI |
| AI Competition | https://github.com/Ludeme/LudiiAICompetition |
| Tutorials | https://ludiitutorials.readthedocs.io |
| User Guide (PDF) | https://ludii.games/downloads/LudiiUserGuide.pdf |
| Language Reference (PDF) | https://ludii.games/downloads/LudiiLanguageReference.pdf |
| Digital Ludeme Project | https://ludeme.eu |

---

## License

The core Ludii JAR is **freeware** (not fully FOSS). The JAR can be downloaded and used freely for research and competition purposes, but the source code is not openly available under a standard OSS license.

Auxiliary repositories on the Ludeme GitHub org are **MIT**:
- https://github.com/Ludeme/LudiiExampleAI -- MIT
- https://github.com/Ludeme/LudiiPythonAI -- MIT
- https://github.com/Ludeme/LudiiAICompetition -- MIT

This license asymmetry is the primary licensing blocker: the core game engine cannot be redistributed or modified as open source.

---

## Installation

- **Java**: Requires Java 8+ (JDK for AI development).
- **Download**: https://ludii.games/download.php
- **Current version**: Ludii-1.3.13.jar (~248 MB)
- **Usage**: `java -jar Ludii-1.3.13.jar` launches the graphical desktop application.
- **AI development**: Add the JAR as a library to a Java project; extend `util.AI`; override `selectAction()`. Export to JAR, load via Ludii GUI or programmatically via `AIRegistry.registerAI()`.

---

## Architecture

Ludii is a **monolithic Java desktop application**. The JAR contains:

| Component | Description |
|-----------|-------------|
| Game engine | Loads and runs .lud game descriptions (proprietary .lud format) |
| GUI | Desktop Swing-based UI: game board rendering, move selection, agent assignment |
| Built-in AI agents | Random, UCT, MCTS variants, Alpha-Beta, and others |
| AIRegistry | Plugin system for third-party AI agents loaded from JAR files |
| Game compiler | Parses .lud descriptions into playable game instances |
| Game library | 1000+ games bundled as .lud files |

### Third-Party AI Interface

```java
public class MyAgent extends util.AI {
    public Move selectAction(Game game, Context context,
                             double maxSeconds, int maxIterations, int maxDepth) {
        // Return a Move
    }
    public void initAI(Game game, int playerID) { }
    public boolean supportsGame(Game game) { return true; }
    public void closeAI() { }
}
```

Registration in a custom launcher:

```java
AIRegistry.registerAI("My Agent",
    () -> { return new MyAgent(); },
    (game) -> { return true; });
StartDesktopApp.main(new String[0]);
```

### No Headless CLI Server

Ludii ships as a **GUI-only desktop application**. There is no built-in command-line server mode, no REST API, no HTTP endpoint, no stdio MCP interface. To use it programmatically, you must write a custom Java wrapper that:

1. Creates a `Game` instance from a .lud file
2. Manages game state (Context) manually
3. Exposes move selection via some protocol (HTTP, gRPC, stdio)
4. Handles the full game loop (start, apply moves, query state, get legal moves)

### Python Bridge

The LudiiPythonAI repo provides a bridge via **jpy** (https://github.com/bcdev/jpy):

```
Python AI (UCT)  <--jpy-->  Java wrapper  <--AIRegistry-->  Ludii JAR
```

The jpy bridge is fragile: it requires manual compilation of native .so/.pyd libraries, manual placement of `jpyconfig.properties`, and exact path coordination between the JAR and the Python source files. It is not pip-installable or maintained as a released package. Last commit was September 2021.

---

## Game Library

Ludii ships with **1000+ games** covering the full spectrum of abstract and traditional strategy games:

### Classic Abstract
- Chess, Chess variants (Crazyhouse, Fischer Random, Bughouse, etc.)
- Go (all standard board sizes and rulesets)
- Hex (all standard sizes, various rule variants)
- Backgammon and variants

### Asian Classics
- Shogi (Japanese chess, multiple historic rulesets)
- Xiangqi (Chinese chess)
- Janggi (Korean chess)
- Mancala variants (Oware, Kalah, Bao, etc.)
- Go-Moku / Renju / Gomoku

### Traditional & Regional
- Hnefatafl (Viking chess) variants
- Senet (ancient Egyptian)
- Royal Game of Ur
- Alquerque and衍生 games
- Nine Men's Morris family
- Tablut and other tafl games
- Surakarta

### Modern Abstract
- Amazons
- Breakthrough
- Arimaa
- Abalone
- Twixt
- Havannah

### Western Classics
- Checkers/Draughts (English, International, Turkish, etc.)
- Reversi/Othello
- Dominoes
- Cribbage
- Poker (simplified variants)

### Other
- Dice games, card games, children's games
- Mathematical puzzle games
- Multi-player games (3+ players, teams)
- Simultaneous-move games

Each game is defined in a .lud file using the Ludii game description language. The grammar is well-documented in the Language Reference PDF.

---

## Why We Did Not Integrate Now

### 1. Freeware License (Primary Blocker)
The core JAR is not open source. We cannot:
- Bundle it in our Docker images for redistribution
- Modify engine internals if bugs are found
- Commit it to a fleet repo without licensing risk
- Ship it as part of an NSIS/Tauri installer

The MIT-licensed auxiliary repos are not useful without the proprietary core.

### 2. No Headless CLI / Server Mode
Ludii is a Swing desktop application. There is:
- No `--headless` or `--server` flag
- No stdout gameplay protocol
- No REST or WebSocket API
- No MCP integration path without writing one

To make it useful as a fleet service, we would need to write a Java HTTP server that:
- Loads .lud game files
- Exposes game state via REST
- Accepts move commands
- Returns legal moves, board state, game outcome
- Manages multiple concurrent game instances

### 3. Java Wrapper Required
The fleet is predominantly Python/FastAPI. Integrating Ludii means:
- Writing and maintaining a Java HTTP wrapper (the Ludii JAR cannot be called from Python directly)
- The jpy bridge is too fragile for production use
- A gRPC or REST server in Java must be created from scratch
- No existing open-source HTTP wrapper for Ludii exists

### 4. JAR Size
248 MB JAR is large for a Docker layer. Manageable but not negligible.

---

## Future Integration Path

### Phase 1 -- Java HTTP Server (WIP)
Write a lightweight Java HTTP server that wraps the Ludii JAR:

```java
// Target architecture:
// GET  /games                        -- list available .lud games
// POST /games/{id}/session           -- start new game session
// POST /games/{id}/session/{sid}/move -- submit move
// GET  /games/{id}/session/{sid}     -- get state, legal moves, board
// DELETE ...                         -- cleanup
```

This server would:
- Load a .lud file into a `Game` instance
- Maintain session state (Context) per connection
- For each move request: apply opponent move, run AI, return result
- Support configurable AI type (Random, UCT, MCTS, custom)
- Return board state as JSON (or PBN/FEN-like notation)

### Phase 2 -- Docker Container
Package the Java HTTP server + Ludii JAR + JDK base image into a Docker container:
- Base: `eclipse-temurin:17-jre`
- JAR + wrapper shaded into a single fat JAR
- Expose HTTP port

### Phase 3 -- games-app Integration
Register the Ludii service in the **games-app** fleet repo alongside existing game engines:
- Stockfish (chess, 10780)
- KataGo (Go, 10782)
- YaneuraOu (shogi, 10781)
- Edax (Othello, 10785)
- MoHex (Hex, 10775)
- GNU Backgammon (10786)
- **Ludii** (proposed) -- provides all 1000+ games via a single unified endpoint

### Port Registration (Reserved)

| Port | Service | Notes |
|------|---------|-------|
| **10783** | Ludii HTTP server | REST API for game sessions, move execution, AI agent selection |
| **10784** | (reserved) | Future: WebSocket streaming or management interface |

These ports are adjacent to the existing games-app range (10775-10787), maintaining fleet adjacency conventions.

### Integration with WEBAPP_PORTS.md
Add to the port registry:

```
| 10783 | games-app (ludii) | Ludii General Game System HTTP wrapper (Docker) |
| 10784 | games-app (ludii) | (reserved -- future management interface)        |
```

### Technical Requirements for the Java HTTP Wrapper

| Component | Detail |
|-----------|--------|
| Language | Java 17+ |
| Framework | Javalin or Spring Boot (lightweight) |
| Build tool | Gradle or Maven |
| Shading | ShadowJar or Maven Assembly (fat JAR with Ludii) |
| API format | REST/JSON |
| Game state serialization | Custom JSON schema (no standard exists) |
| AI agent selection | Per-session config: built-in agent + parameters |
| Concurrent sessions | Thread-safe Context management |
| Docker base | eclipse-temurin:17-jre-alpine (~150 MB) |

### Sample API Calls

```
POST /api/v1/session
  {"game": "Hex", "board_size": 11, "ai": "UCT", "ai_time": 1.0}
  → {"session_id": "abc123", "state": "waiting_for_move", "board": {...}}

POST /api/v1/session/abc123/move
  {"move": "E4"}
  → {"move": "E4", "ai_move": "F5", "legal_moves": [...], "game_over": false}

GET /api/v1/session/abc123
  → {"board": {...}, "legal_moves": [...], "turn": 1, "moves": [...], "game_over": false}
```

---

## References

- Piette, E., Soemers, D.J.N.J., Stephenson, M., Sironi, C.F., Winands, M.H.M., Browne, C. (2020). "Ludii -- The Ludemic General Game System". ECAI 2020. https://arxiv.org/abs/1905.05013
- Browne, C. (2018). "Modern Techniques for Ancient Games". IEEE Conference on Computational Intelligence and Games (CIG).
- Soemers, D.J.N.J., et al. (2019). "Learning Policies from Self-Play for General Game Playing". IEEE CIG.
- Digital Ludeme Project: https://ludeme.eu
- Ludii Downloads: https://ludii.games/download.php
