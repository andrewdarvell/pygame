# coding=utf-8
__author__ = 'darvell'

from pygame import *
import pyganim

WIDTH = 32
HEIGHT = 64
JUMP_POWER = 10
MOVE_SPEED = 5
GRAVITY = 0.35 # Сила, которая будет
COLOR = "#1df1f9"



ANIMATION_DELAY = 0.1 # скорость смены кадров
ANIMATION_LEFT = [('heisenberg/heisenberg_l.png'),
                  ('heisenberg/heisenberg_l_1.png'),
                  ('heisenberg/heisenberg_l.png'),
                  ('heisenberg/heisenberg_l_2.png'),]

ANIMATION_RIGHT = [('heisenberg/heisenberg_r.png'),
                   ('heisenberg/heisenberg_r_1.png'),
                   ('heisenberg/heisenberg_r.png'),
                   ('heisenberg/heisenberg_r_2.png'),]

ANIMATION_STAY_RIGHT = [('heisenberg/heisenberg_r.png', 0.1)]
ANIMATION_STAY_LEFT = [('heisenberg/heisenberg_l.png', 0.1)]

ANIMATION_JUMP_LEFT = [('heisenberg/heisenberg_l_jump.png', 0.1)]
# ANIMATION_JUMP_LEFT = [('heisenberg/heisenberg_l.png', 0.1)]
ANIMATION_JUMP_RIGHT = [('heisenberg/heisenberg_r_jump.png', 0.1)]
# ANIMATION_JUMP_RIGHT = [('heisenberg/heisenberg_r.png', 0.1)]

# ANIMATION_JUMP = [('heisenberg/heisenberg_jump_r.png', 0.1)]
ANIMATION_JUMP = [('heisenberg/heisenberg_jump_r.png', 0.1)]

class Heisenberg(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0   #скорость перемещения. 0 - стоять на месте
        self.yvel = 0 # скорость вертикального перемещения
        self.onGround = False # На земле ли я?
        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект
        self.image = Surface((WIDTH, HEIGHT))
        # self.image.fill(Color(COLOR<))

        self.face_right = True

        self.image.set_colorkey(Color(COLOR))
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()

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
                    self.yvel = 0                 # и энергия прыжка пропадает

    def update(self,  left, right, up, platforms):
        self.image.fill(Color(COLOR))
        if up:
            if self.onGround: # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
            self.image.fill(Color(COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))

        if left:
            self.face_right = False
            self.xvel = -MOVE_SPEED # Лево = x- n
            self.image.fill(Color(COLOR))
            if not up: # и не прыгаем
                self.boltAnimLeft.blit(self.image, (0, 0))  # отображаем анимацию движения
            if up:  # если же прыгаем
                self.boltAnimJumpLeft.blit(self.image, (0, 0))  # отображаем анимацию прыжка

        if right:
            self.face_right = True
            self.xvel = MOVE_SPEED # Право = x + n
            self.image.fill(Color(COLOR))
            if not up:
                self.boltAnimRight.blit(self.image, (0, 0))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))

        if not(left or right): # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                self.image.fill(Color(COLOR))
                if self.face_right:
                    self.boltAnimStayRight.blit(self.image, (0, 0))
                else:
                    self.boltAnimStayLeft.blit(self.image, (0, 0))

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def get_xy(self):
        return {'x': self.rect.x, 'y': self.rect.y}

    def get_direction(self):
        if self.face_right:
            return 1
        else:
            return -1