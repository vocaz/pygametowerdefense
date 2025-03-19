import pygame
import gc
from pygame.locals import *
from towers import *
pygame.init()
current_tower = 1
reallength = 320
realheight = 180
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
testRed({"x":2,"y":3})
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
    button_rect = 0
    for towertype in fetch_alltowertypes():
        button_surf = pygame.Surface((48,30))
        if button_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            hovered = true
        button_rect = pygame.Rect(20, (y*20), 48,30)
        colour = towertype.colour
        pygame.draw.rect(button_surf,colour,button_rect)
        realwindow.blit(button_surf,(48,30))
        y += 1
def update_grid(gridvar):
    y = 0
    for row in gridvar:
        hovered = False
        x = 0
        for tile in row:
            tile_rect = pygame.Rect((x*24) + 52, (y*24) + 46, 24, 24)
            if tile_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                hovered = True
            if tile == 0:
                if hovered == True:
                    pygame.draw.rect(realwindow,(150,150,150),tile_rect)
                else:
                    pygame.draw.rect(realwindow,white,tile_rect)
            if tile == 1:
                if hovered == True:
                    pygame.draw.rect(realwindow,darken_colour(red),tile_rect)
                else:
                    pygame.draw.rect(realwindow,red,tile_rect)
            if tile == 2:
                if hovered == True:
                    pygame.draw.rect(realwindow,darken_colour(green),tile_rect)
                else:
                    pygame.draw.rect(realwindow,green,tile_rect)
            if tile == 3:
                if hovered == True:
                    pygame.draw.rect(realwindow,darken_colour(blue),tile_rect)
                else:
                    pygame.draw.rect(realwindow,blue,tile_rect)
            if hovered == True:
                if pygame.mouse.get_pressed()[0]:
                    grid[y][x] = current_tower
            hovered = False
            x += 1
        y += 1
    for i in range(6):
        pygame.draw.line(realwindow,(0,0,0),(52,i*24 + 46),(24*9 + 52,i*24 + 46))
    for i in range(10):
        pygame.draw.line(realwindow,(0,0,0),(i*24 + 52,46),(i*24 + 52,5*24 + 46))

running = True
while running == True:
    realwindow.fill((255,255,255))
    check_towerselection()
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = (mouse_pos[0]*(320/scaledlength), mouse_pos[1]*(180/scaledheight))
    update_grid(grid)
    scaledwindow.blit(pygame.transform.scale(realwindow, (scaledlength,scaledheight)), position)
    pygame.display.update()
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
                print_grid(grid)
            elif event.key == pygame.K_r:
                grid = reset_grid()
                print_grid(grid)
            elif event.key == pygame.K_1:
                current_tower = 1
            elif event.key == pygame.K_2:
                current_tower = 2
            elif event.key == pygame.K_3:
                current_tower = 3
pygame.quit()