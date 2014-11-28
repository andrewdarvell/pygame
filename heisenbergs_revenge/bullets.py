# coding=utf-8
__author__ = 'darvell'

from pygame import *
import pyganim

GUNBULLET_WIDTH = 32
GUNBULLET_HEIGHT = 32

COLOR = "#1df1f9"
GUNBULLET_SPEED = 15
GUNBULLET_DIST = 300

GUNBULLET_ANIMATION = [('blocks/sand1.png', 0.1)]

class GunBullet(sprite.Sprite):
    def __init__(self, coords, direction):
        sprite.Sprite.__init__(self)
        x = coords['x']
        y = coords['y']
        self.rect = Rect(x, y, GUNBULLET_WIDTH, GUNBULLET_HEIGHT) # прямоугольный объект
        self.image = Surface((GUNBULLET_WIDTH, GUNBULLET_HEIGHT))
        self.image.fill(Color(COLOR))
        self.image.set_colorkey(Color(COLOR))
        self.is_alive = True
        self.xvel = GUNBULLET_SPEED
        self.yvel = 0
        self.direction = direction
        self.dist = 0

        self.boltAnim = pyganim.PygAnimation(GUNBULLET_ANIMATION)
        self.boltAnim.play()

        # print u'NEW BULLET'

    def update(self, colliders):
        if self.is_alive:
            self.image.fill(Color(COLOR))
            self.rect.x += self.xvel*self.direction
            self.boltAnim.blit(self.image, (0, 0))
            self.collide(0, self.yvel, colliders)

            self.rect.y += self.yvel # переносим свои положение на xvel
            self.collide(self.xvel, 0, colliders)
            self.dist += self.xvel
            if self.dist >= GUNBULLET_DIST:
                self.is_alive = False

    def collide(self, xvel, yvel, colliders):
        for c in colliders:
            if sprite.collide_rect(self, c): # если есть пересечение платформы с игроком
                if xvel > 0:                      # если движется вправо
                    self.rect.right = c.rect.left # то не движется вправо
                    self.is_alive = False

                if xvel < 0:                      # если движется влево
                    self.rect.left = c.rect.right # то не движется влево
                    self.is_alive = False

                if yvel > 0:                      # если падает вниз
                    self.rect.bottom = c.rect.top # то не падает вниз
                    self.onGround = True          # и становится на что-то твердое
                    self.yvel = 0                 # и энергия падения пропадает
                    self.is_alive = False

                if yvel < 0:                      # если движется вверх
                    self.rect.top = c.rect.bottom # то не движется вверх
                    self.yvel = 0
                    self.is_alive = False

    def get_status(self):
        return self.is_alive