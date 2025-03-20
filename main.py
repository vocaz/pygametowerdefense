import pygame
import gc
from pygame.locals import *
from towers import *
click = 0
pygame.init()
size = 1
scalingdirection = 1
clock = pygame.time.Clock()
current_tower = 1
reallength = 320
realheight = 180
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
scaledlength = 960
scaledheight = 540
scaledwindow = pygame.display.set_mode((scaledlength,scaledheight))
realwindow = pygame.Surface((reallength,realheight))
font = pygame.font.Font(None,40)
grid = [[0,0,0,0,0,0,0,0,0],
        [0,2,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]
position = (0,0)
def fetch_alltowertypes():
    result = (Tower.__subclasses__())
    return(result)
def darken_colour(ogcolour):
    darkenedcolour = list(ogcolour)
    for i in range (0,3):
        darkenedcolour[i] = darkenedcolour[i]/2
    darkenedcolour = tuple(darkenedcolour)
    return(darkenedcolour)

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
        if button_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            hovered = True
        if hovered == True:
            button_surf.set_alpha(128)
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
                print(current_tower)
        else:
            button_surf.set_alpha(255)
        realwindow.blit(button_surf,button_rect)
        y += 1
def update_grid(gridvar):
    y = 0
    for row in gridvar:
        hovered = False
        x = 0
        for tile in row:
            cords = {"x":x,"y":y}
            tile_rect = pygame.Rect((x*24) + 100, (y*24) + 30, 24, 24)
            if tile_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                hovered = True
            if tile == 0:
                if hovered == True:
                    pygame.draw.rect(realwindow,(150,150,150),tile_rect)
                else:
                    pygame.draw.rect(realwindow,white,tile_rect)
            if isinstance(tile,Tower):
                if hovered == True:
                    pygame.draw.rect(realwindow,darken_colour(tile.colour),tile_rect)
                else:
                    pygame.draw.rect(realwindow,tile.colour,tile_rect)
            if hovered == True:
                if click == 1:
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
    click = 0
    deltatime = clock.tick(60)
    realwindow.fill((255,255,255))
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = (mouse_pos[0]*(320/scaledlength), mouse_pos[1]*(180/scaledheight))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            realwindow.fill((0,0,0))
            closing_text = font.render("goodbye", True, (0,255,0))
            closing_text_rect = closing_text.get_rect()
            closing_text_rect.center = (reallength // 2, realheight // 2)
            realwindow.blit(closing_text, closing_text_rect)
            scaledwindow.blit(pygame.transform.scale(realwindow, (scaledlength,scaledheight)), position)
            pygame.display.update()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print(Tower.instances)
            elif event.key == pygame.K_r:
                grid = reset_grid()
                print_grid(grid)
            elif event.key == pygame.K_1:
                current_tower = testRed
            elif event.key == pygame.K_2:
                current_tower = testGreen
            elif event.key == pygame.K_3:
                current_tower = 3
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = 1    
    check_towerselection()
    update_grid(grid)
    scaledwindow.blit(pygame.transform.scale(realwindow, (scaledlength,scaledheight)), position)
    pygame.display.update()
pygame.quit()
