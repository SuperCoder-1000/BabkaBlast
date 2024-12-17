import pygame
import random

# Initialize pygame
pygame.init()

# Define window size
WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Babka Game")

# Game variables
speed = 0.5
score = 0
game_over = False
time_remaining = 60.0

# Load babka image
babka_image = pygame.image.load('images/babka.png')
babka_rect = babka_image.get_rect(center=(WIDTH / 2, HEIGHT / 2))

# Font for text
font = pygame.font.Font(None, 60)


def draw():
    screen.fill((53, 81, 92))
    screen.blit(babka_image, babka_rect)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    time_text = font.render(f"Time: {int(time_remaining)}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (400, 10))
    if game_over:
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (300, 300))
        if score == 1:
            score_text = font.render(f"You got {score} babka!!!", True, (255, 255, 255))
        else:
            score_text = font.render(f"You got {score} babkas!!!", True, (255, 255, 255))
        screen.blit(score_text, (300, 340))


def place_babka():
    global speed
    babka_rect.x = random.randint(0, WIDTH - babka_rect.width)
    babka_rect.y = 0
    speed += 0.1


def time_up():
    global game_over
    game_over = True


def update():
    global speed
    babka_rect.y += speed
    if babka_rect.y > HEIGHT:
        place_babka()


def on_mouse_down(pos):
    global score
    if babka_rect.collidepoint(pos):
        score += 1
        place_babka()


def update_timer():
    global time_remaining, game_over
    time_remaining -= 1
    if time_remaining <= 0:
        game_over = True


# Main game loop
clock = pygame.time.Clock()
place_babka()
pygame.time.set_timer(pygame.USEREVENT, 1000)  # Timer event every second

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            on_mouse_down(event.pos)
        elif event.type == pygame.USEREVENT:
            update_timer()
            if game_over:
                pygame.time.set_timer(pygame.USEREVENT, 0)  # Stop timer

    if not game_over:
        update()
    draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
