import os
import pygame
import random
from flask import Flask, render_template

# Initialize Flask app
app = Flask(__name__)

# Initialize pygame
pygame.init()

# Game window size
WIDTH, HEIGHT = 600, 400
win = pygame.Surface((WIDTH, HEIGHT))  # Create a surface instead of a window

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Snake settings
snake_size = 20
snake_speed = 10

# Load images (Ensure images are stored in 'static' folder)
snake_img = pygame.image.load("static/snake.png")
snake_img = pygame.transform.scale(snake_img, (20, 20))
obstacle_img = pygame.image.load("static/obstacle.png")
obstacle_img = pygame.transform.scale(obstacle_img, (20, 20))

# Load sounds
pygame.mixer.init()
eat_sound = pygame.mixer.Sound("static/eat.wav")
gameover_sound = pygame.mixer.Sound("static/gameover.wav")

# Font
font = pygame.font.SysFont("comicsansms", 20)

# Game logic function
def game_loop():
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = 0, 0
    snake_body = []
    length = 1
    food_x = random.randrange(0, WIDTH - snake_size, 20)
    food_y = random.randrange(0, HEIGHT - snake_size, 20)
    clock = pygame.time.Clock()
    
    running = True
    while running:
        win.fill(BLACK)
        pygame.draw.rect(win, GREEN, [food_x, food_y, snake_size, snake_size])
        snake_head = [x, y]
        snake_body.append(snake_head)

        if len(snake_body) > length:
            del snake_body[0]

        for part in snake_body[:-1]:
            if part == snake_head:
                running = False  # Snake collides with itself

        for part in snake_body:
            win.blit(snake_img, (part[0], part[1]))

        x += dx
        y += dy

        if x == food_x and y == food_y:
            food_x = random.randrange(0, WIDTH - snake_size, 20)
            food_y = random.randrange(0, HEIGHT - snake_size, 20)
            length += 1
            pygame.mixer.Sound.play(eat_sound)

        pygame.display.update()
        clock.tick(snake_speed)
    
    pygame.quit()

@app.route("/")
def index():
    return "Snake Game is Running!"

@app.route("/play")
def play():
    game_loop()
    return "Game Over!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
