import pygame
import time
from pygame.locals import *
from assets import *
class Monster:
    cooldown = 1
    typeid = -1
    health = -1
    movespeed = -1
    damage = -1
    armor = -1
    hasarmor = False
    totalhp = health + armor
    surface = []
    time_next_attack = 0
    ismoving = True
    def __init__(self,lane):
        self.cords = {"x":304,"y":(lane*24)+24}
        self.lane = lane
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
        curtime = time.time()
        self.time_next_attack = curtime + self.cooldown
        if curtime >= self.time_next_attack:
            towervar.ishit(damage)
    def ishit(self,damage):
        #Runs when either collides with a projectile or is hit by a melee range character
        if hasarmor == True:
            totalhealth -= damage
            if totalhealth < health:
                armorbreak()
        if totalhealth < 0:
            pass
    def armorbreak(self):
        hasarmor = False
        armor = 0
    def draw(self, targetdisplay):
        targetdisplay.blit(self.img, (int(self.cords["x"]), int(self.cords["y"])))
    def rect(self):
        return pygame.Rect(self.cords["x"]+5, self.cords["y"]+16, 6, 16)
class RobZombie(Monster):
    def __init__(self,lane):
        self.health = 190
        self.armor = 1100
        self.movespeed = 0.050
        self.damage = 100
        Monster.__init__(self,lane)
        self.hasarmor = True
        self.typeid = 1
        self.img = assets.Images["monsters"][self.typeid]
        
