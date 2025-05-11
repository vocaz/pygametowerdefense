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
        if self.typeid == 2:
            assets.Images["projectiles"][self.typeid] = assets.Images["projectiles"][self.typeid].convert_alpha()
        targetdisplay.blit(self.img, (int(self.cur_cords[0]), int(self.cur_cords[1])))
class Sun:
    def __init__(self,cords,velocity = [0,0],value = 25,life = 500, wave = True):
        self.cur_cords = cords
        self.velocity = velocity
        self.value = value
        self.img = assets.Images["fans"]["icon"]
        self.max_life = life
        self.life = life
        self.wave = wave
    def rect(self):
        return pygame.Rect(self.cur_cords, [16,16])
    def update(self):
        self.life -= 1
        self.cur_cords[0] += self.velocity[0] + (math.sin(math.radians(self.max_life-self.life))/3)*self.wave #method to make the sun move left to right in a wave motion (dont ask me for the math I chat GPT'd it)
        self.cur_cords[1] += self.velocity[1]
    def draw(self, targetdisplay):
        targetdisplay.blit(self.img, (int(self.cur_cords[0]), int(self.cur_cords[1])))