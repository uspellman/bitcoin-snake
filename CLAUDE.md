# CLAUDE.md — Project Guide for AI Assistance

## Project Overview

This is a personal Python learning and game development workspace. It contains several independent scripts at different stages of development, built while learning Python. The main focus is a **Bitcoin-themed Snake game**, with additional experiments in trading indicators and LLM-powered conversations.

---

## Project Structure

```
Python/
├── bitcoin_snake.py          # Main game — Bitcoin-themed Snake (PRIMARY file)
├── snake_chatgpt.py          # Snake variant with OOP, sound, high score (ChatGPT-generated)
├── snake_grok.py             # Snake variant with grid, wrap-around movement (Grok-generated)
├── btc_top_bottom_indicator.py  # Bitcoin market top/bottom signal script (pandas, TA)
├── bitcoin_logo.png          # Bitcoin logo asset used in the game
├── eat.wav                   # Sound effect for eating food
├── gameover.wav              # Sound effect for game over
├── highscore.txt             # Persisted high score (plain text integer, currently: 9)
├── test_script.py            # Quick import test (talib)
├── try:.py                   # Quick import test (pygame)
├── uninstall_python.sh       # Shell script to uninstall Python
└── Practice Folder/
    ├── collatz2.py           # Empty/stub
    ├── Automate The Boring Stuff/
    │   ├── collatz.py        # Collatz conjecture step (basic if/else)
    │   ├── charactercount.py
    │   ├── clipboard_test.py
    │   ├── fivetimes.py
    │   ├── hello.py
    │   ├── random_number_game.py
    │   ├── yourName.py
    │   ├── while_example.py
    │   ├── if_*.py           # if/elif/else practice scripts
    │   ├── example.py
    │   └── practice.py
    └── Coursera/
        ├── task_list.py      # Groq LLM client with conversation memory (llama-3.3-70b)
        ├── llm_convo.py      # Conversation loop using task_list helpers
        ├── helper_functions.py
        ├── hello_world.py
        ├── key.env           # API keys (DO NOT COMMIT)
        ├── btc_whitepaper_abstract.txt
        └── Jupytr Notebooks/ # Jupyter notebook experiments
```

---

## What Each Major File Does

### `bitcoin_snake.py` — Main Game
- Built with **pygame**
- Bitcoin/crypto theme: snake is gold, food is white, Bitcoin ₿ logo shown in corner
- Colors: `BITCOIN_ORANGE`, `GOLD`, `WHITE`, `BLACK`, `YELLOW`
- Screen: 800×600, block size 20px, speed 10 FPS
- Game flow: SPACEBAR to start → arrow keys to move → wall/self collision = game over
- On death: "You Lost" message + 5-second blinking countdown → auto-quits via `sys.exit(1)`
- State managed via **globals** (`snake`, `snake_direction`, `food`)
- Key functions: `place_food()`, `draw_snake()`, `move_snake()`, `display_message()`
- No high score system, no restart — game ends completely on death

### `snake_chatgpt.py` — Feature-Rich Snake Variant
- Uses **classes**: `Snake` and `Food`
- Has sound (`eat.wav`, `gameover.wav`), high score persistence (`highscore.txt`)
- Speed increases by 0.5 FPS per food eaten
- Game over screen: press R to restart, Q to quit
- Screen: 600×400, cell size 20px
- Uses `pygame.key.get_pressed()` (continuous key polling) vs. event-based input

### `snake_grok.py` — Minimalist Snake Variant
- Screen: 400×400, grid size 20px
- Draws a visible **grid** on the black background
- **Wrap-around movement** (snake passes through walls using modulo)
- Speed increases every 5 points, capped at 20 FPS
- Collision detection uses `len(snake) != len(set(snake))`
- Self-collision ends game; no restart option, closes after 2-second delay

### `btc_top_bottom_indicator.py` — Bitcoin Trading Signal Script
- Fetches 365 days of BTC/USD data from **CoinGecko API**
- Calculates: 50/200 SMA, 50/200 EMA, RSI(14), MACD(12,26,9) using **pandas_ta**
- Buy signal: price < 200 SMA AND RSI < 30 AND MACD > Signal
- Sell signal: price > 200 SMA AND RSI > 70 AND MACD < Signal
- Backtests with $10,000 starting capital and plots with **matplotlib**

### `Practice Folder/Coursera/task_list.py` — LLM Conversation Client
- Uses **Groq API** with `llama-3.3-70b-versatile` model
- Maintains full conversation history (multi-turn memory)
- System prompt: "You are an IT professional with over 30 years of experience."
- API key loaded from `key.env` via `python-dotenv`
- Exit words: `done`, `exit`, `quit`, `conversation done`

---

## Coding Style & Conventions

### General
- Python 3, no type hints
- Minimal or no docstrings in most files; some functions have short `"""docstrings"""`
- Inline comments used liberally to explain logic (e.g., `# Check if snake ate the food`)
- Constants defined at the top of each file in `ALL_CAPS`
- No external config files — all settings are hardcoded constants

### pygame Games
- `pygame.init()` at top, followed by constant definitions, then `pygame.display.set_mode()`
- Drawing follows a consistent pattern each frame: `screen.fill()` → draw objects → `pygame.display.flip()`
- Game speed controlled via `clock.tick(N)` — changing `N` directly changes speed
- Colors are named tuples defined as module-level constants
- Input handling uses `pygame.KEYDOWN` events (not `get_pressed()`) in `bitcoin_snake.py`

### State Management
- `bitcoin_snake.py` uses **global variables** for game state (not classes)
- `snake_chatgpt.py` uses **classes** (`Snake`, `Food`) — OOP approach
- `snake_grok.py` uses globals declared at top level, re-declared inside `main()` via `global`

### File I/O
- High score stored as a plain integer string in `highscore.txt`
- API keys loaded from `.env` files using `python-dotenv` — never hardcoded

---

## Dependencies

| Library | Used In |
|---|---|
| `pygame` | All snake games |
| `pandas`, `numpy` | btc_top_bottom_indicator.py |
| `pandas_ta` | btc_top_bottom_indicator.py |
| `requests` | btc_top_bottom_indicator.py |
| `matplotlib` | btc_top_bottom_indicator.py |
| `groq` | task_list.py |
| `python-dotenv` | task_list.py |

---

## Rules for AI Assistance

### Before Deleting Anything
- **Always ask before deleting any file, function, or block of code.**
- Even if something looks unused or redundant, confirm with the user first — it may be a reference or work in progress.

### Before Modifying Game Logic
- **Never modify game logic without explaining the change first.**
- State what the current behavior is, what will change, and why, before making the edit.
- This applies to: movement, collision detection, speed, scoring, food placement, game over conditions.

### Communication Style
- I am learning Python. Explain changes in plain English before implementing them.
- Don't assume I know advanced Python concepts — briefly explain anything non-obvious.

### General Rules
- Prefer editing existing files over creating new ones.
- Do not add features, refactoring, or "improvements" that weren't requested.
- Do not add comments to code that wasn't changed.
- Do not introduce new dependencies without asking first.
- Keep `key.env` and any API key files out of any commits — treat them as secrets.
- When modifying `bitcoin_snake.py` specifically, note it uses globals (not classes) — do not refactor to OOP unless explicitly asked.
- The `highscore.txt` file contains live game data — do not overwrite or reset it without asking.

---

## Plugin

This project includes a Claude Code plugin located at `.claude/plugins/bitcoin-snake-dev/`.

### What the plugin does

- **Black auto-formatter hook** — After Claude writes any `.py` file, `black` is automatically run on it to keep formatting consistent. It runs silently and never blocks your workflow if `black` is missing.
- **`/review` slash command** — Type `/review` in a Claude Code conversation to run the `review_and_commit.sh` pipeline. This triggers automated code review and commits from within the chat.

### How to use it

The plugin is active automatically when you open this project in Claude Code — no extra steps needed. The hooks config lives in `.claude/settings.json` and the slash command in `.claude/commands/review.md`.

### Setup for new developers

Install the black formatter before starting:

```bash
pip install black
```
