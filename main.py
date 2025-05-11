import pygame
import random
import os
import pickle
import time
from monsters import *
from assets import *
from towers import *

#achievement/stats system
stats_from_session = {'cur_level': 0, 'monsterkills':0, 'fansgenerated':0,'towersplaced':0}

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

#level storage and spawning
spawn_list = []
is_newlevel = True
last_spawn = 0
next_spawn = 0
lastspawnedlane = -1
monsters = []
spawn_index = 0

#playtime management
fancount = 50
time_of_last_fan = 0
projectiles = []
monster_lanes = [0,0,0,0,0]
#testing variables
dospawn = 1
spawn_fan = True

#spawn system
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
dead = False
level_total_zombies = 0
loaded_save = False
at_menu = False
at_intermission = True
start_menu_progress = 1
cur_level = 0
available_towers = []
endframetext = ''
endframetextcolour = (255,255,255)
endframetextduration = 0 #duration in frames in which the text at the end of the frame stays there
towerselection_size = 1
towerselection_scalingdirection = 1
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
def save_handler():
    global loaded_save
    global cur_level
    global at_menu
    global at_intermission
    global stats_from_session #must be changed and kept over multiple function runs
    if not os.path.isfile('save/stats.txt'):
        with open('save/stats.txt', 'wb') as stats_file:
            pickle.dump(stats_from_session, stats_file)
    if not loaded_save:
        with open('save/stats.txt', 'rb') as loaded_file:
            stats_from_session = pickle.load(loaded_file)
        loaded_save = True
    if stats_from_session['cur_level'] == 0:
        at_menu = True
        at_intermission = False
        stats_from_session['cur_level'] = 1
    cur_level = stats_from_session['cur_level']
def start_menu(stats_from_session):
    global cur_level
    global at_menu
    global at_intermission
    global start_menu_progress
    if at_menu:
        if start_menu_progress > 2:
            at_intermission = True
            at_menu = False
        else:
            match start_menu_progress:
                case 1:
                    centre_text = "Welcome to Battle of the Bands!\n You will be started at level 1\n To progress to the next menu\n click the mouse"
                    centre_text = centre_text.split("\n")
                    y_oftext = scaledheight // 2 - 20
                    for line in centre_text:
                        closing_text = size48.render(line, True, white)
                        closing_text_rect = closing_text.get_rect()
                        closing_text_rect.center = (scaledlength // 2, y_oftext)
                        y_oftext += 48
                        scaledwindow.blit(closing_text, closing_text_rect)
                    pygame.display.update()
                case 2:
                    scaledwindow.fill((0,0,0))
                    image_rect = assets.Images['menus'][1].get_rect()
                    image_rect.center = (scaledlength // 2, scaledheight // 2)
                    scaledwindow.blit(assets.Images['menus'][1], image_rect)
                    pygame.display.update()
            if click == 1:
                start_menu_progress += 1
    else:
        pass
def intermission(cur_level,available_towers,stats_from_session):
    global at_intermission
    if at_intermission:
        scaledwindow.fill(pygame.Color('black'))
        # draw centre text displaying next level
        centre_text = f"Next Level:\n{cur_level}"
        centre_text = centre_text.split("\n")
        y_of_text = scaledheight // 2 - 50
        for line in centre_text:
            line_text = size48.render(line, True, white)
            line_text_rect = line_text.get_rect()
            line_text_rect.center = (scaledlength // 2, y_of_text)
            y_of_text += 55
            scaledwindow.blit(line_text, line_text_rect)
        # draw bottom left text displaying available towers
        available_text = size32.render('Available Towers:', True, white)
        available_text_rect = available_text.get_rect()
        available_text_rect.midleft = (30, 300)
        scaledwindow.blit(available_text, available_text_rect)
        #draw available towers
        midleft_x = 15
        for tower in available_towers:
            preview_surface = assets.Images['towers'][tower.typeid]
            preview_surface = pygame.transform.scale_by(preview_surface,5)
            tower_rect = preview_surface.get_rect()
            tower_rect.midleft = (midleft_x, 350)
            scaledwindow.blit(preview_surface, tower_rect)
            midleft_x += 100
        #draw stats
        #draw total monsters killed from save
        kill_text = f'You have killed:\n{"{:,}".format(stats_from_session["monsterkills"])}\nmonsters'
        kill_text = kill_text.split("\n")
        line_1 = size32.render(kill_text[0], True, white)
        line_1_rect = line_1.get_rect(topleft=(20,10))
        scaledwindow.blit(line_1, line_1_rect)
        line_2 = size48.render(kill_text[1], True, white)
        line_2_rect = line_2.get_rect(topleft=(20,50))
        scaledwindow.blit(line_2, line_2_rect)
        line_3 = size32.render(kill_text[2], True, white)
        line_3_rect = line_3.get_rect(topleft=(20,110))
        scaledwindow.blit(line_3, line_3_rect)
        #draw total fans generated from save
        fans_text = f'You have generated:\n{"{:,}".format(stats_from_session["fansgenerated"])}\nfans'
        fans_text = fans_text.split("\n")
        line_1 = size32.render(fans_text[0], True, white)
        line_1_rect = line_1.get_rect(topleft=(600,10))
        scaledwindow.blit(line_1, line_1_rect)
        line_2 = size48.render(fans_text[1], True, white)
        line_2_rect = line_2.get_rect(topleft=(600,50))
        scaledwindow.blit(line_2, line_2_rect)
        line_3 = size32.render(fans_text[2], True, white)
        line_3_rect = line_3.get_rect(topleft=(600,110))
        scaledwindow.blit(line_3, line_3_rect)
        pygame.display.update()
        if click == 1:
            at_intermission = False
def level_manager(spawn_list,levelnum,new_level,available_towers):
    if new_level == True:
        level_file = f'save/level{levelnum}.txt'
        if not os.path.isfile(level_file):
            scaledwindow.fill((0, 0, 0))
            draw_front_and_centre_text("All Levels Finished", (255, 255, 255))
            pygame.display.update()
            time.sleep(1)
            running = False
            pygame.quit()
        else:
            file = open(level_file,'r')
            lines = file.read().splitlines()
            file.close()
            towers_from_file = lines[0].split(',')
            for tower in towers_from_file:
                match tower:
                    case "1":
                        available_towers.append(tambourine)
                    case "2":
                        available_towers.append(cd_player)
                    case "3":
                        available_towers.append(bassist)
            lines = lines[1:]
            for line in lines:
                splitline = line.split(',')
                monster_class = splitline[0]
                match monster_class:
                    case "1":
                        monster_class = RobZombie
                    case "2":
                        monster_class = Buckethead
                    case "3":
                        monster_class = IronMaiden
                zombie_timer = int(splitline[1])
                spawn_list.append([monster_class,zombie_timer])
def fan_manager(): #update fan count, as well as spawn new fan pickups
    global time_of_last_fan
    global time_of_next_fan
    global fancount
    icon_surf = assets.Images["fans"]["counter"]
    icon_surf = pygame.transform.scale_by(icon_surf,2)
    icon_rect = icon_surf.get_rect(topleft=(5,0))
    if time_of_last_fan == 0:
        time_of_last_fan = pygame.time.get_ticks()
        time_of_next_fan = time_of_last_fan + 6000
    if spawn_fan:
        if pygame.time.get_ticks() >= time_of_next_fan:
            projectiles.append(Sun([random.randint(40, 260),0], [0, 0.1]))
            time_of_last_fan = 0
    realwindow.blit(size23.render("{:,}".format(fancount), False, (255, 255, 255)), (45, 12))
    realwindow.blit(icon_surf, icon_rect)
def kill_tower(towervar):
    target_cords = [towervar.cords["x"], towervar.cords["y"]]
    global grid
    print(f'{towervar} killed')
    del towervar
    grid[target_cords[1]][target_cords[0]] = 0

def handle_monsters(): #update monsters (check for collision with towers or projectiles, update pos) and draw monsters
    global dead
    global grid
    global monsters
    global monster_lanes
    for index, monster in sorted(enumerate(monsters), reverse = True):
        monster.update(grid)
        monster_lanes[monster.lane] = [monster.cords["x"], monster.cords["y"]]
        monster.draw(realwindow)
        if monster.cords["x"] <= 85:
            dead = True
        for index2, projectile in sorted(enumerate(projectiles)):
            if isinstance(projectile, Bullet):
                if monster.rect().colliderect(projectile.get_rect()):
                    monster.ishit(projectile.damage)
                    projectiles.pop(index2)
                    if monster.totalhp <= 0:
                        stats_from_session['monsterkills'] += 1
                        monster_lanes[monster.lane] = 0
                        monsters.pop(index)
def failure(cur_level, dead):
    if dead == True:
        scaledwindow.fill(pygame.Color('black'))
        game_over_text = size48.render(f'You died on level {cur_level}!', True, (255, 255, 255))
        game_over_text_rect = game_over_text.get_rect(center = (scaledlength // 2, scaledheight // 2))
        scaledwindow.blit(game_over_text, game_over_text_rect)
        try_again_text = size32.render("To try the level again, close and re-open the game", True, (255, 255, 255))
        try_again_text_rect = try_again_text.get_rect(center = (scaledlength // 2, scaledheight // 2 + 100))
        scaledwindow.blit(try_again_text, try_again_text_rect)
        pygame.display.update()
def spawn_monsters(spawn_list):
    global is_newlevel
    global cur_level
    global at_intermission
    global level_total_zombies
    global monsters
    global last_spawn
    global next_spawn
    global spawn_index #changed variable that persists over runs
    global lastspawnedlane #changed variable that persists over runs
    lanes = [0,1,2,3,4]
    if spawn_index == 0:
        level_total_zombies = len(spawn_list)
    try:
        lanes.remove(lastspawnedlane)
    except:
        pass
    if spawn_index < level_total_zombies:
        spawn_id = spawn_list[0][0]
        spawn_cooldown = int(spawn_list[0][1])
        if last_spawn == 0:
            last_spawn = pygame.time.get_ticks()
            next_spawn = last_spawn + (1000*spawn_cooldown)
        if pygame.time.get_ticks() >= next_spawn:
            spawnlane = random.choice(lanes)
            lastspawnedlane = spawnlane
            monsters.append(spawn_id(spawnlane))
            last_spawn = 0
            (spawn_list.pop(0))
            spawn_index += 1
    else:
        if len(monsters) == 0:
            cur_level += 1
            stats_from_session['cur_level'] = cur_level
            with open('save/stats.txt', 'wb') as stats_file:
                pickle.dump(stats_from_session, stats_file)
            is_newlevel = True
            at_intermission = True
            available_towers = []
def closing(stats_from_session):
    global running
    scaledwindow.fill((0,0,0))
    draw_front_and_centre_text("Closing...", (255, 255, 255))
    pygame.display.update()
    with open('save/stats.txt', 'wb') as stats_file:
        pickle.dump(stats_from_session, stats_file)
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

def get_pos(isscaled, mouse_pos): #get mouse_pos in terms of the 320x180 grid or the full scaled screen
    result = 0
    if isscaled == 1:
        result = (mouse_pos[0]*(320/scaledlength), mouse_pos[1]*(180/scaledheight))
    else:
        result = mouse_pos
    return(result)
def get_scalefactor(): #get scale factor of current display size compared to 320/180
    result = scaledheight/realheight
    return(result)
def check_tomato(): #handle whether or not the user wishes to tomato a band member
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
    if tomato_mask.overlap(cursor_mask, (get_pos(1, mouse_pos)[0] - tomato_rect_unscaled.x, get_pos(1, mouse_pos)[1] - tomato_rect_unscaled.y)):
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
def check_towerselection(fancount): #draw the buttons for each tower on screen, and check if the player has one selected
    y = 0
    global current_tower
    global towerselection_size
    global towerselection_scalingdirection
    button_rect = 0
    for towertype in available_towers:
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
        if button_rect.collidepoint(get_pos(1, mouse_pos)[0], get_pos(1, mouse_pos)[1]):
            hovered = True
        if hovered == True:
            if current_tower != towertype:
                button_surf.set_alpha(255)
                button_surf = pygame.transform.scale_by(button_surf, towerselection_size)
                if towerselection_size >= 1.1:
                    towerselection_scalingdirection = -1
                if towerselection_size < 1.1 and towerselection_scalingdirection == 1:
                    towerselection_size += 0.005
                if towerselection_scalingdirection == -1:
                    towerselection_size -= 0.005
                if towerselection_size <= 1:
                    towerselection_scalingdirection = 1
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
def update_grid(gridvar, projectiles, click): #check for updates on towers (the drawing of towers is included in this section of runtime)
    global monster_lanes #global as many functions use this same variable
    global is_tomatoing #updated in another function before being used
    global fancount #must get changed in multiple functions
    hovered = False
    y = 0
    for row in gridvar:
        x = 0
        for tile in row:
            cords = {"x":x,"y":y}
            tile_surf = pygame.Surface.copy(assets.Images["tiles"]["wood"])
            tile_rect = tile_surf.get_rect(topleft=(((x*24) + 100),((y*24) + 30)))
            if tile_rect.collidepoint(get_pos(1, mouse_pos)[0], get_pos(1, mouse_pos)[1]):
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
                            reset_towerselection()
            hovered = False
            x += 1
        y += 1
def handle_projectiles(projectiles):
    for i, projectile in sorted(enumerate(projectiles), reverse=True):
        kill_bullet = False
        projectile.update()
        projectile.draw(realwindow)
        if isinstance(projectile,Bullet):
            if projectile.range != 0:
                if projectile.distance_moved >= projectile.range * 24:
                    kill_bullet = True
        if projectile.cur_cords[0] > 352 or -32 > projectile.cur_cords[1]:
            kill_bullet = True
        if kill_bullet:
            projectiles.pop(i)
def fan_collection(projectiles):
    global fancount
    global current_tower
    for i, projectile in sorted(enumerate(projectiles), reverse=True):
        if isinstance(projectile, Sun):
            if projectile.rect().collidepoint(get_pos(1, mouse_pos)) and click == 1:
                current_tower = 0
                fancount += projectile.value
                stats_from_session['fansgenerated'] += projectile.value
                projectiles.pop(i)
running = True
while running == True:
    click = 0
    deltatime = clock.tick(60)
    save_handler()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closing(stats_from_session)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dospawn = 1
            elif event.key == pygame.K_r:
                reset_grid()
            elif event.key == pygame.K_1:
                if current_tower == available_towers[0]:
                    reset_towerselection()
                else:
                    if available_towers[0].cost > fancount:
                        show_notenoughfans()
                    else:
                        current_tower = available_towers[0]
            elif event.key == pygame.K_2:
                try:
                    if current_tower == available_towers[1]:
                        reset_towerselection()
                    else:
                        if available_towers[1].cost > fancount:
                            show_notenoughfans()
                        else:
                            current_tower = available_towers[1]
                except:
                    pass
            elif event.key == pygame.K_3:
                try:
                    if current_tower == available_towers[2]:
                        reset_towerselection()
                    else:
                        if available_towers[2].cost > fancount:
                            show_notenoughfans()
                        else:
                            current_tower = available_towers[2]
                except:
                    pass
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = 1
    level_manager(spawn_list, cur_level, is_newlevel, available_towers)
    is_newlevel = False
    intermission(cur_level, available_towers, stats_from_session)
    start_menu(stats_from_session)
    if not at_menu and not at_intermission:
        spawn_monsters(spawn_list)
        realwindow.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()
    if not at_menu and not at_intermission:
        check_towerselection(fancount)
        fan_collection(projectiles)
        update_grid(grid,projectiles,click)
        handle_projectiles(projectiles)
        fan_manager()
        handle_monsters()
        newwindow = pygame.transform.scale(realwindow,(scaledlength,scaledheight))
        scaledwindow.blit(newwindow, position) #draw the new upscaled onto scaled window
        if endframetext != "" and endframetextduration > 0:
            draw_front_and_centre_text(endframetext,endframetextcolour)
            endframetextduration -= 1
        check_tomato()
        failure(cur_level,dead)
        pygame.display.update() #update what is seen