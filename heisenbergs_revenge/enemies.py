# coding=utf-8
__author__ = 'darvell'

from pygame import *
import pyganim
import math

WIDTH = 32
HEIGHT = 64
JUMP_POWER = 10
MOVE_SPEED = 5
GRAVITY = 0.35 # Сила, которая будет
COLOR = "#1df1f9"

ANIMATION_DELAY = 0.1 # скорость смены кадров
ANIMATION_LEFT = [('heisenberg/heisenberg_l.png')]
ANIMATION_RIGHT = [('heisenberg/heisenberg_r.png')]

ANIMATION_STAY_RIGHT = [('heisenberg/heisenberg_r.png', 0.1)]
ANIMATION_STAY_LEFT = [('heisenberg/heisenberg_l.png', 0.1)]

# ANIMATION_JUMP_LEFT = [('heisenberg/heisenberg_jump_l.png', 0.1)]
ANIMATION_JUMP_LEFT = [('heisenberg/heisenberg_l.png', 0.1)]
# ANIMATION_JUMP_RIGHT = [('heisenberg/heisenberg_jump_r.png', 0.1)]
ANIMATION_JUMP_RIGHT = [('heisenberg/heisenberg_r.png', 0.1)]

# ANIMATION_JUMP = [('heisenberg/heisenberg_jump_r.png', 0.1)]
ANIMATION_JUMP = [('heisenberg/heisenberg_jump_r.png', 0.1)]

class Bandit(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.image = Surface((WIDTH, HEIGHT))


        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        self.boltAnimStayRight = pyganim.PygAnimation(ANIMATION_STAY_RIGHT)
        self.boltAnimStayRight.play()
        self.boltAnimStayRight.blit(self.image, (0, 0)) # По-умолчанию, стоим

        self.boltAnimStayLeft = pyganim.PygAnimation(ANIMATION_STAY_LEFT)
        self.boltAnimStayLeft.play()
        self.boltAnimStayLeft.blit(self.image, (0, 0)) # По-умолчанию, стоим

        self.boltAnimJumpLeft= pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight= pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.boltAnimJump= pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJump.play()

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p): # если есть пересечение платформы с игроком
                if xvel > 0:                      # если движется вправо
                    self.rect.right = p.rect.left # то не движется вправо

                if xvel < 0:                      # если движется влево
                    self.rect.left = p.rect.right # то не движется влево

                if yvel > 0:                      # если падает вниз
                    self.rect.bottom = p.rect.top # то не падает вниз
                    self.onGround = True          # и становится на что-то твердое
                    self.yvel = 0                 # и энергия падения пропадает

                if yvel < 0:                      # если движется вверх
                    self.rect.top = p.rect.bottom # то не движется вверх
                    self.yvel = 0

    def update(self,  heisx, heisy, platforms):
        path = math.sqrt(math.pow((heisx-self.rect.x),2)+math.pow(heisy-self.rect.y,2))