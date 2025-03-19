import pygame
from pygame.locals import *

class Tower:
    cost = -1 #cost in fans per placement
    range = -1
    damage = -1
    health = -1
    cooldown = -1 #seconds between each attack
    name = ''
    surface = []
    instances = []
    def __init__(self,new_cords):
        self.cords = new_cords
        Tower.instances.append(self)

class testRed(Tower):
    colour = (255,0,0)
    name = 'Red'
    instances = []
    def __init__(self,new_cords):
        Tower.__init__(self,new_cords)
        testRed.instances.append(self)