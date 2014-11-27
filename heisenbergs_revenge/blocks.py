# coding=utf-8

from pygame import *
import pyganim

BLOCK_WIDTH = 32
BLOCK_HEIGHT = 32
BLOCK_SIZE = (BLOCK_WIDTH, BLOCK_HEIGHT)
PLATFORM_COLOR = "#FF6262"

class Platform_sand(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface(BLOCK_SIZE)
        # self.image = image.load('blocks/sand1.png')
        # self.image.fill(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)


