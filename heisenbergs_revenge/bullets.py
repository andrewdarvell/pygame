# coding=utf-8
__author__ = 'darvell'

from pygame import *
import pyganim
import enemies
import heisenberg
import blocks

GUNBULLET_WIDTH = 5
GUNBULLET_HEIGHT = 3

COLOR = "#1df1f9"
GUNBULLET_SPEED = 10
GUNBULLET_DIST = 500

GUNBULLET_ANIMATION_RIGHT = [('bullets/bullet_r.png', 0.1)]
GUNBULLET_ANIMATION_LEFT = [('bullets/bullet_l.png', 0.1)]

class GunBullet(sprite.Sprite):
    def __init__(self, coords, direction, player):
        sprite.Sprite.__init__(self)
        x = coords['x']
        y = coords['y']
        self.rect = Rect(x, y, GUNBULLET_WIDTH, GUNBULLET_HEIGHT) # прямоугольный объект
        self.image = Surface((GUNBULLET_WIDTH, GUNBULLET_HEIGHT))
        self.image.fill(Color(COLOR))
        self.image.set_colorkey(Color(COLOR))
        self.is_alive = True
        self.xvel = 0
        self.yvel = 0
        self.direction = direction
        self.dist = 0
        self.from_player = player

        self.boltAnimRight = pyganim.PygAnimation(GUNBULLET_ANIMATION_RIGHT)
        self.boltAnimRight.play()

        self.boltAnimLeft = pyganim.PygAnimation(GUNBULLET_ANIMATION_LEFT)
        self.boltAnimLeft.play()

        print u'NEW BULLET'

    def update(self, colliders):
        if self.is_alive:
            self.image.fill(Color(COLOR))

            # self.xvel = 0
            # self.yvel = 0

            self.xvel = GUNBULLET_SPEED * self.direction
            self.collide(0, self.rect.x + self.xvel, colliders)
            self.rect.x += self.xvel


            self.dist += GUNBULLET_SPEED

            self.collide(self.rect.y + self.yvel, 0, colliders)
            self.rect.y += self.yvel

            if self.direction > 0:
                self.boltAnimRight.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))
            if self.dist >= GUNBULLET_DIST:
                self.is_alive = False

    def collide(self, xvel, yvel, colliders):
        for c in colliders:
            if sprite.collide_rect(self, c): # если есть пересечение платформы с игроком
                if isinstance(c, enemies.Bandit) and self.from_player:
                    if c.get_status():
                        self.xvel = 0
                        self.yvel = 0
                        self.is_alive = False
                        c.set_hit()

                if isinstance(c, heisenberg.Heisenberg) and not self.from_player:
                    self.xvel = 0
                    self.yvel = 0
                    self.is_alive = False
                    print 'Head shot!!!'

                if isinstance(c, blocks.Platform_sand):
                    self.xvel = 0
                    self.yvel = 0
                    self.is_alive = False

    def get_status(self):
        return self.is_alive

    def set_not_alive(self):
        print 'set not alive bullet'
        self.is_alive = True