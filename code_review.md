# Code Review: bitcoin_snake.py & game_config.py

---

## Bugs

### 1. Infinite loop in `place_food()` when the board is full
**File:** `bitcoin_snake.py`, line 49
**Description:** The `while True:` loop in `place_food()` has no exit condition other than finding a free cell. If every grid position is occupied by the snake (all 1,200 cells on an 800x600 / 20px grid), the loop runs forever and hangs the game process permanently. The git log references a prior fix for this, but no guard exists in the current code.
**Severity:** High

---

### 2. Unbounded game speed at high levels
**File:** `bitcoin_snake.py`, line 254
**Description:** `clock.tick(BASE_SPEED + (level - 1) * SPEED_PER_LEVEL)` has no upper cap. With `BASE_SPEED = 10` and `SPEED_PER_LEVEL = 2`, the game runs at 20 FPS by level 6, 50 FPS by level 21, and over 100 FPS by level 50. Beyond a moderate level the snake moves faster than human reaction time allows. Neither `bitcoin_snake.py` nor `game_config.py` defines a `MAX_SPEED` constant.
**Severity:** High

---

### 3. `save_leaderboard()` has no exception handling
**File:** `bitcoin_snake.py`, lines 104-107
**Description:** `save_leaderboard()` calls `open()` and `json.dump()` with no `try/except` block. If the write fails for any reason (disk full, permissions denied, path missing), an unhandled exception crashes the game mid-session. By contrast, the paired `load_leaderboard()` at line 101 does wrap its I/O in `try/except (FileNotFoundError, ValueError)`. The save function has no equivalent protection.
**Severity:** Medium

---

### 4. `get_initials()` event loop runs at 100% CPU
**File:** `bitcoin_snake.py`, lines 121-146
**Description:** The `while True:` input loop inside `get_initials()` contains no `clock.tick()` or `pygame.time.delay()` call. It spins at maximum speed while waiting for a keypress, pinning one CPU core at 100% for the entire duration of the initials entry screen.
**Severity:** Medium

---

### 5. No way to cancel or skip the initials prompt
**File:** `bitcoin_snake.py`, lines 115-146
**Description:** `get_initials()` requires the player to type at least one alphabetic character and press ENTER before the function returns. There is no Escape key or any other path to skip the prompt. A player who qualifies for the leaderboard but does not want to enter initials is stuck in the input screen with no exit other than closing the window via the QUIT event (which calls `sys.exit()`).
**Severity:** Medium

---

### 6. Start screen renders on an uncleared display surface
**File:** `bitcoin_snake.py`, line 150
**Description:** `display_message("Hit SPACEBAR to begin", WHITE)` is called immediately after display setup, before any `screen.fill()`. Text is drawn onto an uninitialized surface. pygame typically initializes surfaces to black, so this usually looks correct, but the behavior is not guaranteed. On some systems or pygame versions this could show garbage pixels behind the text.
**Severity:** Low

---

### 7. Leaderboard silently excludes tied scores
**File:** `bitcoin_snake.py`, line 113
**Description:** `qualifies_for_leaderboard()` uses a strict greater-than comparison (`score > leaderboard[-1]['score']`). A score that exactly ties the 5th-place entry does not qualify. The player receives no feedback and is silently excluded from the leaderboard, which is likely unintentional.
**Severity:** Low

---

## Code Quality

### 1. `display_message()` shadows the module-level `font` variable
**Lines 41 and 85** -- A module-level `font` is defined at line 41 and used at line 248 to render the HUD score text. Inside `display_message()`, a local variable also named `font` is created at line 85. They are separate objects in different scopes. The code works today, but the name collision is misleading -- editing one while thinking it affects the other would introduce a silent bug.

### 2. `display_message()` creates a new Font object on every call
**Line 85** -- `pygame.font.Font(None, size)` is called each time `display_message()` is invoked. Font construction is relatively expensive in pygame. The game-over screen calls `display_message()` approximately 9 times per death, each time allocating a new font object. The same small set of sizes (22, 26, 28, 32, 44) is always used, so the objects could be created once rather than on every call.

### 3. Entire game runs at module level with no `main()` function
**Lines 149-257** -- The start screen, event loop, game loop, and all game state are top-level module code. Importing this file from any other script launches the game immediately. The Python convention is `if __name__ == '__main__': main()`. Wrapping the game logic in a function would also make the variable scoping explicit.

### 4. Wildcard import from `game_config`
**Line 8** -- `from game_config import *` dumps all constants into the module namespace without a visible source. A reader who sees `BITCOIN_ORANGE`, `BASE_SPEED`, or `POINTS_PER_LEVEL` in `bitcoin_snake.py` cannot tell where those names come from without opening `game_config.py`. This can also silently hide name collisions.

### 5. `move_snake()` has inconsistent `global` declarations
**Lines 61-81** -- `move_snake()` calls `snake.insert()` and `snake.pop()` (in-place list mutation, no `global` needed) but explicitly declares `global food, score, level` for variable reassignment. The function touches four module-level names in total but only declares three of them. This is correct Python, but the inconsistency makes it harder to see at a glance which globals the function modifies.

### 6. `food is not None` guard is misleading
**Line 245** -- The check `if food is not None:` before drawing food implies `food` could be `None` during normal gameplay. In practice it cannot: `place_food()` is called at line 164 before the loop starts and again at line 236 on every restart. `food` is never reset to `None` after initialization. The guard is harmless but creates a false impression about program state.

### 7. `game_config.py` defines speed settings but no speed ceiling
**game_config.py, lines 16-18** -- `BASE_SPEED` and `SPEED_PER_LEVEL` are tunable constants, making them easy to adjust without touching game logic. The natural companion `MAX_SPEED` is absent. Someone changing `SPEED_PER_LEVEL` in the config has no way to also cap the speed from the same file -- they must edit the game loop directly.

---

## Suggested Improvements

### 1. Cap game speed in `game_config.py`
Add `MAX_SPEED = 20` (or another sensible ceiling) to `game_config.py`, then change line 254 in `bitcoin_snake.py` to:
```python
clock.tick(min(BASE_SPEED + (level - 1) * SPEED_PER_LEVEL, MAX_SPEED))
```
This keeps the ceiling tunable from the config file alongside the other speed constants.

### 2. Fix the `place_food()` infinite loop
Replace the `while True:` loop with a list of free cells. If none exist, signal a win condition rather than freezing:
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
        return False  # board is full -- player wins
    food = random.choice(free_cells)
    return True
```

### 3. Add an Escape key to `get_initials()`
Inside the `KEYDOWN` handler, add:
```python
elif event.key == pygame.K_ESCAPE:
    return None
```
Then check the return value before appending to the leaderboard. This gives players a graceful exit from the prompt.

### 4. Add `clock.tick()` to `get_initials()`
Insert `clock.tick(30)` at the bottom of the `while True:` loop inside `get_initials()`. This limits CPU usage during initials entry at no visible cost to responsiveness.

### 5. Add error handling to `save_leaderboard()`
Wrap the file write in a `try/except (OSError, IOError):` block so a failed save does not crash the game:
```python
def save_leaderboard(leaderboard):
    try:
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump(leaderboard, f, indent=2)
    except (OSError, IOError):
        pass  # non-fatal: leaderboard save failed silently
```

### 6. Rename the local `font` variable inside `display_message()` to avoid shadowing
```python
def display_message(message, color=YELLOW, size=48, y_offset=0):
    msg_font = pygame.font.Font(None, size)
    ...
```
This makes the module-level `font` and the local font unambiguous for anyone reading the code.

### 7. Wrap top-level game code in `if __name__ == '__main__':`
```python
def main():
    # place_food(), game loop, start screen, etc.
    ...

if __name__ == '__main__':
    main()
```
This follows Python convention and makes `bitcoin_snake.py` safely importable without launching the game.
