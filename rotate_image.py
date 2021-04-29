import pygame
import math
import sys
import time 

def check_pygame_events():
    global ship_angle, ship_delta_x, ship_delta_y, game_state
    
    keys = pygame.key.get_pressed()
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
                
    if keys[pygame.K_SPACE] and game_state== GAME_STATE_RUNNING:
        spawn_missile()
    if keys[pygame.K_SPACE] and game_state== GAME_STATE_TITLE:
        game_state = GAME_STATE_RUNNING
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
        ship_delta_x += math.cos(math.radians(ship_angle))*ship_accel
        ship_delta_y += - (math.sin(math.radians(ship_angle)))*ship_accel
    return      
    
def rot_center(image, rect, ship_angle):
    """rotate an image while keeping its center"""
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
    global shipRect, newshipImg, missilelist
    
    #move player
    shipRect.centerx += int(ship_delta_x)
    shipRect.centery += int(ship_delta_y)
    newshipImg,shipRect = rot_center(shipImg, shipRect, ship_angle)
    
    #move missiles
    for missile in missile_list:
        x = missile[0]
        y = missile[1]
        delta_x = missile[2]
        delta_y = missile[3]
        missile[0] += delta_x
        missile[1] += delta_y
    return
    
def check_bounds():
    global ship_delta_x, ship_delta_y, missile_list
    
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
       
    print (len(missile_list) )
    for missile in missile_list:
        if missile[0] <0 or missile[0]>SCREEN_WIDTH:
            missile_list.remove(missile)
        if missile[1] < 0 or missile[1] > SCREEN_HEIGHT:
            missile_list.remove(missile)
            
        
   
def draw_scene():
    screen.fill( (0,0,0) )
    
    for missile in missile_list:
        x = missile[0]
        y = missile[1]
        pygame.draw.circle( screen, (255,255,255) , ( int(missile[0]),int(missile[1]) ),1)

    screen.blit(newshipImg,shipRect)
    return

def title_screen():

    screen.blit(title_image, (0,0))

    
# Init pygame and set up the drawing window
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

#setup player/ship variables and information
shipImg = pygame.image.load('spaceship3.png')
shipRect = shipImg.get_rect(topleft=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
ship_angle=0
ship_delta_x = 0
ship_delta_y = 0
ship_friction = .98
ship_accel = 1.001

#missile information
missile_list = []

shot_time = .3
last_shot_time = time.time()

title_image = pygame.image.load('asteroidback.png')

#constants to track game state
GAME_STATE_TITLE = 0
GAME_STATE_RUNNING = 1
GAME_STATE_WON = 2


game_state = GAME_STATE_TITLE

while True:
    check_pygame_events()
    if game_state == GAME_STATE_RUNNING:
        move_objects()
        decelerate_player()
        check_bounds()
        draw_scene()
    elif game_state == GAME_STATE_TITLE:
        title_screen()
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()
quit()

