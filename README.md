# Bitcoin Snake

A Bitcoin-themed Snake game built with Python and pygame, plus a companion Bitcoin trading signal script.

---

## Project Overview

Bitcoin Snake is a classic Snake game with a crypto twist. The snake is styled in gold, the food is white, and the Bitcoin logo is displayed in the corner of the screen. When the snake dies, the game displays a "You Lost" message and exits after a short countdown. There is no restart — each run is a fresh game.

The project also includes `btc_top_bottom_indicator.py`, a standalone script that fetches real Bitcoin price data and generates buy/sell signals using technical indicators.

---

## Features

- Gold-colored snake on a dark background with Bitcoin orange accents
- Bitcoin logo displayed in the corner during gameplay
- Wall collision and self-collision detection end the game
- "You Lost" screen with a 5-second blinking countdown before auto-exit
- Companion BTC trading signal script using SMA, EMA, RSI, and MACD

---

## How to Play

1. Run the game:
   ```bash
   python bitcoin_snake.py
   ```
2. Press **SPACEBAR** to start.
3. Use the **arrow keys** to move the snake.
4. Eat the white food blocks to grow.
5. Avoid hitting the walls or running into yourself — either ends the game.

---

## Dependencies

Install all required libraries before running:

```bash
pip install pygame pandas numpy pandas_ta requests matplotlib
```

| Library | Used In |
|---|---|
| `pygame` | `bitcoin_snake.py` |
| `pandas`, `numpy` | `btc_top_bottom_indicator.py` |
| `pandas_ta` | `btc_top_bottom_indicator.py` |
| `requests` | `btc_top_bottom_indicator.py` |
| `matplotlib` | `btc_top_bottom_indicator.py` |

---

## File Structure

```
Python/
├── bitcoin_snake.py              # Main game — Bitcoin-themed Snake
├── btc_top_bottom_indicator.py   # Bitcoin buy/sell signal script
├── snake_chatgpt.py              # Snake variant with OOP, sound, high score
├── snake_grok.py                 # Snake variant with grid and wrap-around walls
├── bitcoin_logo.png              # Bitcoin logo asset used in the game
├── eat.wav                       # Sound effect for eating food
├── gameover.wav                  # Sound effect for game over
├── highscore.txt                 # Persisted high score (plain text integer)
└── Practice Folder/              # Learning scripts and exercises
```

---

## Game Settings

| Setting | Value |
|---|---|
| Screen size | 800 x 600 px |
| Block size | 20 px |
| Game speed | 10 FPS |
| Snake color | Gold |
| Food color | White |
