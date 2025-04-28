import pygame
from pygame.locals import *

class Monster:
    typeid = -1
    health = -1
    movespeed = -1
    damage = -1
    armor = -1
    hasarmor = False
    totalhp = health + armor
    surface = []
    def __init__(self,lane):
        self.cords = {"x":320,"y":(lane*24) + 43 - 7}
    def tryeat(self,towervar):
        #runs when collides with tower
        #towervar is the variable assigned with the object of the tower that monster collides with
        towervar.ishit(damage)
    def ishit(self,damage):
        #Runs when either collides with a projectile or is hit by a melee range character
        if hasarmor = True:
            totalhealth -= damage
            if totalhealth < health:
                armorbreak()
        if totalhealth < 0:
            pass
    def armorbreak(self):
        hasarmor = False
        armor = 0
class RobZombie(monster):
    def __init__(self,lane):
        health = 190
        armor = 1100
        movespeed = 4.7
        damage = 100
        Monster.__init__(self,lane)
        hasarmor = True
        typeid = 1
        