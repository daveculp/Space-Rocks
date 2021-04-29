import pygame
import math
import sys
import time
import random

def clamp(n, min_n, max_n):
	if n < min_n:
		return min_n
	elif n > max_n:
		return max_n
	else:
		return n
		
def distance(x1,y1,x2,y2):
	x_term = (x2-x1)**2
	y_term = (y2-y1)**2
	return math.sqrt(x_term + y_term)
	
def vector_mag(vec_1, vec_2):
	return math.sqrt( (vec_1)**2 + (vec_2)**2) 
	
def check_pygame_events():
	global game_state
	
	keys = pygame.key.get_pressed()
	event = pygame.event.poll()
	
	if event.type == pygame.QUIT:
		game_state = GAME_STATE_QUIT
		
	if keys[pygame.K_ESCAPE]:
		game_state = GAME_STATE_QUIT
		
def draw_scene():
	#draw a black rectangle
	rect = pygame.Rect(0,0, SCREEN_WIDTH, 31)
	pygame.rect.draw(screen, BLACK, rect)
	
def title_screen():
	pass
	
def game_paused():
	pass

#=======================================================================
#							GAME SETUP AND VARIABLES				   =
#=======================================================================

#setup colors
BROWN = 193,154,107
BLACK = 0,0,0
RED = 255,0,0
GREEN = 0,255,0
BLUE = 0,0,255
WHITE = 255,255,255

#setup our screen
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900

#Init pygame and set up the drawing window
#pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init()
pygame.key.set_repeat(1,1)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)
#font = pygame.font.Font("./zorque.ttf", 28, bold=True)
screen = pygame.display.set_mode( [SCREEN_WIDTH, SCREEN_HEIGHT])

#init the joysticks
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()

if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    name = joystick.get_name()
    print("Joystick name: {} initialized".format(name))	


#setup player/ship variables and information

#current_ship_img = ship_img_no_thrust
#ship_rect = ship_img_no_thrust.get_rect(topleft=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
ship_angle = 0
ship_delta_x = 0
ship_delta_y = 0
ship_friction = .98
ship_accel = 1.001
ship_energy = 100
num_smart_bombs = 1
last_smart_bomb_time = time.time()
game_score = 0

#missile related variables and constants
missile_list = []
shot_time = .25  #time between sucessive shots
last_shot_time = time.time()
MISSILE_DX = 0
MISSILE_DY = 1
MISSILE_RECT = 2

#Asteroid related variables and constants
asteroid_list = []
AST_DX = 0
AST_DY = 1
AST_RECT = 2
AST_SIZE = 3
AST_ROT_ANGLE = 4
AST_ROT_SPEED = 5

AST_LARGE = 2
AST_MED = 1
AST_SMALL = 0

#constants to track game state
GAME_STATE_TITLE = 0
GAME_STATE_RUNNING = 1
GAME_STATE_END = 2
GAME_STATE_PAUSED = 3
GAME_STATE_QUIT = 4
GAME_STATE_GAME_OVER = 5
GAME_STATE_LEVEL_OVER = 6
game_state = GAME_STATE_TITLE #set initial game state
game_level = 1

#explosions:
explosion_list = []
EXP_IMAGE = 0
EXP_RECT = 1
EXP_DX = 2
EXP_DY = 3
EXP_FRAME = 4
EXP_LAST_TIME = 5
EXP_SIZE = 6

EXP_SMALL = AST_SMALL
EXP_MED = AST_MED
EXP_LARGE = AST_LARGE

	
#=======================================================================
#							MAIN GAME LOOP							   =
#=======================================================================

while game_state != GAME_STATE_QUIT:
	check_pygame_events()
	if game_state == GAME_STATE_RUNNING:
		draw_scene()
		pygame.display.update()
	
	elif game_state == GAME_STATE_TITLE:
		title_screen()
		pygame.display.update()
	elif game_state == GAME_STATE_PAUSED:
		game_paused()
	clock.tick(30)

print("Thanks for playing!!")
pygame.quit()
sys.exit()
	
	


