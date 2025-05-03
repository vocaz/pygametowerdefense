import pygame

class assets:
    @classmethod
    def load(cls):
        root = 'data/'
        cls.Images = {
    "towers":{1:pygame.image.load("data/images/towers/tambourine.png")},
    "tomato":[pygame.image.load("data/images/ui/tomato.png").convert_alpha(),0],
    "monsters":{1:pygame.image.load("data/images/monsters/normal.png")}
    }