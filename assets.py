import pygame

class assets:
    @classmethod
    def load(cls):
        root = 'data/'
        cls.Images = {
    "menus":{1:pygame.image.load("data/images/start_menu/menu 2.png")},
    "projectiles":{1:pygame.image.load("data/images/projectiles/tambourine.png"),
                   2:pygame.Surface([640,480], pygame.SRCALPHA, 32)}, #transparent surface for towers with no visible projectiles (melee characters),
    "tiles":{"wood":pygame.image.load("data/images/misc/wood tile.png")},
    "fans":{"counter":pygame.image.load("data/images/ui/fan counter.png"),"icon":pygame.image.load("data/images/ui/fan icon.png")},
    "towers":{1:pygame.image.load("data/images/towers/tambourine.png"),
              2:[pygame.image.load("data/images/towers/bassist.png"),pygame.image.load("data/images/towers/bassist_attack.png")],
              3:pygame.image.load("data/images/towers/cd player.png"),},
    "tomato":[pygame.image.load("data/images/ui/tomato.png").convert_alpha(),0],
    "monsters":{1:pygame.image.load("data/images/monsters/normal.png"),
                2:pygame.image.load("data/images/monsters/buckethead.png"),
                3:[pygame.image.load("data/images/monsters/iron_maiden_with_helmet.png"),pygame.image.load("data/images/monsters/iron_maiden_no_helmet.png")]}
    }