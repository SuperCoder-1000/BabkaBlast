import pygame
import random
import asyncio

class Babka(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/babka.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1.0
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom > 600:
            self.reset_position()
            self.speed += 0.25
    
    def reset_position(self):
        self.rect.x = random.randint(0, 600 - self.rect.width)
        self.rect.y = 0

async def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((600,600))
    pygame.display.set_caption("Babka Blast")
    Clock = pygame.time.Clock()

    # Game variables
    score = 0
    game_over = False
    time_remaining = 60.0
    start_time = pygame.time.get_ticks() / 1000
    FPS = 60

    # Initialize sprite
    babka = Babka(300, 300)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(babka)

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if babka.rect.collidepoint(event.pos):
                    score += 1
                    babka.speed += 0.25
                    babka.reset_position()
            elif event.type == pygame.FINGERDOWN and not game_over:
                if babka.rect.collidepoint(event.pos):
                    score += 1
                    babka.speed += 0.25
                    babka.reset_position()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    score = 0
                    game_over = False
                    time_remaining = 60.0
                    start_time = pygame.time.get_ticks() / 1000
                    babka.speed = 1.0
                    babka.reset_position()
        
        if not game_over:
            current_time = pygame.time.get_ticks() / 1000
            time_remaining = max(0, 60.0 - (current_time - start_time))
            if time_remaining <= 0:
                time_remaining = 0
                game_over = True
            all_sprites.update()
        
        # Draw
        screen.fill((125,249,255))
        all_sprites.draw(screen)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        time_text = font.render(f'Time: {int(time_remaining)}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (10, 50))
        
        
        if game_over:
            screen.fill((125,249,255))
            font_large = pygame.font.Font(None, 74)
            game_over_text = font_large.render('Game Over!', True, (255, 0, 0))
            final_score = font_large.render(f'Final Score: {score}', True, (0, 0, 0))
            screen.blit(game_over_text, (200, 250))
            screen.blit(final_score, (180, 350))
        
        pygame.display.flip()
        Clock.tick(FPS)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())