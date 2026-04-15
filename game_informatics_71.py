import pygame
import os

WIDTH = 800
HEIGHT = 650
FPS = 30

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

game_folder = os.path.dirname(__file__)
player_img = pygame.image.load(os.path.join(game_folder, 'car.png'))
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.orig_image = player_img
        self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        self.speedx = 0
        self.speedy = 0
        self.pv = 0
        pov = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.speedy = -10
            if keystate[pygame.K_LEFT]:
                self.pv = self.pv + 2
                self.speedx = self.speedx - 2
            if keystate[pygame.K_RIGHT]:
                self.pv = self.pv - 2
                self.speedx = self.speedx + 2
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
            if keystate[pygame.K_LEFT]:
                pov = pov - 2
                self.pv = pov
                self.speedx = self.speedx - 2
            if keystate[pygame.K_RIGHT]:
                pov = pov + 2
                self.pv = pov
                self.speedx = self.speedx + 2
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.image = pygame.transform.rotate(self.orig_image, self.pv)
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.rect.right < 0:
            self.rect.right = WIDTH
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Medical Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # закрытие через крестик
        if event.type == pygame.QUIT:
            running = False
    # Обновление
    all_sprites.update()
    player.update()
    screen.blit(player.image, player.rect)
    # Рендеринг
    screen.fill(GREEN)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()