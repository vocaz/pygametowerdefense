import pygame

class assets:
    @classmethod
    def load(cls):
        root = 'data/'
        cls.Images = {
    "projectiles":{1:pygame.image.load("data/images/projectiles/tambourine.png"),},
    "tiles":{"wood":pygame.image.load("data/images/misc/wood tile.png")},
    "fans":{"counter":pygame.image.load("data/images/ui/fan counter.png"),"icon":pygame.image.load("data/images/ui/fan icon.png")},
    "towers":{1:pygame.image.load("data/images/towers/tambourine.png")},
    "tomato":[pygame.image.load("data/images/ui/tomato.png").convert_alpha(),0],
    "monsters":{1:pygame.image.load("data/images/monsters/normal.png")}
    }