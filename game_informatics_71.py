import pygame
import os
import math

WIDTH = 1500
HEIGHT = 1200
FPS = 30

RED = (255, 0, 0)
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
car_img = pygame.image.load(os.path.join(game_folder, 'vehicle_11669271.png')).convert_alpha()
background_ = pygame.image.load(os.path.join(game_folder, '33210.jpg')).convert()
background = pygame.transform.scale(background_, (WIDTH, HEIGHT))
background_rect = background.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.orig_image = pygame.transform.scale(player_img, (150, 130))
        self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(700, 1000)
        self.rect.center = self.pos
        self.angle = 0
        self.speed = 0
        self.rot_speed = 5

    def update(self):
        self.old_pos = pygame.Vector2(self.pos.x, self.pos.y)
        self.old_angle = self.angle

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.speed = 12
        elif keystate[pygame.K_DOWN]:
            self.speed = -8
        else:
            self.speed = 0

        if self.speed != 0:
            if keystate[pygame.K_LEFT]:
                self.angle += self.rot_speed
            if keystate[pygame.K_RIGHT]:
                self.angle -= self.rot_speed

        rad = math.radians(self.angle)
        self.pos.x += self.speed * math.cos(rad)
        self.pos.y -= self.speed * math.sin(rad)

        self.image = pygame.transform.rotate(self.orig_image, self.angle + 270)
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

        # Границы экрана
        if self.pos.x > WIDTH: self.pos.x = WIDTH
        if self.pos.x < 0: self.pos.x = 0
        if self.pos.y > HEIGHT: self.pos.y = HEIGHT
        if self.pos.y < 0: self.pos.y = 0


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.transform.scale(car_img, (150, 150))
        self.image = pygame.transform.rotate(img, 90)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        #self.image.fill((255, 0, 0, 100)) # Раскомментировать в случае ЧП
        self.rect = self.image.get_rect(center=(x, y))

class FinishZone(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        # Полупрозрачный зеленый цвет, чтобы игрок видел, куда ехать
        self.image.fill((0, 255, 0, 100))
        self.rect = self.image.get_rect(center=(x, y))

# Инициализация объектов
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

finish_group = pygame.sprite.Group()


finish_line = FinishZone(852.5, 310, 210, 390)
all_sprites.add(finish_line)
finish_group.add(finish_line)

player = Player()
all_sprites.add(player)

# Расстановка мобов
mob_positions = [
    (545, 170),
    (995, 170),
    (335, 730),
    (995, 730)
]
for pos in mob_positions:
    m = Mob(pos[0], pos[1])
    all_sprites.add(m)
    mobs.add(m)

#ограничение для клумбы в центре (координаты X, Y, ширина, высота)
flower_bed = Obstacle(748, 610, 890, 210)
all_sprites.add(flower_bed)
obstacles.add(flower_bed)

st = 0
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # Проверка столкновений 
    car_hits = pygame.sprite.spritecollide(player, mobs, False)
    flower_hits = pygame.sprite.spritecollide(player, obstacles, False)

    if car_hits or flower_hits:
        if car_hits:
            st += 1
            print(f"Столкновение с машиной! Всего: {st}")

        # Возвращаем на позицию до столкновения
        player.pos = pygame.Vector2(player.old_pos.x, player.old_pos.y)
        player.angle = player.old_angle
        player.speed = 0
        player.rect.center = player.pos

    won = pygame.sprite.spritecollide(player, finish_group, False)
    if won:
        print("УРОВЕНЬ ПРОЙДЕН!")
        running = False

        # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
