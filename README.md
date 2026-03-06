# Bitcoin Snake

> Classic arcade Snake, reimagined for the crypto era. Gold snake. Bitcoin orange. Real stakes — no continues.

---

```
╔══════════════════════════════════════════════════════════╗
║  ₿  Score: 12    Best: 24    Level: 3                   ║
║                                                          ║
║                                                          ║
║              ▓▓▓▓▓▓                                     ║
║                   ▓▓                                     ║
║                   ▓▓                                     ║
║                   ▓▓▓▓▓▓▓▓                              ║
║                         ▓▓                               ║
║                         ▓▓                               ║
║                                                          ║
║                                  ░░                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

Stack sats. Don't crash. Get on the board.

---

## Features

- **Bitcoin theme** — gold snake, Bitcoin orange UI, ₿ logo on-screen at all times
- **Level progression** — speed increases every 5 points, up to a max cap (if you can handle it)
- **Persistent high score** — your best run is saved between sessions
- **Top 5 leaderboard** — earn a spot and enter your initials for arcade immortality
- **Restart without quitting** — press R after a loss and go again immediately
- **Companion trading script** — `btc_top_bottom_indicator.py` fetches live BTC price data and generates buy/sell signals using SMA, EMA, RSI, and MACD

---

## Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/uspellman/bitcoin-snake.git
cd bitcoin-snake

# 2. Install dependencies
pip install pygame

# 3. Run the game
python bitcoin_snake.py
```

> The trading signal script needs additional libraries:
> ```bash
> pip install pandas numpy pandas_ta requests matplotlib
> python btc_top_bottom_indicator.py
> ```

---

## Controls

| Key | Action |
|---|---|
| `SPACEBAR` | Start game |
| Arrow keys | Change direction |
| `R` | Restart after game over |
| `Q` | Quit after game over |

---

## How It Works

- Press SPACEBAR on the title screen to begin
- Guide the gold snake to eat white food blocks — each one grows your snake and adds to your score
- Every 5 points advances you to the next level and increases speed
- Hit a wall or yourself and the run is over
- If your score cracks the top 5, you'll be prompted to enter your initials
- Press R to immediately start a new run, or Q to exit

---

## Project Structure

```
bitcoin-snake/
├── bitcoin_snake.py              # Main game
├── game_config.py                # All constants (colors, speed, screen size)
├── btc_top_bottom_indicator.py   # Bitcoin buy/sell signal script
├── snake_chatgpt.py              # Snake variant — OOP, sound, high score
├── snake_grok.py                 # Snake variant — grid display, wrap-around walls
├── bitcoin_logo.png              # Bitcoin logo asset
├── eat.wav                       # Sound effect
├── gameover.wav                  # Sound effect
├── highscore.txt                 # Persisted high score (plain integer)
├── leaderboard.json              # Top 5 leaderboard entries
├── CHANGELOG.md                  # Version history
└── Practice Folder/              # Learning scripts and exercises
```

---

## Game Settings

| Setting | Value |
|---|---|
| Screen | 800 x 600 px |
| Block size | 20 px |
| Starting speed | 10 FPS |
| Speed increase | +2 FPS per level |
| Max speed | 30 FPS |
| Points per level | 5 |

---

## Contributing

Found a bug or have an idea? Open an issue or submit a pull request.

This project uses an automated code review pipeline. From within Claude Code, run:

```
/review
```

This triggers `review_and_commit.sh`, which performs a structured review pass and commits clean changes. The pipeline is defined in `.claude/commands/review.md`.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for the full version history.

---

## License

MIT — do whatever you want with it. Just don't run it during a bull market; you'll never stop playing.
