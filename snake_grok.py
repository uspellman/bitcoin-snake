import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Snake properties
snake = [(GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)]
snake_direction = (GRID_SIZE, 0)
snake_grow = False

# Food
food = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

# Score
score = 0

# Game speed
speed = 10

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

def draw_food():
    pygame.draw.rect(screen, RED, (food[0], food[1], GRID_SIZE, GRID_SIZE))

def game_over():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Game Over! Score: {score}", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

def main():
    global snake, snake_direction, snake_grow, food, score, speed

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != (0, GRID_SIZE):
                    snake_direction = (0, -GRID_SIZE)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -GRID_SIZE):
                    snake_direction = (0, GRID_SIZE)
                elif event.key == pygame.K_LEFT and snake_direction != (GRID_SIZE, 0):
                    snake_direction = (-GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-GRID_SIZE, 0):
                    snake_direction = (GRID_SIZE, 0)

        new_head = ((snake[0][0] + snake_direction[0]) % WIDTH, (snake[0][1] + snake_direction[1]) % HEIGHT)
        snake.insert(0, new_head)

        if snake[0] == food:
            food = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            snake_grow = True
            score += 1
            # Increase speed every 5 points
            if score % 5 == 0:
                speed = min(speed + 1, 20)  # Cap speed at 20
        else:
            if not snake_grow:
                snake.pop()
            snake_grow = False

        # Check for collision with self
        if len(snake) != len(set(snake)):  # If there are duplicate coordinates
            game_over()
            return

        # Drawing
        screen.fill(BLACK)
        draw_grid()
        draw_snake()
        draw_food()

        # Display score
        font = pygame.font.Font(None, 24)
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(speed)

if __name__ == "__main__":
    main()