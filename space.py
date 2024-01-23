import sys
import time

import pygame  # Импортируем модуль pygame
import pygame.font
from pygame.sprite import Group, Sprite


class Ino(pygame.sprite.Sprite):  # Класс враг
    def __init__(self, screen):  # Инициализируем врага и задаем начальную позицию
        super(Ino, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('Images/pixil-vrag.png')  # Загружаем врага
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width  # Задаем ширину
        self.rect.y = self.rect.height  # Задаем высоту
        self.x = float(self.rect.x)  # Задаем начальную координату x
        self.y = float(self.rect.y)  # Задаем начальную координанту y

    def draw(self):  # Выводи врага на экран
        self.screen.blit(self.image, self.rect)

    def update(self):  # Перемещение врагов
        self.y += 0.1
        self.rect.y = self.y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, monstr_gun):  # Создание пули в текущей позиции
        super(Bullet, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 4, 10)  # Создаем начальные координаты и размеры пули
        self.color = 186, 85, 211  # Задаем цвет пули
        self.speed = 25  # Задаем скорость пули
        self.rect.centerx = monstr_gun.rect.centerx
        self.rect.top = monstr_gun.rect.top
        self.y = float(self.rect.y)

    def update(self):  # Перемещение пули вверх
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):  # Рисуем пулю на экране
        pygame.draw.rect(self.screen, self.color, self.rect)


class Monstr(Sprite):  # Класс Монстр-пушки

    def __init__(self, screen):  # Инициализация Монстра-пушки
        super(Monstr, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('Images/pixil_monstr.png')  # Загружаем изображение с монстром
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom
        self.mright = False
        self.mleft = False

    def output(self):  # Изображаем монстра-пушки на экран
        self.screen.blit(self.image, self.rect)

    def update_monstr_gun(self):  # Обновление позиции монстр-пушки
        if self.mright and self.rect.right < self.screen_rect.right:
            self.center += 1.5
        elif self.mleft and self.rect.left > 0:
            self.center -= 1.5

        self.rect.centerx = self.center

    def create_monstr_gun(self):  # Размещение пушки-монстра внизу
        self.center = self.screen_rect.centerx


class Scores():  # Выводим игровую информацию
    def __init__(self, screen, stats):  # Инициализируем подсчет очков
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.text_color = (255, 140, 0)
        self.text_color_high_score = (139, 9, 139)
        self.font = pygame.font.SysFont(None, 48)
        self.image_score()
        self.image_high_score()
        self.image_monstrs()

    def image_score(self):  # Преобразование текст счета в графическое изображение
        self.score_img = self.font.render(str(self.stats.score), True, self.text_color, (0, 0, 0))
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 40
        self.score_rect.top = 20

    def show_score(self):  # Выводим счет на экран
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.monstrs.draw(self.screen)

    def image_high_score(self):  # Пробразует код в графическое изображение
        self.high_score_image = self.font.render(str(self.stats.high_score), True, self.text_color_high_score,
                                                 (0, 0, 0))
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top + 20

    def image_monstrs(self):  # Количество жизней у игрока
        self.monstrs = Group()
        for monstr_number in range(self.stats.monstr_gun_left):
            monstr_gun = Monstr(self.screen)
            monstr_gun.rect.x = 30 + monstr_number * monstr_gun.rect.width
            monstr_gun.rect.y = 15
            self.monstrs.add(monstr_gun)


class Stats():  # Создаем статистику в игре, и отслеживаем ее
    def __init__(self):  # Инициализируем статистику
        self.reset_stats()
        self.run_game = True
        with open('high_score.txt', 'r') as f:
            self.high_score = int(f.readline())

    def reset_stats(self):  # Статистика во время игры
        self.monstr_gun_left = 2
        self.score = 0


def events(screen, monstr_gun, bullets):  # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Если нажат крестик то игра закрывается
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:  # Если нажата клавиша 'D' то монстр передвигается вправо
                monstr_gun.mright = True
            elif event.key == pygame.K_a:  # Если нажата клавиша 'A' то монстр передвигается вправо
                monstr_gun.mleft = True
            elif event.key == pygame.K_SPACE:  # Если нажата клавиша 'SPACE' то монстр выпускает пулю
                new_bullet = Bullet(screen, monstr_gun)
                bullets.add(new_bullet)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                monstr_gun.mright = False
            elif event.key == pygame.K_a:
                monstr_gun.mleft = False


def update_screen(screen, bg_color, stats, scores_main, monstr_gun, inos, bullets):  # Обновление экрана
    screen.fill(bg_color)  # Создаем заливку окна
    scores_main.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    monstr_gun.output()  # Выводим монстра на экран
    inos.draw(screen)
    pygame.display.flip()  # Создаем последний экран


def update_inos(stats, screen, scores_main, monstr_gun, inos, bullets):  # Обновление позиции врагов
    inos.update()
    if pygame.sprite.spritecollideany(monstr_gun, inos):
        gun_monstr_kill(stats, screen, scores_main, monstr_gun, inos, bullets)
    inos_check(stats, screen, scores_main, monstr_gun, inos, bullets)


def update_bullets(screen, stats, scores_main, inos, bullets):  # Обновление позиции пули (удаление ее за экраном)
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, inos, True, True)
    if collisions:
        for inos in collisions.values():
            stats.score += 1 * len(inos)
        scores_main.image_score()
        check_high_score(stats, scores_main)
        scores_main.image_monstrs()
    if len(inos) == 0:
        bullets.empty()
        create_army(screen, inos)


def create_army(screen, inos):  # Создание армии врагов
    ino = Ino(screen)
    ino_width = ino.rect.width
    number_ino_x = int((700 - 2 * ino_width) / ino_width)
    ino_height = ino.rect.height
    number_ino_y = int((800 - 500 - 2 * ino_height) / ino_height)

    for row_number in range(number_ino_y):  # Создаем ряды врагов
        for ino_number in range(number_ino_x):
            ino = Ino(screen)
            ino.x = ino_width + ino_width * ino_number
            ino.y = ino_height + ino_height * row_number
            ino.rect.x = ino.x
            ino.rect.y = ino.rect.height + 3 * ino.rect.height * row_number
            inos.add(ino)


def gun_monstr_kill(stats, screen, scores_main, monstr_gun, inos, bullets):  # Столкновение пушки и армии
    if stats.monstr_gun_left > 0:
        stats.monstr_gun_left -= 1
        scores_main.image_monstrs()
        inos.empty()
        bullets.empty()
        create_army(screen, inos)
        monstr_gun.create_monstr_gun()
        time.sleep(0.5)
    else:
        stats.run_game = False
        sys.exit()


def inos_check(stats, screen, scores_main, monstr_gun, inos, bullets):  # Проверка, есть ли враги на краю экрана
    screen_rect = screen.get_rect()
    for ino in inos.sprites():
        if ino.rect.bottom >= screen_rect.bottom:
            gun_monstr_kill(stats, screen, scores_main, monstr_gun, inos, bullets)
            break


def check_high_score(stats, scores_main):  # Проверка новых рекордов
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scores_main.image_high_score()
        with open('high_score.txt', 'w') as f:
            f.write(str(stats.high_score))


def running():
    pygame.init()  # Инициализируем окно
    screen = pygame.display.set_mode((700, 800))  # Создаем размеры окна
    pygame.display.set_caption('Space events')  # Создаем название игры
    bg_color = (0, 0, 0)  # Создаем фоновый черный цвет окна
    monstr_gun = Monstr(screen)  # Инициализируем монстра на экране
    bullets = Group()  # Групируем пули
    inos = Group()  # Групируем врагов
    create_army(screen, inos)
    stats = Stats()  # Групируем статистику
    scores_main = Scores(screen, stats)

    while True:  # Обрабатываем действие пользователя в игре
        events(screen, monstr_gun, bullets)
        if stats.run_game:
            monstr_gun.update_monstr_gun()
            update_screen(screen, bg_color, stats, scores_main, monstr_gun, inos, bullets)
            update_bullets(screen, stats, scores_main, inos, bullets)
            update_inos(stats, screen, scores_main, monstr_gun, inos, bullets)


running()
