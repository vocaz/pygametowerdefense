import pygame
import time
from pygame.locals import *
from assets import *
from bullets import *
class Monster:
    cooldown = 1
    typeid = -1
    health = -1
    movespeed = -1
    damage = -1
    armor = -1
    hasarmor = False
    surface = []
    last_attack_time = 0
    time_next_attack = 0
    ismoving = True
    def __init__(self,lane):
        self.cords = {"x":304,"y":(lane*24)+24}
        self.lane = lane
        self.totalhp = self.health + self.armor
    def update(self,grid):
        self.ismoving = True
        for tower in grid[self.lane]:
            if tower != 0:
                if self.rect().colliderect(tower.rect()):
                    self.ismoving = False
                    self.tryeat(tower)
        if self.ismoving:
            self.cords["x"] -= self.movespeed
    def tryeat(self,towervar):
        if self.last_attack_time == 0:
            self.last_attack_time = pygame.time.get_ticks()
            self.time_next_attack = self.last_attack_time + (self.cooldown * 1000)
        if pygame.time.get_ticks() >= self.time_next_attack:
            towervar.ishit(self.damage)
            self.last_attack_time = 0
    def ishit(self,damage):
        #Runs when either collides with a projectile or is hit by a melee range character
        if self.hasarmor == True:
            self.totalhp -= damage
            if self.totalhp < self.health:
                self.armorbreak()
        else:
            self.totalhp -= damage
    def armorbreak(self):
        hasarmor = False
        armor = 0
    def draw(self, targetdisplay):
        targetdisplay.blit(self.img, (int(self.cords["x"]), int(self.cords["y"])))
    def rect(self):
        return pygame.Rect(self.cords["x"]+5, self.cords["y"]+16, 6, 16)
class RobZombie(Monster):
    def __init__(self,lane):
        self.health = 181
        self.armor = 0
        self.movespeed = 0.03
        self.damage = 100
        Monster.__init__(self,lane)
        self.hasarmor = False
        self.typeid = 1
        self.img = assets.Images["monsters"][self.typeid]
class Buckethead(Monster):
    def __init__(self,lane):
        self.health = 181
        self.armor = 300
        self.movespeed = 0.03
        self.damage = 100
        Monster.__init__(self, lane)
        self.hasarmor = True
        self.typeid = 2
        self.armor_img = assets.Images["monsters"][self.typeid]
        self.noarmor_img = assets.Images["monsters"][1]
        self.img = self.armor_img
    def armorbreak(self):
        self.img = self.noarmor_img
        self.hasarmor = False
        self.armor = 0
class IronMaiden(Monster):
    def __init__(self,lane):
        self.armor = 50
        self.health = 181
        self.movespeed = 0.1
        self.damage = 100
        Monster.__init__(self, lane)
        self.hasarmor = True
        self.typeid = 3
        self.armor_img = assets.Images["monsters"][self.typeid][0]
        self.noarmor_img = assets.Images["monsters"][self.typeid][1]
        self.img = self.armor_img
    def armorbreak(self):
        self.img = self.noarmor_img
        self.hasarmor = False
        self.armor = 0
        self.movespeed = 0.03
