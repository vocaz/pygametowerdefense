import pygame

class assets:
    @classmethod
    def load(cls):
        root = 'data/'
        cls.Images = {
    "tomato":[pygame.image.load("data/images/ui/tomato.png").convert_alpha(),0]}