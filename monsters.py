import pygame
from pygame.locals import *
from assets import *
class Monster:
    typeid = -1
    health = -1
    movespeed = -1
    damage = -1
    armor = -1
    hasarmor = False
    totalhp = health + armor
    surface = []
    ismoving = True
    framemovespeed = (24 / movespeed) / 60
    def __init__(self,lane):
        self.cords = {"x":320,"y":(lane*24) + 43 - 7}
        self.lane = lane
    def update(self,grid):
        self.ismoving = True
        for tower in grid[self.lane]:
            if tower != 0:
                if self.rect().colliderect(plant.rect()):
                    self.moving = False
                    tower.ishit()
        if self.moving:
            self.cords[0] -= self.framemovespeed
    def tryeat(self,towervar):
        #runs when collides with tower
        #towervar is the variable assigned with the object of the tower that monster collides with
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
        targetdisplay.blit(self.img, (int(self.cords[0]), int(self.cords[1])))
    def rect(self):
        return pygame.Rect(self.pos[0]+5, self.pos[1]+16, 6, 16)
class RobZombie(Monster):
    def __init__(self,lane):
        self.health = 190
        self.armor = 1100
        self.movespeed = 4.7
        self.damage = 100
        Monster.__init__(self,lane)
        self.hasarmor = True
        self.typeid = 1
        self.img = assets.Images["monsters"][self.typeid]
        
