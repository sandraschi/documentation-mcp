# Games App - Project Status

**Source Repo:** `D:\Dev\repos\games-app`  
**Type:** Web-based Games Collection  
**Last Updated:** 2025-12-26

---

## Overview

A comprehensive web-based games collection with 75 games, built using HTML, CSS, and JavaScript. Features AI opponents for strategy games (Chess, Shogi, Go, Xiangqi) and multiplayer support via WebSocket. Includes comprehensive Japanese learning suite with integrated manga/anime content in knowledge tree.

---

## Current Status: ✅ **PRODUCTION-READY** (with P2P Cloud Sync)
**Last Updated:** 2026-03-29
**Active Version:** [2.5.0]

### Key Capabilities
- **High-Fidelity Analysis**: Stockfish, Yaneuraou, KataGo.
- **Global Synchronization**: P2P state mirroring via Firebase (europe-west1).
- **Multi-Instance Support**: Concurrent player sessions across instances.
- **SOTA Port Compliance**: Engines bound to 10780-10782 range.

### ✅ Completed Features

**Game Collection (75 games):**
- 21 Board Games (Chess variants, Shogi, Go, Xiangqi, Gomoku, Checkers, Monopoly, Risk, Catan, Ticket to Ride, etc.)
- 8 Arcade Games (Snake, Tetris, Pac-Man, Frogger, Asteroids, etc.)
- 8 Puzzle & Word Games (Sudoku, Word Search, Scrabble, Crossword, etc.)
- 6 Windows Classic Games (Solitaire, Minesweeper, FreeCell, Spider Solitaire, Hearts, Gem Cascade)
- 15 Japanese Learning Games (Yojijukugo, Karuta, Kanji Stroke Order, Mahjong, Hanafuda, Hiragana/Katakana, Kanji Master, Japanese Grammar, JLPT Vocabulary, JLPT Practice Test, Kanji Table, Japanese Flashcards, Japanese Listening, Manga Guide, Anime Guide)
- 5 Card Games (Texas Hold'em, Contract Bridge, Old Maid, Schnapsen, Tarock)
- 3 Dice Games (Yahtzee, Craps, Cho-Han Bakuchi)
- 3 Party Games (Tongue Twister, Text Adventures, Pub Quiz)

**AI Integration:**
- Stockfish 16 (Chess, ~3500 ELO)
- YaneuraOu v9.10 (Shogi)
- KataGo v1.15.3 (Go)
- Minimax algorithms (Gomoku, Checkers, Mühle)
- **NEW (2025-12-02):** Xiangqi AI opponent with move evaluation system

**Multiplayer:**
- WebSocket-based local multiplayer server
- Real-time move synchronization
- Chat support
- Game state management

**Recent Improvements (2025-12-26):**
- **🖼️ 50×50 Kanji Wallpaper Grid:** 2,500 kanji in classical layout with selectable display modes
- **📖 Manga Guide:** ¥600B industry deep-dive with 8 genres, historical timeline, creator profiles
- **🎬 Anime Guide:** ¥2.5T industry analysis with 15 studios, 8 genres, seiyu culture, timeline
- **🛒 Time Sales Database:** Half-price supermarket timing guide (fresh sushi ¥100-200!)
- **📀 Second-Hand Media Economy:** BookOff/Mandarake culture with no "used" stigma
- **📚 Flashcard System:** 600+ AI-generated vocabulary cards with spaced repetition
- **📝 JLPT Practice Tests:** Database-driven questions with explanations and progress tracking
- **🇯🇵 Complete Japanese Learning Suite:** Unified kanji table, flashcards, JLPT testing interface

**Recent Improvements (2025-12-02):**
- **Xiangqi (Chinese Chess):**
  - Fixed critical CSS Grid rendering issues (board collapsing to 1px)
  - Fixed JavaScript syntax errors (duplicate catch blocks, emoji encoding)
  - Implemented AI opponent with move evaluation
  - Added proper error handling and initialization
  - Board now renders correctly as 9×10 grid (90 cells)

---

## Technical Stack

**Frontend:**
- HTML5, CSS3, JavaScript (ES6+)
- Canvas API (for arcade games)
- Web Audio API (for sound effects)
- IndexedDB (for game statistics)

**Backend:**
- Python 3.8+ (for AI engines)
- WebSocket server (for multiplayer)
- FastAPI (optional, for API endpoints)

**AI Engines:**
- Stockfish 16 (Windows binary)
- YaneuraOu v9.10 (Windows binary)
- KataGo v1.15.3 (Windows binary)
- Custom minimax implementations

**Deployment:**
- Docker support (Dockerfile, docker-compose.yml)
- Windows-native (AI engines are Windows binaries)
- Local web server (Python http.server or custom)

---

## Key Features

### Game Features
- ✅ 77 playable games
- ✅ AI opponents for strategy games
- ✅ Local multiplayer via WebSocket
- ✅ Game statistics tracking (IndexedDB)
- ✅ Dark mode theme support
- ✅ Responsive design
- ✅ Education pages for obscure games

### AI Features
- ✅ Multiple AI difficulty levels
- ✅ Move evaluation and scoring
- ✅ Legal move validation
- ✅ Check/checkmate detection
- ✅ Opening books (for Chess)

### Multiplayer Features
- ✅ Real-time synchronization
- ✅ Automatic player matching
- ✅ Chat support
- ✅ Disconnect handling
- ✅ Game state persistence

---

## Recent Fixes (2025-12-02)

### Xiangqi Board Rendering
**Problem:** Board was collapsing to width/height 1px, showing as "red blob" or "loading board..." message.

**Root Causes:**
1. CSS Grid not properly configured (missing explicit grid-template-rows/columns)
2. Cells not explicitly positioned in grid (missing grid-row/grid-column)
3. JavaScript syntax errors preventing script execution
4. Emoji encoding issues in strings

**Solutions:**
1. Added explicit `grid-template-columns: repeat(9, 60px)` and `grid-template-rows: repeat(10, 60px)`
2. Set explicit board dimensions (586px × 644px) with `!important` flags
3. Added `grid-row` and `grid-column` positioning for each cell
4. Fixed all syntax errors (removed duplicate catch, fixed quotes, removed emoji)
5. Added robust error handling and initialization

### Xiangqi AI Implementation
**Features:**
- Move evaluation system with piece values (General=1000, Rook=9, etc.)
- Check detection (+50 points)
- Center control and pawn advancement bonuses
- Top 3 move selection with randomness
- Legal move validation (doesn't leave own general in check)

**AI Functions:**
- `getAllValidMoves(row, col)`: Returns all legal moves
- `evaluateMove(fromRow, fromCol, toRow, toCol)`: Scores move quality
- `aiTurn()`: Main AI function

---

## Known Issues

**None currently blocking**

---

## Dependencies

**Python:**
- `websockets>=12.0` (for multiplayer server)
- `aiohttp` (for async HTTP)
- `asyncio` (for AI engine communication)

**JavaScript:**
- No external dependencies (vanilla JS)
- IndexedDB (browser native)
- WebSocket API (browser native)

**AI Engines:**
- Stockfish 16 (Windows binary, included)
- YaneuraOu v9.10 (Windows binary, included)
- KataGo v1.15.3 (Windows binary, included)

---

## Quick Start

**Option 1: Simple (No Docker)**
```powershell
cd D:\Dev\repos\games-app
python -m http.server 8000
# Open http://localhost:8000
```

**Option 2: Docker**
```powershell
cd D:\Dev\repos\games-app
docker compose up -d
# Open http://localhost:8000
```

**Option 3: With AI Engines**
```powershell
cd D:\Dev\repos\games-app
.\START_ALL_SERVERS.ps1
# Starts web server + AI engines + multiplayer server
```

---

## Documentation

**Main Docs:**
- `README.md` - Overview and quick start
- `TECHNICAL.md` - Technical architecture
- `CHANGELOG.md` - Version history
- `PROGRESS_*.md` - Progress notes by date

**Game-Specific:**
- Education pages for each game (history, rules, strategy)
- Help screens for complex games

**Deployment:**
- `DEPLOYMENT_GUIDE.md` - Deployment instructions
- `DOCKER_GUIDE.md` - Docker setup
- `WEB_SERVER_GUIDE.md` - Web server configuration

---

## Future Enhancements (Optional)

1. **AI Improvements:**
   - Minimax algorithm for Xiangqi (stronger play)
   - Opening books for more games
   - Difficulty levels (easy/medium/hard)

2. **Multiplayer:**
   - Internet play (Firebase or custom server)
   - Game rooms/lobbies
   - Spectator mode

3. **UI/UX:**
   - Move history display
   - Game replay feature
   - Piece animations
   - Sound effects for all games

4. **Mobile Support:**
   - Touch controls for board games
   - Responsive layouts
   - Mobile-optimized UI

---

## Project Health

**Status:** ✅ Healthy  
**Last Major Update:** 2025-12-26 (Manga/Anime guides + Time sales + Kanji wallpaper)  
**Test Coverage:** Manual testing  
**Documentation:** Comprehensive  
**Maintenance:** Active

