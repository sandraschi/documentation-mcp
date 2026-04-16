# Games App - Project Structure

**Source Repo:** `D:\Dev\repos\games-app`  
**Last Updated:** 2025-12-26

---

## Directory Layout

```
games-app/
├── *.html                 # Game HTML files (77 games)
├── *.js                   # Game JavaScript files
├── *.css                  # Stylesheets
├── js/                    # Shared JavaScript libraries
│   ├── core/              # Core game utilities
│   └── engines/           # AI engine wrappers
├── data/                  # Game data (crosswords, puzzles, etc.)
├── games-mcp/             # MCP server for games (FastMCP)
├── stockfish/             # Stockfish chess engine (Windows binary)
├── yaneuraou/             # YaneuraOu shogi engine (Windows binary)
├── katago/                # KataGo go engine (Windows binary)
├── logs/                  # Server logs
├── *.py                   # Python servers (AI engines, multiplayer)
├── *.ps1                  # PowerShell startup scripts
├── *.bat                  # Batch startup scripts
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker image definition
├── requirements.txt       # Python dependencies
└── *.md                   # Documentation files
```

---

## Key Files

### Game Files
- `index.html` - Main game index page
- `chess.html`, `shogi.html`, `go.html`, `xiangqi.html` - Strategy games with AI
- `monopoly.html`, `risk.html`, `catan.html` - Board games
- `solitaire.html`, `minesweeper.html` - Windows classic games
- `japanese-knowledge-tree.html` - Comprehensive cultural encyclopedia (includes manga & anime branches)
- `*-education.html` - Education/help pages for games

### JavaScript Files
- `chess.js`, `shogi.js`, `go.js` - Game logic + AI integration
- `xiangqi.js` - Chinese Chess (recently fixed + AI added)
- `multiplayer-simple.js` - WebSocket multiplayer client
- `stats-manager.js` - Game statistics (IndexedDB)
- `theme-switcher.js` - Dark/light mode theme

### Python Servers
- `stockfish-server.py` - Chess AI server
- `shogi-server.py` - Shogi AI server
- `go-server.py` - Go AI server
- `multiplayer-server.py` - WebSocket multiplayer server
- `web-server.py` - Optional web server

### Configuration
- `docker-compose.yml` - Docker services
- `Dockerfile` - Docker image
- `requirements.txt` - Python dependencies
- `START_ALL_SERVERS.ps1` - Startup script

### Documentation
- `README.md` - Overview
- `TECHNICAL.md` - Technical architecture
- `CHANGELOG.md` - Version history
- `PROGRESS_*.md` - Progress notes
- `DEPLOYMENT_GUIDE.md` - Deployment instructions
- `DOCKER_GUIDE.md` - Docker setup

---

## Architecture

### Frontend (Client-Side)
- **HTML/CSS/JavaScript** - Vanilla JS, no frameworks
- **Canvas API** - For arcade games (Snake, Tetris, Pac-Man)
- **Web Audio API** - For sound effects
- **IndexedDB** - For game statistics persistence
- **WebSocket API** - For multiplayer

### Backend (Server-Side)
- **Python Servers** - AI engines and multiplayer
- **WebSocket Server** - Real-time multiplayer
- **FastAPI** - Optional REST API
- **asyncio** - Async AI engine communication

### AI Integration
- **Stockfish** - Chess engine (UCI protocol)
- **YaneuraOu** - Shogi engine (USI protocol)
- **KataGo** - Go engine (GTP protocol)
- **Custom AI** - Minimax for simpler games

### Data Storage
- **IndexedDB** - Client-side game statistics
- **In-Memory** - Game state (JavaScript objects)
- **WebSocket** - Real-time multiplayer state

---

## Game Categories

### Board Games (21)
- Chess variants (2D, 3D, vs AI, puzzles, famous games)
- Shogi (Japanese Chess)
- Go, Gomoku
- Checkers, Connect Four, Mühle
- Ludo, Mensch ärgere dich nicht!
- Snakes & Ladders
- Monopoly, Risk, Battleship, Clue
- Settlers of Catan, Ticket to Ride, Carcassonne

### Arcade Games (8)
- Snake, Tetris, Breakout, Pong
- Pac-Man, Frogger, Q*bert, Asteroids

### Puzzle & Word Games (8)
- Sudoku, Word Search, Scrabble, Crossword
- Pentomino, Dominoes, Memory, Rubik's Cube

### Windows Classic Games (6)
- Solitaire/Klondike, Minesweeper, FreeCell
- Spider Solitaire, Hearts, Gem Cascade

### Japanese Learning Games (15)
- Yojijukugo (四字熟語), Karuta, Kanji Stroke Order
- Mahjong, Hanafuda, Hiragana/Katakana, Kanji Master
- Japanese Grammar, JLPT Vocabulary, JLPT Practice Test
- Kanji Table, Japanese Flashcards, Japanese Listening
- Manga Guide, Anime Guide

### Card Games (5)
- Texas Hold'em, Contract Bridge
- Old Maid, Schnapsen, Tarock

### Dice Games (3)
- Yahtzee, Craps, Cho-Han Bakuchi

### Party Games (3)
- Tongue Twister, Text Adventures, Pub Quiz

---

## Integration Points

### AI Engines
- **Communication:** UCI/USI/GTP protocols via subprocess
- **Async:** asyncio for non-blocking communication
- **Servers:** Separate Python servers for each engine

### Multiplayer
- **WebSocket:** Real-time bidirectional communication
- **Server:** `multiplayer-server.py` (port 9877)
- **Client:** `multiplayer-simple.js`

### Statistics
- **Storage:** IndexedDB (browser native)
- **Manager:** `stats-manager.js`
- **Tracking:** Unobtrusive game result recording

### Theme System
- **Switcher:** `theme-switcher.js`
- **Storage:** localStorage
- **Default:** Dark mode

---

## Development Workflow

### Adding a New Game
1. Create `game-name.html` with HTML structure
2. Create `game-name.js` with game logic
3. Add link to `index.html`
4. (Optional) Create `game-name-education.html` for help/history

### Adding AI to a Game
1. Implement move generation function
2. Implement move evaluation function
3. Implement `aiTurn()` function
4. Hook into game flow (after player move)

### Testing
- Manual testing in browser
- Check console for errors
- Test on different screen sizes
- Test with/without AI engines

---

## Deployment

### Local Development
```powershell
python -m http.server 8000
```

### Docker
```powershell
docker compose up -d
```

### Production
- Use `DEPLOYMENT_GUIDE.md` for instructions
- Configure reverse proxy (nginx/Traefik)
- Set up SSL certificates
- Configure firewall rules

---

## Dependencies

### Python
- `websockets>=12.0` - WebSocket server
- `aiohttp` - Async HTTP client
- `asyncio` - Async support

### JavaScript
- None (vanilla JS, browser APIs only)

### External Binaries
- Stockfish 16 (Windows)
- YaneuraOu v9.10 (Windows)
- KataGo v1.15.3 (Windows)

---

## File Naming Conventions

- **Games:** `game-name.html`, `game-name.js`
- **Education:** `game-name-education.html`
- **Servers:** `*-server.py`
- **Scripts:** `START_*.ps1`, `*.bat`
- **Docs:** `PROGRESS_YYYY-MM-DD.md`, `*_GUIDE.md`

---

## Code Organization

### Game Logic
- Game state in JavaScript objects
- Event handlers for user interaction
- Rendering functions for display
- AI functions (if applicable)

### Shared Utilities
- `js/core/` - Core game utilities
- `js/engines/` - AI engine wrappers
- `stats-manager.js` - Statistics
- `theme-switcher.js` - Theme management

### Server Code
- One server per AI engine
- WebSocket server for multiplayer
- Async/await pattern throughout
- Error handling and logging

