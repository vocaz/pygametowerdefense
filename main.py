import pygame
import gc
import random
from monsters import *
from assets import *
from towers import *
dospawn = 1
monster_timer = 1
lastspawnedlane = 0
monsters = []
#colours
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

#input handling
pos = 0
mouse_pos = []
click = 0

#pygame setup
clock = pygame.time.Clock()
reallength = 320
realheight = 180
scaledlength = 960
scaledheight = 540
scaledwindow = pygame.display.set_mode((scaledlength,scaledheight))
realwindow = pygame.Surface((reallength,realheight))
pygame.init()

#globals
size = 1
scalingdirection = 1
assets.load()
current_tower = 0
is_tomatoing = False
font = pygame.font.Font(None,40)
grid = [[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]
position = (0,0)
cursor = pygame.Surface((5,5))
cursor.fill((255,255,255))
cursor_mask = pygame.mask.from_surface(cursor)
def draw_monsters():
    global grid
    global monsters
    monster_lanes = [False, False, False, False, False]
    for index, monster in sorted(enumerate(monsters), reverse = True):
        monster.update(grid)
        monster.draw(realwindow)
        monster_lanes[monster.lane] = True
def spawn_monster():
    lanes = [0,1,2,3,4]
    try:
        lanes.remove(lastspawnedlane)
    except:
        pass
    spawnlane = random.choice(lanes)
    lastspawnedlane = spawnlane
    monsters.append(RobZombie(spawnlane))
def draw_centretext(text,colour):
    realwindow.fill((0,0,0))
    closing_text = font.render(text, True, colour)
    closing_text_rect = closing_text.get_rect()
    closing_text_rect.center = (reallength // 2, realheight // 2)
    realwindow.blit(closing_text, closing_text_rect)
    scaledwindow.blit(pygame.transform.scale(realwindow, (scaledlength,scaledheight)), position)
def reset_towerselection():
    global current_tower
    current_tower = 0
def reset_grid():
    global grid
    grid = [[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]
def fetch_alltowertypes():
    result = (Tower.__subclasses__())
    return result
def darken_colour(ogcolour):
    darkenedcolour = list(ogcolour)
    for i in range (0,3):
        darkenedcolour[i] = darkenedcolour[i]/2
    darkenedcolour = tuple(darkenedcolour)
    return darkenedcolour
def get_pos(isscaled):
    global mouse_pos
    result = 0
    if isscaled == 1:
        result = (mouse_pos[0]*(320/scaledlength), mouse_pos[1]*(180/scaledheight))
    else:
        result = mouse_pos
    return(result)
def get_scalefactor():
    result = scaledheight/realheight
    return(result)
def check_tomato():
    global is_tomatoing
    sf = get_scalefactor()
    keyed_tomato = assets.Images["tomato"][0]
    tomato_scaled_size = (80,80)
    if is_tomatoing == True:
        tomato_scaled_size = (80*1.2,80*1.2)
    tomato_size = (tomato_scaled_size[0]/sf,tomato_scaled_size[1]/sf)
    keyed_tomato_scaled = pygame.transform.scale(keyed_tomato, tomato_scaled_size)
    keyed_tomato_unscaled = pygame.transform.scale(keyed_tomato, tomato_size)
    tomato_mask = pygame.mask.from_surface(keyed_tomato_unscaled)
    tomato_rect_unscaled = keyed_tomato_unscaled.get_rect(bottomright=(320,180))
    tomato_rect_scaled = keyed_tomato_scaled.get_rect(bottomright=(scaledlength,scaledheight))
    if tomato_mask.overlap(cursor_mask, (get_pos(1)[0] - tomato_rect_unscaled.x, get_pos(1)[1] - tomato_rect_unscaled.y)):
        if click == 1:
            if is_tomatoing == False:
                is_tomatoing = True
            elif is_tomatoing == True:
                is_tomatoing = False
            print(is_tomatoing)
    scaledwindow.blit(keyed_tomato_scaled, tomato_rect_scaled)
def check_towerselection():
    y = 0
    global current_tower
    global size
    global scalingdirection
    button_rect = 0
    for towertype in fetch_alltowertypes():
        hovered = False
        colour = towertype.colour
        button_surf = pygame.Surface((60, 20))
        button_surf.fill(colour)
        button_rect = button_surf.get_rect(center=(40, y * 20 + 46))
        if button_rect.collidepoint(get_pos(1)[0], get_pos(1)[1]):
            hovered = True
        if hovered == True:
            if current_tower != towertype:
                button_surf.set_alpha(255)
                button_surf = pygame.transform.scale_by(button_surf,size)
                if size >= 1.1:
                    scalingdirection = -1
                if size < 1.1 and scalingdirection == 1:
                    size += 0.005
                if scalingdirection == -1:
                    size -= 0.005
                if size <= 1:
                    scalingdirection = 1
                if click == 1:
                    current_tower = towertype
            else:
                if click == 1:
                    reset_towerselection()
        else:
            button_surf.set_alpha(50)
        if towertype == current_tower:
            button_surf.set_alpha(255)
            button_surf = pygame.transform.scale_by(button_surf,1.1)
        realwindow.blit(button_surf,button_rect)
        y += 1
def update_grid(gridvar):
    global click
    global is_tomatoing
    hovered = False
    y = 0
    for row in gridvar:
        x = 0
        for tile in row:
            cords = {"x":x,"y":y}
            tile_surf = pygame.Surface((24,24))
            tile_rect = tile_surf.get_rect(topleft=(((x*24) + 100),((y*24) + 30)))
            if tile_rect.collidepoint(get_pos(1)[0], get_pos(1)[1]):
                hovered = True
            if tile == 0:
                if hovered == True:
                    pygame.draw.rect(realwindow,(150,150,150),tile_rect)
                else:
                    pygame.draw.rect(realwindow,white,tile_rect)
            if isinstance(tile,Tower):
                tile_surf.fill(tile.colour)
                if hovered == True:
                    tile_surf.set_alpha(120)
                realwindow.blit(tile_surf,tile_rect)
            if hovered == True:
                if click == 1:
                    if is_tomatoing == True:
                        if tile != 0:
                            print(f'Tomatoed {tile.name}')
                            del tile
                            grid[y][x] = 0
                            is_tomatoing = False
                    else:
                        if current_tower == 0:
                            pass
                        else:
                            grid[y][x] = current_tower(cords)
            hovered = False
            x += 1
        y += 1
    
    for i in range(6):
        pygame.draw.line(realwindow,(0,0,0),(100,i*24 + 30),(24*9 + 100,i*24 + 30))
    for i in range(10):
        pygame.draw.line(realwindow,(0,0,0),(i*24 + 100,30),(i*24 + 100,5*24 + 30))

running = True
while running == True:
    if dospawn == 1:
        spawn_monster()
        dospawn = 0
    click = 0
    deltatime = clock.tick(60)
    realwindow.fill((255,255,255))
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            draw_centretext("Closing...",(255,255,255))
            pygame.display.update()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tower_cords = []
                for instance in Tower.instances:
                    tower_cords.append(f'{instance.name}:{instance.cords}')
                print(tower_cords)
            elif event.key == pygame.K_r:
                reset_grid()
            elif event.key == pygame.K_1:
                if current_tower == testRed:
                    reset_towerselection()
                else:
                    current_tower = testRed
            elif event.key == pygame.K_2:
                if current_tower == testGreen:
                    reset_towerselection()
                else:
                    current_tower = testGreen
            elif event.key == pygame.K_3:
                if current_tower == testBlue:
                    reset_towerselection()
                else:
                    current_tower = testBlue
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = 1
    check_towerselection()
    update_grid(grid)
    draw_monsters()
    newwindow = pygame.transform.scale_by(realwindow,3)
    scaledwindow.blit(newwindow, position)
    check_tomato()
    pygame.display.update()
    print(get_pos(1))
pygame.quit()
