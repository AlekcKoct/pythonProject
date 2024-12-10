
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
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# класс истребителя
#Изменяем фон чтобы спрайт истребителя воспринимался эффектнее
class Jet(pygame.sprite.Sprite):
    def __init__(self):
        super(Jet, self).__init__()
        self.surf = pygame.image.load("image/plane.png").convert()
        self.surf = pygame.transform.scale(self.surf, (75, 30))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.x = 15
        self.rect.y = 250

    # Перемещение истребителя при нажатии определенной кнопки
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(7, 0)

        # Чтобы держать истребителя в зоне окна
        if self.rect.left < 0:
            self.rect.left = 0
       
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
               random.randint(0, SCREEN_WIDTH),
               random.randint(SCREEN_HEIGHT + 20, SCREEN_HEIGHT + 150),
            )
        )
        self.speed = random.randint(8, 25)

    # Удаление ракет при пересечении левого края окна
    def update(self):
        self.rect.y -= 15
        #self.rect.move_ip((-self.speed, 0))
        if self.rect.bottom < 0:
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

    #Удаление облака при пересечении левого края окна
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
           self.kill()

# Инициализация микшера звука
pygame.mixer.init()

# Инициализация библиотеки pygame
pygame.init()
clock = pygame.time.Clock()

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
collision_sound.set_volume(0.3)
life_img = pygame.image.load("image/heart.png")
life_img = pygame.transform.scale(life_img, (20,20))
# количество жизней
run_1 = 5
def show_hearth():
    global run_1
    show = 0
    x = 5
    while show != run_1:
        screen.blit(life_img, (x, 5))
        x += 20
        show += 1
# Основной игровой цикл
while run_1 >= 1:
    # Создание экрана как обьекта
    # Размеры определяются постоянными параметрами SCREEN_WIDTH и SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('  My Game')
    img = pygame.image.load("image/plane.png")
    pygame.display.set_icon(img)

    # Создание событий и добавления новых ракет и облаков
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 200)
    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 1000)

    # Создание истребителя
    jet = Jet()

    # Создание групп всех спрайтов ракет и облака
    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(jet)

    running = True
    # Переменная для работы основного цикла
    #running = True
    # Игровой цикл
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
                run_1 = 0
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

        # обработка нажатие клавиш и обновления
        pressed_keys = pygame.key.get_pressed()
        jet.update(pressed_keys)

        # Проверка на достижение правого края окна
        if jet.rect.right > SCREEN_WIDTH:
            time.sleep(2)
            run_1 += 2
            running = False  # Устанавливаем флаг для выхода из цикла

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
            # установить звук столкновения
            collision_sound.play()
            time.sleep(2)  # задержка на 2 сек чтобы было слышно столкновения
            jet.kill()  # истребитель сбит

            # стоп цикла
            running = False
        show_hearth()
        # Перенести все в окно
        pygame.display.flip()

        # частота 30 кадров в секунду
        clock.tick(40)

    run_1 -= 1

# Остановить все звуки и выйти из микшера
pygame.mixer.music.stop()
pygame.mixer.quit()
