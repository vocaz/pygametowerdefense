import pygame
import gc
import random
from monsters import *
from assets import *
from towers import *

#pygame setup
clock = pygame.time.Clock()
reallength = 320
realheight = 180
scaledlength = 960
scaledheight = 540
scaledwindow = pygame.display.set_mode((scaledlength,scaledheight))
realwindow = pygame.Surface((reallength,realheight))
pygame.init()
assets.load()

#playtime management
fancount = 50
time_of_last_fan = 0
endframetext = ''
endframetextcolour = (255,255,255)
endframetextduration = 0 #duration in frames in which the text at the end of the frame stays there
projectiles = []
monster_lanes = [0,0,0,0,0]
#testing variables
dospawn = 1
spawn_fan = True

#spawn system
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

#font initialization
size16 = pygame.font.Font("data/quaver.ttf", 16)
size23 = pygame.font.Font("data/quaver.ttf", 23)
size32 = pygame.font.Font("data/quaver.ttf", 32)
size48 = pygame.font.Font("data/quaver.ttf", 48)
size60 = pygame.font.Font("data/quaver.ttf", 60)
#globals
size = 1
scalingdirection = 1
current_tower = 0
is_tomatoing = False
grid = [[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]
position = (0,0)

#mouse for mask collision setup
cursor = pygame.Surface((5,5))
cursor.fill((255,255,255))
cursor_mask = pygame.mask.from_surface(cursor)

def fan_manager():
    global time_of_last_fan
    global time_of_next_fan
    global fancount
    icon_surf = assets.Images["fans"]["counter"]
    icon_surf = pygame.transform.scale_by(icon_surf,2)
    icon_rect = icon_surf.get_rect(topleft=(5,0))
    if time_of_last_fan == 0:
        time_of_last_fan = pygame.time.get_ticks()
        time_of_next_fan = time_of_last_fan + 10000
    if spawn_fan:
        if pygame.time.get_ticks() >= time_of_next_fan:
            fancount += 25
            time_of_last_fan = 0
    realwindow.blit(size23.render("{:,}".format(fancount), False, (255, 255, 255)), (45, 12))
    realwindow.blit(icon_surf, icon_rect)
def kill_tower(towervar):
    target_cords = [towervar.cords["x"], towervar.cords["y"]]
    global grid
    print(f'{towervar} killed')
    del towervar
    grid[target_cords[1]][target_cords[0]] = 0

def handle_monsters():
    global grid
    global monsters
    global monster_lanes
    for index, monster in sorted(enumerate(monsters), reverse = True):
        monster.update(grid)
        monster.draw(realwindow)
        monster_lanes[monster.lane] = [monster.cords["x"], monster.cords["y"]]
def spawn_monster():
    lanes = [0,1,2,3,4]
    try:
        lanes.remove(lastspawnedlane)
    except:
        pass
    spawnlane = random.choice(lanes)
    lastspawnedlane = spawnlane
    monsters.append(RobZombie(spawnlane))
def closing():
    scaledwindow.fill((0,0,0))
    draw_front_and_centre_text("Closing...", (255, 255, 255))
    pygame.display.update()
    running = False
    pygame.quit()
def draw_front_and_centre_text(text,colour): #this a function designed to run at the very end of the frame. it simply draws given text of a specific font onto the scaledwindow after the realwindow has been scaled onto it
    closing_text = size60.render(text, True, colour)
    closing_text_rect = closing_text.get_rect()
    closing_text_rect.center = (scaledlength // 2, scaledheight // 2)
    scaledwindow.blit(closing_text, closing_text_rect)
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
def show_notenoughfans():
    global endframetextduration
    global endframetext
    global endframetextcolour
    endframetext = 'Not enough fans'
    endframetextcolour = pygame.Color('crimson')
    endframetextduration = 30
def check_towerselection():
    y = 0
    global fancount
    global current_tower
    global size
    global scalingdirection
    button_rect = 0
    for towertype in fetch_alltowertypes():
        hovered = False
        colour = towertype.colour
        button_surf = pygame.Surface((60, 20))
        button_surf.fill(colour)
        icon_surf = assets.Images["fans"]["icon"]
        icon_rect = icon_surf.get_rect(center = (button_surf.get_width()/2,button_surf.get_height()/2))
        icon_rect.move_ip(15,0)
        button_surf.blit(icon_surf,icon_rect)
        button_surf.blit(size16.render("{:,}".format(towertype.cost), False, (255, 255, 255)), (5, 4))
        button_rect = button_surf.get_rect(center=(40, y * 20 + 60))
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
                    if towertype.cost > fancount:
                        show_notenoughfans()
                    else:
                        current_tower = towertype
            else:
                if click == 1:
                    reset_towerselection()
        else:
            if fancount >= towertype.cost:
                button_surf.set_alpha(200)
            else:
                button_surf.set_alpha(50)
        if towertype == current_tower:
            button_surf.set_alpha(255)
            button_surf = pygame.transform.scale_by(button_surf,1.1)
        realwindow.blit(button_surf,button_rect)
        y += 1
def update_grid(gridvar):
    global monster_lanes
    global tile_surf
    global click
    global is_tomatoing
    global projectiles
    global fancount
    hovered = False
    y = 0
    for row in gridvar:
        x = 0
        for tile in row:
            cords = {"x":x,"y":y}
            tile_surf = pygame.Surface.copy(assets.Images["tiles"]["wood"])
            tile_rect = tile_surf.get_rect(topleft=(((x*24) + 100),((y*24) + 30)))
            if tile_rect.collidepoint(get_pos(1)[0], get_pos(1)[1]):
                hovered = True
            if tile == 0:
                if hovered == True:
                    tile_surf.set_alpha(255)
                    realwindow.blit(tile_surf,tile_rect)
                else:
                    tile_surf.set_alpha(120)
                    realwindow.blit(tile_surf,tile_rect)
            if isinstance(tile,Tower):
                if tile.health <= 0:
                    kill_tower(tile)
                else:
                    tile.update(monster_lanes,projectiles)
                    sprite_surf = tile.img
                    sprite_rect = sprite_surf.get_rect(bottomleft=(0,24))
                    tile_surf.blit(sprite_surf,sprite_rect)
                    if hovered == True:
                        tile_surf.set_alpha(120)
                    else:
                        tile_surf.set_alpha(255)
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
                            fancount -= current_tower.cost
                            grid[y][x] = current_tower(cords)
            hovered = False
            x += 1
        y += 1
def handle_projectiles():
    global projectiles
    for i, projectile in sorted(enumerate(projectiles), reverse=True):
        kill_bullet = False
        projectile.update()
        projectile.draw(realwindow)
        if projectile.range != 0:
            print(projectile.origin[0])
            print(projectile.range * 24)
            if projectile.cur_cords[0] - projectile.origin[0] >= projectile.range * 24:
                kill_bullet = True
        if projectile.cur_cords[0] > 352 or -32 > projectile.cur_cords[1]:
            kill_bullet = True
        if kill_bullet:
            projectiles.pop(i)
running = True
while running == True:
    if dospawn == 1:
        spawn_monster()
        dospawn = 0
    click = 0
    deltatime = clock.tick(60)
    realwindow.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closing()
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
                    if fetch_alltowertypes()[0].cost > fancount:
                        show_notenoughfans()
                    else:
                        current_tower = fetch_alltowertypes()[0]
            elif event.key == pygame.K_2:
                if current_tower == testGreen:
                    reset_towerselection()
                else:
                    if fetch_alltowertypes()[1].cost > fancount:
                        show_notenoughfans()
                    else:
                        current_tower = fetch_alltowertypes()[1]
            elif event.key == pygame.K_3:
                if current_tower == tambourine:
                    reset_towerselection()
                else:
                    if fetch_alltowertypes()[2].cost > fancount:
                        show_notenoughfans()
                    else:
                        current_tower = fetch_alltowertypes()[2]
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = 1
    check_towerselection() #draw the buttons for each tower on screen, and check if the player has one selected
    update_grid(grid) #check for updates on towers (the drawing of towers is included in this section of runtime)
    fan_manager()#update fan count, as well as increment fan count
    handle_projectiles()
    handle_monsters() #update monsters (check for collision with towers or projectiles, update pos) and draw monsters
    newwindow = pygame.transform.scale(realwindow,(scaledlength,scaledheight))
    scaledwindow.blit(newwindow, position) #update scaled size window
    if endframetext != "" and endframetextduration > 0:
        draw_front_and_centre_text(endframetext,endframetextcolour)
        endframetextduration -= 1
    check_tomato() #handle the ability to tomato band members
    pygame.display.update() #update what is seen