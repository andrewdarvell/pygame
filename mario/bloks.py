#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pyganim

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
ANIMATION_BLOCKTELEPORT = [
            ('blocks/portal2.png'),
            ('blocks/portal1.png')]

class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        # self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load('blocks/platform.png')
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("blocks/dieBlock.png")
        # self.image = image.load("%s/blocks/dieBlock.png" % ICON_DIR)

class BlockTeleport(Platform):
    def __init__(self, x, y, goX,goY):
        Platform.__init__(self, x, y)
        self.goX = goX # координаты назначения перемещения
        self.goY = goY # координаты назначения перемещения
        boltAnim = []
        for anim in ANIMATION_BLOCKTELEPORT:
            boltAnim.append((anim, 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))