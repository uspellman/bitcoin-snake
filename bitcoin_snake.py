import pygame
import random
import time
import sys
import os
import json
from datetime import date
from game_config import *

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bitcoin Snake')

# Clock for controlling game speed
clock = pygame.time.Clock()

# Snake initial position
snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
snake_direction = (BLOCK_SIZE, 0)

# Food
food = None

# Score and level
score = 0
level = 1

# High score — load from file
HIGH_SCORE_FILE = os.path.join(os.path.dirname(__file__), 'highscore.txt')
LEADERBOARD_FILE = os.path.join(os.path.dirname(__file__), 'leaderboard.json')
try:
    with open(HIGH_SCORE_FILE, 'r') as f:
        high_score = int(f.read().strip())
except (FileNotFoundError, ValueError):
    high_score = 0

# Font for Bitcoin logo and messages
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 48)  # Larger font for messages
huge_font = pygame.font.Font(None, 72)  # Even larger font for countdown
bitcoin_logo = font.render('₿', True, WHITE)

def place_food():
    """Place food at a random position that's not occupied by the snake."""
    global food  # Declare food as global here since we modify it
    while True:
        new_food = (random.randrange(0, SCREEN_WIDTH, BLOCK_SIZE), 
                    random.randrange(0, SCREEN_HEIGHT, BLOCK_SIZE))
        if new_food not in snake:
            food = new_food
            return

def draw_snake():
    """Draw the snake on the screen."""
    for segment in snake:
        pygame.draw.rect(screen, WHITE, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

def move_snake():
    """Move the snake in the current direction."""
    new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
    
    # Check if snake has hit the boundaries or itself
    if new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT or new_head in snake[:-1]:
        return False
    
    # Move the snake
    snake.insert(0, new_head)
    
    # Check if snake ate the food
    global food, score, level  # Declare food, score, and level as global here since we modify them
    if new_head == food:
        score += 1
        level = score // POINTS_PER_LEVEL + 1
        place_food()
    else:
        snake.pop()
    
    return True

# Function to display messages with centered text
def display_message(message, color=YELLOW, size=48, y_offset=0):
    font = pygame.font.Font(None, size)
    lines = message.split('\n')
    total_height = sum(font.render(line, True, color).get_height() for line in lines)
    start_y = SCREEN_HEIGHT // 2 - total_height // 2 + y_offset
    
    for line in lines:
        text = font.render(line, True, color)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, start_y))
        start_y += text.get_height()

def load_leaderboard():
    """Load the leaderboard from JSON, returning a list sorted by score (high to low)."""
    try:
        with open(LEADERBOARD_FILE, 'r') as f:
            data = json.load(f)
            return sorted(data, key=lambda e: e['score'], reverse=True)
    except (FileNotFoundError, ValueError):
        return []

def save_leaderboard(leaderboard):
    """Save the leaderboard list to JSON."""
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f, indent=2)

def qualifies_for_leaderboard(score, leaderboard):
    """Return True if the score earns a spot in the top 5."""
    if len(leaderboard) < 5:
        return True
    return score > leaderboard[-1]['score']

def get_initials():
    """Show an input screen and return up to 3 uppercase initials typed by the player."""
    initials = ""
    font_prompt = pygame.font.Font(None, 34)
    font_input = pygame.font.Font(None, 60)

    while True:
        screen.fill(BLACK)

        prompt = font_prompt.render("You made the top 5!  Enter your initials:", True, BITCOIN_ORANGE)
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT // 2 - 80))

        display_str = initials.ljust(3, '_')
        text = font_input.render(display_str, True, GOLD)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 10))

        hint = font_prompt.render("ENTER to confirm  |  BACKSPACE to delete", True, WHITE)
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT // 2 + 70))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and initials:
                    return initials.upper()
                elif event.key == pygame.K_BACKSPACE:
                    initials = initials[:-1]
                elif len(initials) < 3 and event.unicode.isalpha():
                    initials += event.unicode.upper()


# Wait for spacebar to start
display_message("Hit SPACEBAR to begin", WHITE)
pygame.display.flip()
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                waiting = False

# Game loop
running = True
place_food()  # Ensure food is placed before starting the game loop

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction[1] == 0:
                snake_direction = (0, -BLOCK_SIZE)
            elif event.key == pygame.K_DOWN and snake_direction[1] == 0:
                snake_direction = (0, BLOCK_SIZE)
            elif event.key == pygame.K_LEFT and snake_direction[0] == 0:
                snake_direction = (-BLOCK_SIZE, 0)
            elif event.key == pygame.K_RIGHT and snake_direction[0] == 0:
                snake_direction = (BLOCK_SIZE, 0)

    # Move the snake
    if not move_snake():
        # Check and update high score
        new_high_score = score > high_score
        if new_high_score:
            high_score = score
            with open(HIGH_SCORE_FILE, 'w') as f:
                f.write(str(score))

        # Check leaderboard qualification; prompt for initials if earned
        leaderboard = load_leaderboard()
        if score > 0 and qualifies_for_leaderboard(score, leaderboard):
            initials = get_initials()
            leaderboard.append({
                'initials': initials,
                'score': score,
                'level': level,
                'date': date.today().isoformat()
            })
            leaderboard.sort(key=lambda e: e['score'], reverse=True)
            leaderboard = leaderboard[:5]
            save_leaderboard(leaderboard)

        # Draw game over screen
        screen.fill(BLACK)
        display_message("You Lost", YELLOW, 44, -220)
        display_message(f"Score: {score}  |  Best: {high_score}  |  Level: {level}", WHITE, 28, -178)
        if new_high_score:
            display_message("NEW HIGH SCORE!", BITCOIN_ORANGE, 32, -143)
        display_message("-- LEADERBOARD --", BITCOIN_ORANGE, 26, -103)
        if leaderboard:
            for i, entry in enumerate(leaderboard):
                line = f"#{i+1}  {entry['initials']}  {entry['score']}pts  Lvl {entry['level']}  {entry['date']}"
                display_message(line, WHITE, 22, -75 + i * 24)
        else:
            display_message("No entries yet", WHITE, 22, -51)
        display_message(f"Snake length: {len(snake)} blocks", WHITE, 26, 65)
        display_message("R to Restart  |  Q to Quit", WHITE, 28, 100)

        pygame.display.flip()

        # Wait for player to press R or Q
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Reset game state for a new round
                        snake.clear()
                        snake.append((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                        snake_direction = (BLOCK_SIZE, 0)
                        score = 0
                        level = 1
                        place_food()
                        waiting_for_input = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    # Drawing
    screen.fill(BLACK)
    draw_snake()
    if food is not None:  # Check if food is set before drawing
        pygame.draw.rect(screen, GOLD, pygame.Rect(food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
    screen.blit(bitcoin_logo, (10, 10))  # Positioning the Bitcoin logo
    score_text = font.render(f"Score: {score}  Best: {high_score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (40, 10))
    
    pygame.display.flip()
    
    # Control game speed
    clock.tick(BASE_SPEED + (level - 1) * SPEED_PER_LEVEL)

# If we get here, it's because the user closed the window normally
pygame.quit()