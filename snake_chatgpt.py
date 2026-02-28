import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Load Sounds
pygame.mixer.init()
EAT_SOUND = pygame.mixer.Sound("eat.wav")
GAME_OVER_SOUND = pygame.mixer.Sound("gameover.wav")

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Load High Score
HIGH_SCORE_FILE = "highscore.txt"
def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

class Snake:
    def __init__(self):
        self.body = [[100, 100], [80, 100], [60, 100]]
        self.direction = "RIGHT"

    def move(self):
        head = self.body[0][:]
        if self.direction == "UP":
            head[1] -= CELL_SIZE
        elif self.direction == "DOWN":
            head[1] += CELL_SIZE
        elif self.direction == "LEFT":
            head[0] -= CELL_SIZE
        elif self.direction == "RIGHT":
            head[0] += CELL_SIZE
        self.body.insert(0, head)
        self.body.pop()

class Food:
    def __init__(self):
        self.position = self.generate_food()

    def generate_food(self):
        return [random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
                random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE]

    def draw(self):
        pygame.draw.rect(screen, RED, pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

def check_collision(snake):
    head = snake.body[0]
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        return True
    if head in snake.body[1:]:
        return True
    return False

def display_text(text, x, y, size=30, color=BLACK):
    font = pygame.font.SysFont("Arial", size)
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

def main():
    snake = Snake()
    food = Food()
    running = True
    score = 0
    high_score = load_high_score()
    global FPS
    FPS = 10  # Reset speed to default

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and snake.direction != "DOWN":
            snake.direction = "UP"
        if keys[pygame.K_DOWN] and snake.direction != "UP":
            snake.direction = "DOWN"
        if keys[pygame.K_LEFT] and snake.direction != "RIGHT":
            snake.direction = "LEFT"
        if keys[pygame.K_RIGHT] and snake.direction != "LEFT":
            snake.direction = "RIGHT"

        snake.move()
        if check_collision(snake):
            GAME_OVER_SOUND.play()
            return True  # Return True to indicate game over

        if snake.body[0] == food.position:
            score += 1
            EAT_SOUND.play()
            snake.body.append(snake.body[-1])
            food = Food()
            FPS += 0.5  # Increase speed slightly

        for segment in snake.body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))
        food.draw()

        display_text(f"Score: {score}", 10, 10)
        display_text(f"High Score: {high_score}", 400, 10)
        pygame.display.flip()
        clock.tick(FPS)

    if score > high_score:
        save_high_score(score)
    return False

def show_game_over():
    screen.fill(WHITE)
    display_text("GAME OVER", WIDTH // 2 - 80, HEIGHT // 2 - 50, size=40, color=RED)
    display_text("Press R to Restart, Q to Quit", WIDTH // 2 - 150, HEIGHT // 2, size=25)
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return False

def game_loop():
    while True:
        game_over = main()
        if game_over:
            if not show_game_over():
                break
    pygame.quit()

game_loop()
