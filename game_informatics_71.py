import pygame
import os
import math

WIDTH = 1500
HEIGHT = 1200
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Medical Game")
clock = pygame.time.Clock()

# Загрузка изображения
game_folder = os.path.dirname(__file__)
player_img = pygame.image.load(os.path.join(game_folder, 'car_12689302.png')).convert_alpha()
background_ = pygame.image.load(os.path.join(game_folder, '33210.jpg')).convert()
background = pygame.transform.scale(background_, (1500, 1200))
background_rect = background.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.orig_image = pygame.transform.scale(player_img,( 150, 130))
        self.image = self.orig_image
        self.rect = self.image.get_rect()
        # Используем float для координат, чтобы движение было плавным
        self.pos = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
        self.rect.center = self.pos

        self.angle = 0  # Текущий угол поворота
        self.speed = 0  # Текущая скорость
        self.rot_speed = 5  # Скорость поворота колес

    def update(self):
        keystate = pygame.key.get_pressed()

        # 1. Управление скоростью
        if keystate[pygame.K_UP]:
            self.speed = 12
        elif keystate[pygame.K_DOWN]:
            self.speed = -8
        else:
            self.speed = 0  # Машина встает, если не жать газ (можно заменить на инерцию)

        # 2. Управление поворотом (только в движении)
        if self.speed != 0:
            if keystate[pygame.K_LEFT]:
                self.angle += self.rot_speed
            if keystate[pygame.K_RIGHT]:
                self.angle -= self.rot_speed

        # 3. Расчет движения (Тригонометрия)
        rad = math.radians(self.angle)
        self.pos.x += self.speed * math.cos(rad)
        self.pos.y -= self.speed * math.sin(rad)

        # 4. Поворот спрайта
        self.image = pygame.transform.rotate(self.orig_image, self.angle + 270)
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))

        # 5. Границы экрана (телепортация)
        if self.pos.x > WIDTH: self.pos.x = 0
        if self.pos.x < 0: self.pos.x = WIDTH
        if self.pos.y > HEIGHT: self.pos.y = 0
        if self.pos.y < 0: self.pos.y = HEIGHT


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление (вызываем один раз для группы)
    all_sprites.update()

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
