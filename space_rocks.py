import pygame
import math
import sys
import time 
import random 

def distance(x1,y1,x2,y2):
    return math.sqrt( (x2-x1)**2 + (y2-y1)**2 )
  
def detect_collisions(): 
    global player_score, missile_list, asteroid_list, player_lives

    new_asteroids = []
    
    for missile in reversed(missile_list):
        for asteroid in reversed(asteroid_list):
            dist = distance(missile[X],missile[Y],asteroid[X],asteroid[Y])
            if dist < asteroid[SIZE]:
                player_score += asteroid[SIZE]*5
                bang_large.play()
                if missile in missile_list:
                    missile_list.remove(missile)
                if asteroid in asteroid_list:
                    asteroid_list.remove(asteroid)
                if asteroid[SIZE] == ASTEROID_SMALL:
                    break
                for i in range( asteroid[SIZE]//16 + 1):
                    x = asteroid[X] + random.randint(-10,10)
                    y = asteroid[Y] + random.randint(-10,10)
                    delta_x = asteroid[DELTA_X] * random.uniform(-2,2)
                    delta_y = asteroid[DELTA_Y] * random.uniform(-2,2)
                    red = random.randint(0,255)
                    green = random.randint(0,255)
                    blue = random.randint(0,255)
                    if asteroid[SIZE] == 64:
                        size = 16
                    else:
                        size = 8
                    new_asteroid = [x,y,delta_x,delta_y, [red,green,blue], size]
                    new_asteroids.append(new_asteroid)
                break
    
    #check for asteroid collisions with the players ship 
    for asteroid in asteroid_list:
        left = int(asteroid[X])- asteroid[SIZE]
        top = int(asteroid[Y]) + asteroid[SIZE]
        width = height = asteroid[SIZE]*2
        asteroid_rect = pygame.Rect(left,top,width,height)
        if shipRect.colliderect(asteroid_rect):
            #player_lives -= 1
            pass
    #add the new asteroids in to the asteroid list
    for asteroid in new_asteroids:
        asteroid_list.append(asteroid)
    return
    
def spawn_random_asteroid():
    global asteroid_list
    
    red = random.randint(0,255)
    green = random.randint(0,255)
    blue = random.randint(0,255)
    trans = random.randint(75,200)
    
    size = random.randint(0,2)
    x = shipRect.centerx
    y = shipRect.centery
    
    while distance(x,y,shipRect.centerx, shipRect.centery) < 200:
        x = random.randint(64,SCREEN_WIDTH-64)
        y = random.randint(64,SCREEN_HEIGHT-64)
        
    delta_x = delta_y = 0
    while delta_x == 0 and delta_y == 0:
        delta_x = random.randint(-3,3)
        delta_y = random.randint(-3,3)
    asteroid = [x,y,delta_x,delta_y, [red,green,blue, trans], ASTEROID_SIZES[size]]
    asteroid_list.append(asteroid)
    
def check_pygame_events():
    global ship_angle, ship_delta_x, ship_delta_y, game_state
    
    keys = pygame.key.get_pressed()
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        game_state = GAME_STATE_QUIT
                
    if keys[pygame.K_SPACE] and game_state == GAME_STATE_RUNNING:
        fire_sound.play()
        spawn_missile()
    if keys[pygame.K_p] and game_state == GAME_STATE_RUNNING:
        game_state = GAME_STATE_PAUSED
    if keys[pygame.K_SPACE] and game_state == GAME_STATE_TITLE:
        game_state = GAME_STATE_RUNNING
        reset_game()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
    if keys[pygame.K_LEFT]:
        ship_angle += 5
    if keys[pygame.K_RIGHT]:
        ship_angle -= 5
    if keys[pygame.K_DOWN]:
        ship_delta_x -= math.cos(math.radians(ship_angle))*ship_accel
        ship_delta_y -= - (math.sin(math.radians(ship_angle)))*ship_accel
    if keys[pygame.K_UP]:
        thrust_sound.play()
        ship_delta_x += math.cos(math.radians(ship_angle))*ship_accel
        ship_delta_y += - (math.sin(math.radians(ship_angle)))*ship_accel
    return      
    
def rot_center(image, rect, ship_angle):
    rot_image = pygame.transform.rotate(image, ship_angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image,rot_rect

def spawn_missile():
    global last_shot_time, missile_list
    
    if time.time() - last_shot_time < shot_time:
        return
        
    last_shot_time = time.time()
    rect = shipRect
    x = rect.centerx + math.cos(math.radians(ship_angle))
    y = rect.centery + (-math.sin(math.radians(ship_angle)))
    delta_x = math.cos(math.radians(ship_angle))*4 + ship_delta_x
    delta_y = -(math.sin(math.radians(ship_angle))*4) + ship_delta_y
    
    missile = [x,y,delta_x,delta_y]
    missile_list.append(missile)
    
def decelerate_player():
    global ship_delta_x, ship_delta_y
    
    if ship_delta_x != 0:   
        ship_delta_x *= ship_friction

    if ship_delta_y !=0:  
        ship_delta_y *= ship_friction
    return
    
def move_objects():
    global shipRect, newshipImg, missilelist, asteroid_list
    
    #move player
    shipRect.centerx += int(ship_delta_x)
    shipRect.centery += int(ship_delta_y)
    newshipImg,shipRect = rot_center(shipImg, shipRect, ship_angle)
    
    #move missiles
    for missile in missile_list:
        missile[X] += missile[DELTA_X]
        missile[Y] += missile[DELTA_Y]
        
    for asteroid in asteroid_list:
        asteroid[X] = asteroid[X] + asteroid[DELTA_X]
        asteroid[Y] = asteroid[Y] + asteroid[DELTA_Y]
        
    return
    
    
def check_bounds():
    global ship_delta_x, ship_delta_y, missile_list, asteroid_list
    global missile_remove
    global missile_remove
    
    if shipRect.top <0:
        shipRect.top = 1
        ship_delta_y = -(ship_delta_y)
        
    if shipRect.bottom > SCREEN_HEIGHT:
        shipRect.bottom = SCREEN_HEIGHT-1
        ship_delta_y = -(ship_delta_y)
        
    if shipRect.left < 0:
        shipRect.left = 0
        ship_delta_x = -(ship_delta_x)
    
    if shipRect.right > SCREEN_WIDTH:
        shipRect.right = SCREEN_WIDTH-1
        ship_delta_x = -(ship_delta_x)
    
    #missile_copy = copy.deepcopy(missile_list)
       
    for missile in missile_list:
        if missile[X] <0 or missile[X]>SCREEN_WIDTH or missile[Y] < 0 or missile[Y] > SCREEN_HEIGHT:
            missile_list.remove(missile)
            
    for asteroid in asteroid_list:
        if asteroid[X] < asteroid[SIZE] or asteroid[X] > SCREEN_WIDTH-asteroid[SIZE]:
            asteroid[DELTA_X] = -asteroid[DELTA_X]
        if asteroid[Y] < asteroid[SIZE] or asteroid[Y] > SCREEN_HEIGHT-asteroid[SIZE] :
            asteroid[DELTA_Y] = -asteroid[DELTA_Y]
   
def draw_scene():
    screen.fill( (0,0,0,128) )
    
    screen.blit(background_image,(0,0) )
    score_text = font.render("SCORE: "+str(player_score), 1, GREEN)
    screen.blit(score_text,(0, 5))

    for asteroid in asteroid_list:
        pygame.draw.circle(screen, asteroid[COLOR], (int(asteroid[X]), int(asteroid[Y])), asteroid[SIZE], 0)
    
    for missile in missile_list:
        x = missile[X]
        y = missile[Y]
        pygame.draw.circle( screen, (255,255,255) , ( int(missile[X]),int(missile[Y]) ),1)

    screen.blit(newshipImg,shipRect)
    
    left = player_lives*32
    for x in range(player_lives):
        rect = (SCREEN_WIDTH-left+(x*32),10,32,32)
        screen.blit(shipImg, rect)
        
    return
    
def reset_game():
    global player_score
    
    player_score = 0
    
    for x in range(20):
        spawn_random_asteroid()
    pygame.mixer.music.play(-1)
    time.sleep(1)

def check_extra_life():
    global extra_life_score, player_lives
    
    if player_score > extra_life_score and player_score< max_lives_score:
        extra_ship_sound.play()
        player_lives += 1
        extra_life_score = extra_life_score + 1000

def game_paused():
    global game_state
    pygame.mixer.pause()
    pygame.mixer.music.pause()
    while game_state == GAME_STATE_PAUSED:
        keys = pygame.key.get_pressed()
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_u] and game_state == GAME_STATE_PAUSED:
            game_state = GAME_STATE_RUNNING
            pygame.mixer.unpause()
            pygame.mixer.music.unpause()

            
    return
        
def title_screen():

    screen.blit(title_image, (0,0))

#======================================================================#
#                        GAME SETUP AND VARIABLES                      #
#======================================================================#
 
#setup colors
BROWN = 193,154,107
BLACK = 0,0,0
RED = 255,0,0
GREEN = 0,255,0
BLUE = 0,0,255
WHITE = 255,255,255

# Init pygame and set up the drawing window
pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.SRCALPHA, 32)

#setup player/ship variables and information
shipImg = pygame.image.load('spaceship5.png')
shipRect = shipImg.get_rect(topleft=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
ship_angle = 0
ship_delta_x = 0
ship_delta_y = 0
ship_friction = .98
ship_accel = 1.001

#score variables
player_score = 0
player_lives = 3
extra_life_score = 1000
max_lives_score = 3000

#missile information
missile_list = []
shot_time = .1  #time between sucessive shots
last_shot_time = time.time()

#Asteroid related variables
asteroid_list = []
X = 0
Y = 1
DELTA_X = 2
DELTA_Y = 3
COLOR = 4
SIZE = 5

ASTEROID_LARGE = 64
ASTEROID_MED = 16
ASTEROID_SMALL = 8
ASTEROID_SIZES =[ASTEROID_SMALL, ASTEROID_MED, ASTEROID_LARGE]

#constants to track game state
GAME_STATE_TITLE = 0
GAME_STATE_RUNNING = 1
GAME_STATE_END = 2
GAME_STATE_PAUSED = 3
GAME_STATE_QUIT = 4
game_state = GAME_STATE_TITLE #set initial game state

#LOAD GAME SOUNDS AND GRAPHICS
title_image = pygame.image.load('asteroidback.png')
background_image = pygame.image.load('background2.png')
fire_sound = pygame.mixer.Sound("fire.wav")
fire_sound.set_volume(.2)
bang_small = pygame.mixer.Sound("bangSmall.wav")
bang_med = pygame.mixer.Sound("bangMedium.wav")
thrust_sound = pygame.mixer.Sound("thrust.wav")
thrust_sound.set_volume(1)
bang_large = pygame.mixer.Sound("bangLarge.wav")
extra_ship_sound = pygame.mixer.Sound("extraShip.wav")
game_music = pygame.mixer.music.load('music.wav')
asteroid_small_image = pygame.image.load("asteroid_small.png")
asteroid_medium_image = pygame.image.load("asteroid_medium.png")
asteroid_large_image = pygame.image.load("asteroid_large.png")
#======================================================================#
#                        MAIN GAME LOOP                                #
#======================================================================#
while game_state != GAME_STATE_QUIT:
    check_pygame_events()
    if game_state == GAME_STATE_RUNNING:
        move_objects()
        check_bounds()        
        detect_collisions()
        decelerate_player()
        check_extra_life()
        draw_scene()
    elif game_state == GAME_STATE_TITLE:
        title_screen()
    elif game_state == GAME_STATE_PAUSED:
        game_paused()
    pygame.display.update()
    clock.tick(30)

print("Thanks for playing!")
pygame.quit()
sys.exit()

