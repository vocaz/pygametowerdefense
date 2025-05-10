import pygame
import math
import random
from assets import *

class Bullet:
    def __init__(self,typeid,cords,velocity,damage,range):
        self.typeid = typeid
        self.distance_moved = 0
        self.cur_cords = cords
        self.velocity = velocity
        self.damage = damage
        self.img = assets.Images["projectiles"][typeid]
        self.range = range
    def get_rect(self):
        return pygame.Rect(self.cur_cords, self.img.get_size())
    def update(self):
        self.cur_cords[0] += self.velocity[0]
        self.cur_cords[1] += self.velocity[1]
        self.distance_moved += self.velocity[0]
    def draw(self, targetdisplay):
        targetdisplay.blit(self.img, (int(self.cur_cords[0]), int(self.cur_cords[1])))