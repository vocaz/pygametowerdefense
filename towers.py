import pygame

import assets
from assets import *
from pygame.locals import *
class Tower:
    typeid = 0
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
    def rect(self):
        tile_surf = pygame.Surface((24,24))
        tile_rect = tile_surf.get_rect(topleft=(((self.cords["x"]*24) + 100),((self.cords["y"]*24) + 30)))
        return tile_rect
    def ishit(self, dmg):
        self.health -= dmg
        print(f'current hp = {self.health}')
class testRed(Tower):
    health = 300
    colour = (255,0,0)
    name = 'Red'
    instances = []
    def __init__(self,new_cords):
        Tower.__init__(self,new_cords)
        testRed.instances.append(self)
class testGreen(Tower):
    health = 300
    colour = (0,255,0)
    name = 'Green'
    instances = []
    def __init__(self,new_cords):
        Tower.__init__(self,new_cords)
        testGreen.instances.append(self)
class tambourine(Tower):
    typeid = 1
    health = 300
    colour = (0,0,255)
    name = 'Tambourine'
    instances = []
    def __init__(self,new_cords):
        Tower.__init__(self,new_cords)
        self.img = assets.Images["towers"][self.typeid]
        tambourine.instances.append(self)