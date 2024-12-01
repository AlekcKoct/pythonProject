
# код программы создан при начальной помощи GPT, поисковика Яндекс
# а также справочной литературы по PyGame и Python 3 2е издание
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import random

from pygame.locals import (
    K_DOWN,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_UP,
    KEYDOWN,
    QUIT,
    RLEACCEL,
    )

# Определение высоты и ширины окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# класс истребителя
#Изменяем фон чтобы спрайт истребителя воспринимался эффектнее
class Jet(pygame.sprite.Sprite):
    def __init__(self):
        super(Jet, self).__init__()
        self.surf = pygame.image.load("image/plane.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    # Перемещение истребителя при нажатии определенной кнопки
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Чтобы держать истребителя в зоне окна
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Определяем класс ракет
# Изменяем фон чтобы ракеты воспринимались эффектнее
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("image/missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # Начальная позиция определяется функцией random
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Удаление ракет при пересечении левого края окна
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Класс облаков
# Изменяем фон чтобы облака воспринимались эффектнее
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("image/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # TНачальная позиция генерируется функцией random
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Удаление облака при пересечении левого края окна
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

# Инициализация микшера звука
pygame.mixer.init()

# Инициализация библиотеки pygame
pygame.init()
clock = pygame.time.Clock()

# Создание экрана как обьекта
# Размеры определяются постоянными параметрами SCREEN_WIDTH и SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Создание событий и добавления новых ракет и облаков
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Создание истребителя
jet = Jet()

# Создание групп всех спрайтов ракет и облака
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(jet)

# Загрузка фонового сопровождения
pygame.mixer.music.load("sound/highway.mp3")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.1)

# Загрузка звуковых файлов
move_up_sound = pygame.mixer.Sound("sound/rising.ogg")
move_down_sound = pygame.mixer.Sound("sound/falling.ogg")
collision_sound = pygame.mixer.Sound("sound/vzryiv.ogg")

# Громкость для всех звуков
move_up_sound.set_volume(0.1)
move_down_sound.set_volume(0.1)
collision_sound.set_volume(0.4)

# Переменная для работы основного цикла
running = True

# Основной игровой цикл
while running:
    # Реакция на изменение событий
    for event in pygame.event.get():
        # А было ли нажата какая-нибудь клавиша?
        if event.type == KEYDOWN:
            # Была ли нажата клавиша ESC?, если да, то выход
            if event.key == K_ESCAPE:
                running = False

        # Проверка нажатия закрытия окна в верху окна
        elif event.type == QUIT:
            running = False

        # добавление новых ракет
        elif event.type == ADDENEMY:
            # Добавления и обновление ракет в окно в виде спрайтов
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Добавление новых облаков
        elif event.type == ADDCLOUD:
            # Добавления и обновление облаков в окно в виде спрайтов
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # Обработка нажатие клавиш и обновления
    pressed_keys = pygame.key.get_pressed()
    jet.update(pressed_keys)

    # Обновление позиции ракет и препятствий
    enemies.update()
    clouds.update()

    # Заполнение окна голубым цветом
    screen.fill((135, 206, 250))

    # внесение всех спрайтов в окно
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Обработка столкновения
    if pygame.sprite.spritecollideany(jet, enemies):
        # сбросить все звуки и установить звук столкновения
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()
        #задержка на 1 сек чтобы было слышно столкновение
        time.sleep(1)
        # истребитель сбит
        jet.kill()

        # стоп цикла
        running = False

    # Перенести все в окно
    pygame.display.flip()

    # частота 30 кадров в секунду
    clock.tick(30)

# Остановить все звуки и выйти из микшера
pygame.mixer.music.stop()
pygame.mixer.quit()
