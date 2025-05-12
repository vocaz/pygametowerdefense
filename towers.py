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
    def update(self,monster_lanes,projectiles):
        if monster_lanes[self.cords["y"]] != 0:
            if monster_lanes[self.cords["y"]][0] <= (24*self.range + self.cords["x"]*24 + 100):
                self.tryattack(((self.cords['x']*24 + 100),(self.cords['y']*24+35)),projectiles)
    def rect(self):
        tile_surf = pygame.Surface((24,24))
        tile_rect = tile_surf.get_rect(topleft=(((self.cords["x"]*24) + 100),((self.cords["y"]*24) + 30)))
        return tile_rect
    def ishit(self, dmg):
        self.health -= dmg
class tambourine(Tower):
    typeid = 1
    cooldown = 1.425
    cost = 125
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
    def tryattack(self,origin,projectiles):
        if self.last_attack_time == 0:
            self.last_attack_time = pygame.time.get_ticks()
            self.time_next_attack = self.last_attack_time + (self.cooldown * 1000)
        if pygame.time.get_ticks() >= self.time_next_attack:
            projectiles.append(Bullet(1,[origin[0],origin[1]],[2,0],self.damage,0))
            self.last_attack_time = 0
class bassist(Tower):
    typeid = 2
    cooldown = 1.425
    cost = 100
    range = 1
    damage = 50
    health = 800
    colour = (255,0,0)
    name = 'Bassist'
    attack_anim_frame_counter = 0
    instances = []
    def __init__(self,new_cords):
        Tower.__init__(self,new_cords)
        self.idle_img = assets.Images["towers"][self.typeid][0]
        self.atk_img = assets.Images["towers"][self.typeid][1]
        self.img = self.idle_img
        bassist.instances.append(self)
    def update(self,monster_lanes,projectiles):
        if self.attack_anim_frame_counter > 0:
            self.img = self.atk_img
            self.attack_anim_frame_counter -= 1
        if self.attack_anim_frame_counter == 0:
            self.img = self.idle_img
        if monster_lanes[self.cords["y"]] != 0:
            if monster_lanes[self.cords["y"]][0] <= (24 * self.range + self.cords["x"] * 24 + 100):
                self.tryattack(((self.cords['x'] * 24 + 100), (self.cords['y'] * 24 + 30)), projectiles)
    def tryattack(self,origin,projectiles):
        if self.last_attack_time == 0:
            self.last_attack_time = pygame.time.get_ticks()
            self.time_next_attack = self.last_attack_time + (self.cooldown * 1000)
        if pygame.time.get_ticks() >= self.time_next_attack:
            self.attack_anim_frame_counter = 30
            projectiles.append(Bullet(2, [origin[0], origin[1]], [2, 0], self.damage, 1))
            self.last_attack_time = 0
class cd_player(Tower):
    typeid = 3
    cooldown = 12
    range = 0
    cost = 50
    health = 300
    colour = (120,120,120)
    name = 'CD Player'
    instances = []
    def __init__(self,new_cords):
        Tower.__init__(self,new_cords)
        cd_player.instances.append(self)
        self.img = assets.Images["towers"][self.typeid]
    def update(self,monster_lanes,projectiles):
            self.tryattack(((self.cords['x']*24 + 100),(self.cords['y']*24+30)),projectiles)
    def tryattack(self,origin,projectiles):
        if self.last_attack_time == 0:
            self.last_attack_time = pygame.time.get_ticks()
            self.time_next_attack = self.last_attack_time + (self.cooldown * 1000)
        if pygame.time.get_ticks() >= self.time_next_attack:
            projectiles.append(Sun([origin[0],origin[1]], [0, 0.1]))
            self.last_attack_time = 0