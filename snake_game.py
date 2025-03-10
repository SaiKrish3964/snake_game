import pygame
import time
import random

# Initialize pygame
pygame.init()

# Game window size
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game 🐍")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Load assets
snake_img = pygame.image.load(r"C:\Users\Lenovo\Desktop\snake.png")  # Load snake image
snake_img = pygame.transform.scale(snake_img, (20, 20))  # Resize to fit
obstacle_img = pygame.image.load(r"C:\Users\Lenovo\Desktop\obstacle.png")  # Load obstacle image
obstacle_img = pygame.transform.scale(obstacle_img, (20, 20))  # Resize to fit

# Background music
pygame.mixer.music.load(r"C:\Users\Lenovo\Desktop\background.mp3")
pygame.mixer.music.play(-1)  # Loop the background music

eat_sound = pygame.mixer.Sound(r"C:\Users\Lenovo\Desktop\eat.wav")  # Eating sound
gameover_sound = pygame.mixer.Sound(r"C:\Users\Lenovo\Desktop\gameover.wav")  # Game over sound

# Snake settings
snake_size = 20
snake_speed = 10

# Font
font = pygame.font.SysFont("comicsansms", 20)

# Function to display score
def show_score(score):
    value = font.render("Score: " + str(score), True, WHITE)
    win.blit(value, [10, 10])

# Game loop function
def game_loop():
    game_over = False
    game_close = False

    # Snake starting position
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = 0, 0

    # Snake body
    snake_body = []
    length = 1

    # Food position
    food_x = round(random.randrange(0, WIDTH - snake_size) / 20) * 20
    food_y = round(random.randrange(0, HEIGHT - snake_size) / 20) * 20

    # Obstacle position
    obstacle_x = round(random.randrange(0, WIDTH - snake_size) / 20) * 20
    obstacle_y = round(random.randrange(0, HEIGHT - snake_size) / 20) * 20

    clock = pygame.time.Clock()

    while not game_over:
        while game_close:
            win.fill(BLACK)
            message = font.render("Game Over! Press R to Restart or Q to Quit", True, RED)
            win.blit(message, [WIDTH // 6, HEIGHT // 3])
            show_score(length - 1)
            pygame.display.update()

            # Game over sound
            pygame.mixer.Sound.play(gameover_sound)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        game_loop()  # Restart game

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -snake_size, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = snake_size, 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -snake_size
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, snake_size

        # Move snake
        x += dx
        y += dy

        # Check boundaries (Game Over)
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            game_close = True

        win.fill(BLACK)

        # Draw food
        pygame.draw.rect(win, GREEN, [food_x, food_y, snake_size, snake_size])

        # Draw obstacle
        win.blit(obstacle_img, (obstacle_x, obstacle_y))

        # Draw snake
        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_body.append(snake_head)

        if len(snake_body) > length:
            del snake_body[0]

        for part in snake_body[:-1]:
            if part == snake_head:
                game_close = True  # If snake collides with itself, game over

        for part in snake_body:
            win.blit(snake_img, (part[0], part[1]))  # Display snake image instead of a square

        show_score(length - 1)
        pygame.display.update()

        # Eating food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - snake_size) / 20) * 20
            food_y = round(random.randrange(0, HEIGHT - snake_size) / 20) * 20
            length += 1
            pygame.mixer.Sound.play(eat_sound)  # Play eating sound

        # Collision with obstacle (Game Over)
        if x == obstacle_x and y == obstacle_y:
            game_close = True

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Start the game
game_loop()
