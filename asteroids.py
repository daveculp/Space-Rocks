import pygame
import random
import time
import math
import sys


def distance(x1,y1,x2,y2):
    return math.sqrt( (x2-x1)**2 + (y2-y1)**2 )

def check_pygame_events():
    keys = pygame.key.get_pressed()
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

def draw_screen():
    screen.fill( BLACK ) #paint the background in black

    score_text = font.render("SCORE: "+str(player_score), 1, GREEN)
    screen.blit(score_text,(0, 5))

    for asteroid in asteroid_list:
        pygame.draw.circle(screen, asteroid[COLOR], (asteroid[X], asteroid[Y]), asteroid[SIZE], 0)

def move_objects():
    global asteroid_list
    for asteroid in asteroid_list:
        asteroid[X] = asteroid[X]+asteroid[DELTA_X]
        asteroid[Y] = asteroid[Y]+asteroid[DELTA_Y]
  
def check_bounds():
    global asteroid_list
    
    for asteroid in asteroid_list:
        if asteroid[X] < asteroid[SIZE] or asteroid[X] > SCREEN_WIDTH-asteroid[SIZE]:
            asteroid[DELTA_X] = -asteroid[DELTA_X]
        if asteroid[Y] < asteroid[SIZE] or asteroid[Y] > SCREEN_HEIGHT-asteroid[SIZE] :
            asteroid[DELTA_Y] = -asteroid[DELTA_Y]
            
def spawn_asteroid():
    global asteroid_list
    
    red = random.randint(0,255)
    green = random.randint(0,255)
    blue = random.randint(0,255)
    size = random.randint(0,2)
    x=SCREEN_WIDTH//2
    y=SCREEN_HEIGHT//2
    
    while distance(x,y,SCREEN_WIDTH//2, SCREEN_HEIGHT//2) < 200:
        x = random.randint(100,SCREEN_WIDTH-100)
        y = random.randint(100,SCREEN_HEIGHT-100)
        
    delta_x = delta_y = 0
    while delta_x == 0 and delta_y==0:
        delta_x = random.randint(-3,3)
        delta_y = random.randint(-3,3)
    
    asteroid = [x,y,delta_x,delta_y, [red,green,blue], ASTEROID_SIZES[size]]
    asteroid_list.append(asteroid)


#===============================================================================
#                       Gloabls and Constants area                             =
#===============================================================================
#Our screen width and height
SCREEN_WIDTH = 800 
SCREEN_HEIGHT= 800

#setup colors
BROWN = 193,154,107
BLACK = 0,0,0
RED = 255,0,0
GREEN = 0,255,0
BLUE = 0,0,255
WHITE = 255,255,255

GAME_STATE_TITLE = 0
GAME_STATE_RUNNING = 1
GAME_STATE_WON = 2

asteroid_list = []
X = 0
Y = 1
DELTA_X = 2
DELTA_Y = 3
COLOR = 4
SIZE = 5

ASTEROID_SIZES =[8,16,64]


game_state = GAME_STATE_RUNNING
player_score = 0
#===============================================================================
#                       Initilizations area                                   =
#===============================================================================

pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init()
screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF )
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()

#setup our font
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 136)


for x in range(20):
    spawn_asteroid()
time.sleep(3)

#===============================================================================
#                       Main Game Loop                                         =
#===============================================================================
while True:
    check_pygame_events()
    if game_state == GAME_STATE_RUNNING:
        move_objects()
        check_bounds()
        draw_screen()
    elif game_state == GAME_STATE_TITLE:
        pass
    elif game_state == GAME_STATE_WON:
        pass

    pygame.display.flip()
    clock.tick(30) 