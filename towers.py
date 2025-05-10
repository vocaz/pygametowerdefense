import pygame

import assets
from assets import *
from pygame.locals import *
from bullets import *
class Tower:
    typeid = 0
    cost = -1 #cost in fans per placement
    range = -1
    damage = -1
    health = -1
    cooldown = -1 #seconds between each attack
    name = ''
    last_attack_time = 0
    time_next_attack = 0
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
    cost = 75
    health = 300
    colour = (255,0,0)
    name = 'Red'
    instances = []
    def __init__(self,new_cords):
        Tower.__init__(self,new_cords)
        testRed.instances.append(self)
class testGreen(Tower):
    cost = 50
    health = 300
    colour = (0,255,0)
    name = 'Green'
    instances = []
    def __init__(self,new_cords):
        Tower.__init__(self,new_cords)
        testGreen.instances.append(self)
class tambourine(Tower):
    typeid = 1
    cooldown = 1.425
    cost = 50
    range = 6
    damage = 20
    health = 300
    colour = (0,0,255)
    name = 'Tambourine'
    instances = []
    def __init__(self,new_cords):
        Tower.__init__(self,new_cords)
        self.img = assets.Images["towers"][self.typeid]
        tambourine.instances.append(self)
    def update(self,monster_lanes,projectiles):
        if monster_lanes[self.cords["y"]] != 0:
            if monster_lanes[self.cords["y"]][0] <= (24*self.range + self.cords["x"]*24 + 100):
                self.tryattack(((self.cords['x']*24 + 100),(self.cords['y']*24+30)),projectiles)
    def tryattack(self,origin,projectiles):
        if self.last_attack_time == 0:
            self.last_attack_time = pygame.time.get_ticks()
            self.time_next_attack = self.last_attack_time + (self.cooldown * 1000)
        if pygame.time.get_ticks() >= self.time_next_attack:
            projectiles.append(Bullet(1,[origin[0],origin[1]],[2,0],self.damage,0))
            self.last_attack_time = 0
