# coding=utf-8
__author__ = 'darvell'

from pygame import *
import pyganim
import math
import bullets
import blocks

WIDTH = 32
HEIGHT = 64
JUMP_POWER = 15
MOVE_SPEED = 3
GRAVITY = 0.35 # Сила, которая будет
COLOR = "#1df1f9"
RELOAD_TIME = 100

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
        self.image.set_colorkey(Color(COLOR))
        self.is_alive = True
        self.lifes = 3
        self.brake = 0
        self.no_path = False
        self.need_bullet = False
        self.direction = 0
        self.reload = RELOAD_TIME

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

    def collide(self, xvel, yvel, objects):
        for p in objects:
            if sprite.collide_rect(self, p):
                if isinstance(p, blocks.Platform_sand):
                    if xvel > 0:                      # если движется вправо
                        self.rect.right = p.rect.left # то не движется вправо
                        # self.yvel = -10
                        self.no_path = True

                    if xvel < 0:                      # если движется влево
                        self.rect.left = p.rect.right # то не движется влево
                        # self.yvel = -10
                        self.no_path = True

                    if yvel > 0:                      # если падает вниз
                        self.rect.bottom = p.rect.top # то не падает вниз
                        self.onGround = True          # и становится на что-то твердое
                        self.yvel = 0                 # и энергия падения пропадает

                    if yvel < 0:                      # если движется вверх
                        self.rect.top = p.rect.bottom # то не движется вверх
                        self.yvel = 0

    def update(self,  heis_coord, objects):
        if self.is_alive and self.brake == 0:
            self.image.fill(Color(COLOR))
            heisx = heis_coord.get('x')
            heisy = heis_coord.get('y')
            # self.xvel = 0
            # self.yvel = 0


            path = math.sqrt(math.pow((heisx-self.rect.x), 2)+math.pow(heisy-self.rect.y, 2))
            # print path
            directx = 1  # направление движения по x
            directy = 1  # направление движения по y

            if not self.onGround:
                self.yvel += GRAVITY

            self.onGround = False
            self.rect.y += self.yvel
            self.collide(0, self.yvel, objects)


            if (path >= 50) and (path <500):
                if heisx < self.rect.x:
                    directx = -1
                    self.boltAnimLeft.blit(self.image, (0, 0))
                    self.direction = -1
                elif heisx > self.rect.x:
                    directx = 1
                    self.boltAnimRight.blit(self.image, (0, 0))
                    self.direction = 1
                elif heisx == self.rect.x:
                    # directx = 0
                    self.boltAnimRight.blit(self.image, (0, 0))

                if self.reload == 0:
                    self.need_bullet = True
                    self.reload = RELOAD_TIME
                    print self.reload
                elif self.reload > 0:
                    self.reload -= 1

                self.xvel = MOVE_SPEED * directx
                self.rect.x += self.xvel
                self.collide(self.xvel, 0, objects)

                pathy = math.fabs(heisy - self.rect.y)
                if (heisy < self.rect.y) and self.onGround and (pathy > 100):
                    self.jump()
                if self.onGround and self.no_path:
                    self.jump()
                    self.no_path = False
            else:
                self.boltAnimRight.blit(self.image, (0, 0))
        else:
            self.brake -= 1

    def get_status(self):
        return self.is_alive

    def jump(self):
        self.yvel = -JUMP_POWER

    def set_hit(self):
        if self.is_alive:
            if self.lifes > 1:
                self.lifes -= 1
                print 'Hit enemy!!!!'
                self.brake = 50
            else:
                self.is_alive = False
                print 'Enemy down!!'

    def get_xy(self):
        return {'x': self.rect.x, 'y': self.rect.y}

    def get_nbullet(self):
        return self.need_bullet

    def set_ndullet(self, value):
        self.need_bullet = value
        print 'Need bullet False!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'

    def get_direction(self):
        return self.direction
