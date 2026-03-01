import pygame
import random
import time
import sys
import os

# Initialize Pygame
pygame.init()

# Define colors
BITCOIN_ORANGE = (247, 147, 26)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)  # Added yellow for text

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20

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

# Score
score = 0

# High score — load from file
HIGH_SCORE_FILE = os.path.join(os.path.dirname(__file__), 'highscore.txt')
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
        pygame.draw.rect(screen, GOLD, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

def move_snake():
    """Move the snake in the current direction."""
    new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
    
    # Check if snake has hit the boundaries or itself
    if new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT or new_head in snake[:-1]:
        return False
    
    # Move the snake
    snake.insert(0, new_head)
    
    # Check if snake ate the food
    global food, score  # Declare food and score as global here since we might modify them
    if new_head == food:
        score += 1
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
        screen.fill(BLACK)

        # Check and update high score
        new_high_score = score > high_score
        if new_high_score:
            high_score = score
            with open(HIGH_SCORE_FILE, 'w') as f:
                f.write(str(score))

        # Display messages with proper positioning in yellow
        display_message("You Lost", YELLOW, 48, -130)
        display_message(f"Score: {score}  |  Best: {high_score}", WHITE, 36, -75)
        if new_high_score:
            display_message("NEW HIGH SCORE!", BITCOIN_ORANGE, 42, -30)
        display_message(f"Snake length: {len(snake)} blocks", WHITE, 36, 20 if new_high_score else -30)
        display_message("R to Restart  |  Q to Quit", WHITE, 36, 65 if new_high_score else 20)

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
                        place_food()
                        waiting_for_input = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    # Drawing
    screen.fill(BLACK)
    draw_snake()
    if food is not None:  # Check if food is set before drawing
        pygame.draw.rect(screen, WHITE, pygame.Rect(food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
    screen.blit(bitcoin_logo, (10, 10))  # Positioning the Bitcoin logo
    score_text = font.render(f"Score: {score}  Best: {high_score}", True, WHITE)
    screen.blit(score_text, (40, 10))
    
    pygame.display.flip()
    
    # Control game speed
    clock.tick(10)  # Adjust speed by changing this number

# If we get here, it's because the user closed the window normally
pygame.quit()