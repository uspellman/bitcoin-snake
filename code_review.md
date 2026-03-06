# Code Review: bitcoin_snake.py & game_config.py

---

## Bugs

### 1. Infinite loop when the board is full
**File:** `bitcoin_snake.py`, lines 49–54
**Severity:** High

`place_food()` uses a `while True` loop that only exits when it finds a grid position not occupied by the snake. If the snake ever fills all 1,200 cells (800×600 grid at BLOCK_SIZE 20), no empty cell will ever be found and the loop runs forever, freezing the game with no way to recover. This is a real crash condition for any player who reaches a very long snake.

---

### 2. Game speed is unbounded at high levels
**File:** `bitcoin_snake.py`, line 254
**Severity:** High

```python
clock.tick(BASE_SPEED + (level - 1) * SPEED_PER_LEVEL)
```

There is no maximum cap on the FPS. With `BASE_SPEED = 10` and `SPEED_PER_LEVEL = 2`, the game hits 20 FPS at level 6, 50 FPS at level 21, and 108 FPS at level 50 (score 245). Beyond a moderate level the game becomes physically impossible to play — the snake moves faster than human reaction time. Nothing in `game_config.py` defines an upper limit.

---

### 3. Start screen renders on an uncleared surface
**File:** `bitcoin_snake.py`, lines 150–151
**Severity:** Low

```python
display_message("Hit SPACEBAR to begin", WHITE)
pygame.display.flip()
```

`display_message()` is called immediately after pygame setup, but `screen.fill()` is never called first. The display surface is uninitialized at this point. pygame typically zeroes the buffer to black, so in practice this is usually invisible, but it is not guaranteed behavior and is a latent visual glitch.

---

### 4. No way to cancel the initials prompt
**File:** `bitcoin_snake.py`, lines 115–146
**Severity:** Medium

`get_initials()` requires the player to type at least one character and press ENTER before returning. There is no Escape key or other path to skip the prompt. If a player qualifies for the leaderboard but does not want to enter initials, they are stuck in the input screen with no exit other than closing the window entirely (which triggers `sys.exit()`).

---

### 5. `qualifies_for_leaderboard()` returns `True` for a score of 0 on an empty board
**File:** `bitcoin_snake.py`, lines 109–113 and 191
**Severity:** Low

`qualifies_for_leaderboard()` returns `True` whenever `len(leaderboard) < 5`, regardless of the score value. A score of 0 would pass this check on an empty leaderboard. The outer `score > 0` guard at line 191 prevents the prompt from appearing, but the function itself produces a misleading result for any caller who doesn't add that extra check.

---

## Code Quality

### 1. Module-level `font` variable is shadowed inside `display_message()`
**File:** `bitcoin_snake.py`, lines 41 and 85

A module-level `font` is defined at line 41 and used at line 248 to render the HUD score text. Inside `display_message()`, a local variable also named `font` is created at line 85. They are separate objects in different scopes. The code works, but the name collision is confusing — editing either one while thinking it affects the other would introduce a silent bug.

---

### 2. `display_message()` creates a new `Font` object on every call
**File:** `bitcoin_snake.py`, line 85

```python
font = pygame.font.Font(None, size)
```

Font construction is relatively expensive in pygame. The game over screen calls `display_message()` approximately 9 times per death, each time allocating a new font object. The same small set of sizes (22, 26, 28, 32, 44) is always used, so the objects could be created once rather than on every call.

---

### 3. `move_snake()` mutates `snake` without a `global` declaration, inconsistently
**File:** `bitcoin_snake.py`, lines 61–81

`move_snake()` calls `snake.insert()` and `snake.pop()` (list mutation — no `global` needed) but explicitly declares `global food, score, level` for simple variable reassignment. The function touches four globals in total but only declares three of them. This is technically correct in Python, but the inconsistency makes it harder to understand which globals the function modifies at a glance.

---

### 4. `food is not None` guard is misleading
**File:** `bitcoin_snake.py`, line 245

```python
if food is not None:
    pygame.draw.rect(...)
```

`place_food()` is called before the game loop starts (line 164) and on every restart (line 236). `food` is never reset to `None` after that. The guard implies `food` could be `None` during normal gameplay, which it cannot. The check is safe, but it creates a false impression about the program's state.

---

### 5. Wildcard import from `game_config`
**File:** `bitcoin_snake.py`, line 8

```python
from game_config import *
```

All constants are dumped into the module's namespace without a visible source. Reading the file alone, there is no indication where `BITCOIN_ORANGE`, `BASE_SPEED`, `POINTS_PER_LEVEL`, etc. come from. This can also hide name collisions silently.

---

### 6. All game logic runs at the top level of the module
**File:** `bitcoin_snake.py`, lines 149–257

The start screen, event loop, game loop, and all game state are top-level module code. This means importing the file from any other script launches the game immediately. The Python convention is `if __name__ == '__main__': main()` — wrapping the game logic in a `main()` function.

---

### 7. `game_config.py` defines speed settings but no speed ceiling
**File:** `game_config.py`, lines 16–18

`BASE_SPEED` and `SPEED_PER_LEVEL` are defined as tunable constants, making them easy to adjust without touching game logic. However, the natural companion constant `MAX_SPEED` is absent. Someone changing `SPEED_PER_LEVEL` in the config has no way to also set a cap from the same file — they would need to edit the game loop directly.

---

## Suggested Improvements

### 1. Add a speed cap to `game_config.py`
Add `MAX_SPEED = 20` to `game_config.py`. Then in `bitcoin_snake.py` at line 254:
```python
clock.tick(min(BASE_SPEED + (level - 1) * SPEED_PER_LEVEL, MAX_SPEED))
```
This keeps speed tunable from one place and prevents the game from becoming unplayable.

---

### 2. Fix the `place_food()` infinite loop
Replace the `while True` loop with a list of free cells. If no free cells exist, the player has won:
```python
def place_food():
    global food
    free_cells = [
        (x, y)
        for x in range(0, SCREEN_WIDTH, BLOCK_SIZE)
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE)
        if (x, y) not in snake
    ]
    if not free_cells:
        return False  # Board is full — player wins
    food = random.choice(free_cells)
    return True
```

---

### 3. Add an Escape key to `get_initials()`
Inside the `KEYDOWN` handler in `get_initials()`:
```python
elif event.key == pygame.K_ESCAPE:
    return None
```
Then check the return value before appending to the leaderboard. This gives the player a graceful exit from the prompt.

---

### 4. Rename local `font` in `display_message()` to avoid shadowing
```python
def display_message(message, color=YELLOW, size=48, y_offset=0):
    msg_font = pygame.font.Font(None, size)
    lines = message.split('\n')
    ...
```
This makes the module-level `font` and the local font unambiguous.

---

### 5. Wrap top-level game code in a `main()` function
```python
def main():
    # place_food(), game loop, start screen, etc.
    ...

if __name__ == '__main__':
    main()
```
This follows Python convention and makes the file safely importable without launching the game.
