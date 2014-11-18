# coding utf-8

import pygame
from pygame.locals import *

pygame.init()

background = [1, 1, 2, 2, 2, 1]
screen = [0]*6
for i in range(6):
    screen[i] = background[i]

playerpos = 3
screen[playerpos] = 8
print screen
screen[playerpos] = background[playerpos]
playerpos -= 1
screen[playerpos]=8
print(screen)