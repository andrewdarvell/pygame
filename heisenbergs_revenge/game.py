# coding=utf-8

import pygame
import heisenberg
from pygame import *
from blocks import *

import tiledtmxloader

import helperspygame # Преобразует tmx карты в формат  спрайтов pygame


WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота окна
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#1df1f9"
CENTER_OF_SCREEN = WIN_WIDTH / 2, WIN_HEIGHT / 2



class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def reverse(self, pos):# получение внутренних координат из глобальных
        return pos[0] - self.state.left, pos[1] - self.state.top

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)

def load_level(path):
    global playerX, playerY # объявляем глобальные переменные, это координаты героя
    global total_level_height, total_level_width
    global sprite_layers # все слои карты

    world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(path)
    resources = helperspygame.ResourceLoaderPygame()
    resources.load(world_map)

    sprite_layers = helperspygame.get_layers_from_map(resources)
    platforms_layer = sprite_layers[1]

    for row in range(0, platforms_layer.num_tiles_x): # перебираем все координаты тайлов
        for col in range(0, platforms_layer.num_tiles_y):
            if platforms_layer.content2D[col][row] is not None:
                pf = Platform_sand(row * BLOCK_HEIGHT, col * BLOCK_WIDTH)# как и прежде создаем объкты класса Platform
                platforms.append(pf)

    monsters_layer = sprite_layers[2]
    for monster in monsters_layer.objects:
        try:
            x = monster.x
            y = monster.y
            if monster.name == "Heisenberg":
                playerX = x
                playerY = y - 64
        except:
            print(u"Ошибка на слое монстров")

    total_level_width = platforms_layer.num_tiles_x * BLOCK_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = platforms_layer.num_tiles_y * BLOCK_HEIGHT   # высоту


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Heisenberg's Revenge")
    bg = Surface((WIN_WIDTH, WIN_HEIGHT)) # Создание видимой поверхности
    renderer = helperspygame.RendererPygame() # визуализатор
    bg.fill(Color(BACKGROUND_COLOR))


    timer = pygame.time.Clock()
    load_level('maps/map1.tmx')
    # load_level('/home/darvell/PycharmProjects/SuperMarioBoy-0.2.2/levels/map_1.tmx')
    camera = Camera(camera_configure, total_level_width, total_level_height)

    left = right = False # по умолчанию - стоим
    up = False
    running = False

    try:
        hero = heisenberg.Heisenberg(playerX, playerY) # создаем героя по (x,y) координатам
        entities.add(hero)
    except:
        print (u"Не удалось на карте найти героя, взяты координаты по-умолчанию")
        hero = heisenberg.Heisenberg(65, 65)
    entities.add(hero)

    while 1:
        timer.tick(60)
        for e in pygame.event.get(): # Обрабатываем события
            if e.type == QUIT:
                raise SystemExit, "QUIT"

            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit, "QUIT"

            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
               right = True

            if e.type == KEYUP and e.key == K_RIGHT:
               right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
            if e.type == KEYUP and e.key == K_SPACE:
                up = False

            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True
            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False

        for sprite_layer in sprite_layers: # перебираем все слои
            if not sprite_layer.is_object_group: # и если это не слой объектов
                renderer.render_layer(screen, sprite_layer) # отображаем его
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        center_offset = camera.reverse(CENTER_OF_SCREEN)
        camera.update(hero)
        renderer.set_camera_position_and_size(center_offset[0], center_offset[1], WIN_WIDTH, WIN_HEIGHT, "center")
        hero.update(left, right, up, platforms) # передвижение
        pygame.display.update()     # обновление и вывод всех изменений на экран
        screen.blit(bg, (0, 0))      # Каждую итерацию необход

entities = pygame.sprite.Group() # Все объекты
platforms = []
if __name__ == "__main__":
    main()