import pygame
import math
import sys
import time 
import random 

def clamp(n, minn, maxn):
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n
    
def distance(x1,y1,x2,y2):
    return math.sqrt( (x2-x1)**2 + (y2-y1)**2 )
    
def vector_mag(vec_1, vec_2):
    return math.sqrt( (vec_1)**2 + (vec_2)**2 )
  
def detect_collisions(): 
    global game_score, missile_list, asteroid_list, player_lives
    global ship_energy

    new_asteroids = []  # list to keep new asteroids in
    
    # DETECT COLLSIONS BETWEEN MISSILE AND ASTEROID
    for missile in reversed(missile_list):
        for asteroid in reversed(asteroid_list):
            left_rect = missile[MISSILE_RECT]
            right_rect = asteroid[AST_RECT].inflate(-5,-5)
            if left_rect.colliderect(right_rect) == True:
                game_score += asteroid[AST_RECT].width*2
                x = asteroid[AST_RECT].left
                y = asteroid[AST_RECT].top
                delta_x = asteroid[AST_DX]
                delta_y = asteroid[AST_DY]
                spawn_explosion( x, y, delta_x, delta_y, asteroid[AST_SIZE])
                
                #now remove the asteroid and missile from the lists
                missile_list.remove(missile)
                asteroid_list.remove(asteroid)
                    
                if asteroid[AST_SIZE] == AST_SMALL:
                    bang_small.play()
                    break #we dont need to do anything more with a small asteroid
                bang_large.play()
                
                if asteroid[AST_SIZE] == AST_MED:
                    spawn_num = random.randint(0,2)
                else:
                    spawn_num = random.randint(0,4)
                #spawn_num = asteroid[AST_SIZE] * 2 #the number of new asteroids to spawn from this astroid+
                
                #now spawn new asteroids in place of the destroyed asteroid
                for i in range(spawn_num):
                    #get an x and y near the center of the destroyed asteroid
                    x = asteroid[AST_RECT].x + random.randint(-10,10)
                    y = asteroid[AST_RECT].y + random.randint(-10,10)
                    #get a random x and y speed for the new roid
                    delta_x = delta_y = 0
                    while delta_x == 0 or delta_y == 0: # we dont want a stationary asteroid
                        delta_x = asteroid[AST_DX] + random.randint(-4,4)
                        delta_y = asteroid[AST_DY] + random.randint(-4,4)
                        
                    if asteroid[AST_SIZE] == AST_LARGE:
                        size = AST_MED
                        width = asteroid_medium_image.get_width()
                        height = asteroid_medium_image.get_height()
                    else:
                        size = AST_SMALL
                        width = asteroid_small_image.get_width()
                        height = asteroid_small_image.get_height() 
                                             
                    rect = pygame.Rect(x,y, width,height) 
                    new_asteroid = [delta_x,delta_y, rect, size]
                    new_asteroids.append(new_asteroid)
                break
    
    #check for asteroid collisions with the players ship 
    left_rect = ship_rect.inflate(-10,-10)
    for asteroid in reversed(asteroid_list):
        right_rect = asteroid[AST_RECT].inflate(-10,-10)
        if left_rect.colliderect(right_rect):
            bang_large.play()
            magnitude = vector_mag(asteroid[AST_DX], asteroid[AST_DY]) + \
            vector_mag(ship_delta_x, ship_delta_y)
            damage = asteroid[AST_RECT].width//16 * magnitude
            ship_energy -= int(damage)
            if ship_energy < 0:
                ship_energy = 0
            x = asteroid[AST_RECT].x
            y = asteroid[AST_RECT].y
            delta_x = asteroid[AST_DX]
            delta_y = asteroid[AST_DY]
            spawn_explosion( x, y, delta_x, delta_y, asteroid[AST_SIZE])
            asteroid_list.remove(asteroid)

    #add the new asteroids in to the asteroid list
    for asteroid in new_asteroids:
        asteroid_list.append(asteroid)
    return
    
def do_smart_bomb():
    global game_score, missile_list, asteroid_list, player_lives, last_smart_bomb_time
    global num_smart_bombs
    
    if  time.time() - last_smart_bomb_time < 1 or num_smart_bombs < 1:
        return
    
    num_smart_bombs -= 1
    last_smart_bomb_time = time.time()
    new_asteroids = []
    print("Smart bomb!")
    for asteroid in reversed(asteroid_list):
        game_score += asteroid[AST_RECT].width*2
            
        #now remove the asteroid from the lists
        asteroid_list.remove(asteroid)
        #spawn an explosion
        x = asteroid[AST_RECT].x
        y = asteroid[AST_RECT].y
        delta_x = asteroid[AST_DX]
        delta_y = asteroid[AST_DY]
        spawn_explosion( x, y, delta_x, delta_y, asteroid[AST_SIZE])
        if asteroid[AST_SIZE] == AST_SMALL:
            bang_small.play()
            continue #we dont need to do anything more with a small asteroid
            
        bang_large.play()
        if asteroid[AST_SIZE] == AST_MED:
            spawn_num = random.randint(0,2)
        else:
            spawn_num = random.randint(0,4)        
        #spawn_num = asteroid[AST_SIZE] * 2 #the number of new asteroids to spawn from this astroid+
        
        #now spawn new asteroids in place of the destroyed asteroid
        for i in range(spawn_num):
            #get an x and y near the center of the destroyed asteroid
            x = asteroid[AST_RECT].x + random.randint(-10,10)
            y = asteroid[AST_RECT].y + random.randint(-10,10)
            #get a random x and y speed for the new roid
            delta_x = delta_y = 0
            while delta_x == 0 or delta_y == 0: # we dont want a stationary asteroid
                delta_x = asteroid[AST_DX] + random.randint(-4,4)
                delta_y = asteroid[AST_DY] + random.randint(-4,4)
                
            if asteroid[AST_SIZE] == AST_LARGE:
                size = AST_MED
                width = asteroid_medium_image.get_width()
                height = asteroid_medium_image.get_height()
            else:
                size = AST_SMALL
                width = asteroid_small_image.get_width()
                height = asteroid_small_image.get_height() 
                                     
            rect = pygame.Rect(x,y, width,height) 
            new_asteroid = [delta_x,delta_y, rect, size]
            new_asteroids.append(new_asteroid)
            
    #add the new asteroids in to the asteroid list
    for asteroid in new_asteroids:
        asteroid_list.append(asteroid)
    return
    
def spawn_random_asteroid():
    global asteroid_list
    
    size = random.randint(0,2)
    x = ship_rect.centerx
    y = ship_rect.centery
    
    if size == AST_LARGE:
        width = asteroid_large_image.get_width()
        height = asteroid_large_image.get_height()
    elif size == AST_MED:
        width = asteroid_medium_image.get_width()
        height = asteroid_medium_image.get_height() 
    else:
        width = asteroid_small_image.get_width()
        height = asteroid_small_image.get_height()  
        
    while distance(x,y,ship_rect.centerx, ship_rect.centery) < 300:
        x = random.randint(width,SCREEN_WIDTH-width)
        y = random.randint(height,SCREEN_HEIGHT-height)
        
    delta_x = delta_y = 0
    while delta_x == 0 and delta_y == 0: # dont want stationary asteroids
        delta_x = random.randint(-3,3)
        delta_y = random.randint(-3,3)
        
    rect = pygame.Rect(x, y, width, height)
    asteroid = [delta_x,delta_y, rect, size]
    asteroid_list.append(asteroid)
    
def check_pygame_events():
    global ship_angle, ship_delta_x, ship_delta_y, game_state, current_ship_img
    button0 = False
    button1 = False
    button7 = False
    button9 = False
    axis0 = False
    axis1 = False
    keys = pygame.key.get_pressed()
    event = pygame.event.poll()
    
    if joystick_count >0:
        axis0 = joystick.get_axis(0)
        axis1 = joystick.get_axis(1)
        button1 = joystick.get_button(1)
        button0 = joystick.get_button(0)
        button9 = joystick.get_button(9)
        button7 = joystick.get_button(7)
    
    if event.type == pygame.QUIT:
        game_state = GAME_STATE_QUIT

    if (keys[pygame.K_SPACE] or button1) and game_state == GAME_STATE_RUNNING:
        fire_sound.play()
        spawn_missile()
    if keys[pygame.K_p] and game_state == GAME_STATE_RUNNING:
        game_state = GAME_STATE_PAUSED
    if (keys[pygame.K_SPACE] or button9 or button7) and game_state == GAME_STATE_TITLE:
        game_state = GAME_STATE_RUNNING
        reset_game()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        ship_angle += 5
    if  axis0  < -0.01:
        ship_angle += axis0*-5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        ship_angle -= 5
    if axis0 > .01:
        ship_angle -= axis0*5
    #if keys[pygame.K_DOWN]:
        #ship_delta_x -= math.cos(math.radians(ship_angle))*ship_accel
        #ship_delta_y -= - (math.sin(math.radians(ship_angle)))*ship_accel
        
    if axis1 < -0.05:
        current_ship_img = ship_img_thrust
        thrust_sound.play()
        if vector_mag(ship_delta_x, ship_delta_y) < 10.0:
            ship_delta_x += math.cos(math.radians(ship_angle))*(axis1*-ship_accel)
            ship_delta_y += - (math.sin(math.radians(ship_angle)))*(axis1*-ship_accel)
    elif keys[pygame.K_UP] or keys[pygame.K_w]:
        current_ship_img = ship_img_thrust
        thrust_sound.play()
        if vector_mag(ship_delta_x, ship_delta_y) < 10.0:
            ship_delta_x += math.cos(math.radians(ship_angle))*ship_accel
            ship_delta_y += - (math.sin(math.radians(ship_angle)))*ship_accel
    else:
        current_ship_img = ship_img_no_thrust

        
    if keys[pygame.K_s] or button0:
        do_smart_bomb()
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
    x = ship_rect.centerx
    y = ship_rect.centery 
    width = missile_image.get_width()
    height = missile_image.get_height()
    delta_x = math.cos(math.radians(ship_angle))*9 + ship_delta_x
    delta_y = -(math.sin(math.radians(ship_angle))*9) + ship_delta_y
    #delta_x = math.cos(math.radians(ship_angle))*10 
    #delta_y = -(math.sin(math.radians(ship_angle))*10) 
    rect = pygame.Rect(x,y,width, height)
    missile = [delta_x,delta_y, rect]
    missile_list.append(missile)
  
def spawn_explosion(x,y, delta_x, delta_y, size):
    global explosion_list
    
    rect = pygame.Rect(x,y, explosion_graphics[0].get_width(), explosion_graphics[0].get_height())
    spawn_time = time.time()
    
    explosion = [0,rect, delta_x, delta_y,0, spawn_time, size]
    explosion_list.append(explosion)
    return 

def update_explosions():
    global explosion_list
    
    for explosion in reversed(explosion_list):
        if time.time() - explosion[EXP_LAST_TIME] > .09:
            explosion[EXP_FRAME] += 1
            if explosion[EXP_FRAME] == len(explosion_graphics):
                explosion_list.remove(explosion)
                continue
            explosion[EXP_LAST_TIME] = time.time()
                    
    
def move_objects():
    global ship_rect, drawn_ship_img, missilelist, asteroid_list, explosion_list
    global ship_delta_x, ship_delta_y
    
    #move player
    ship_rect.move_ip(int(ship_delta_x), int(ship_delta_y))
    drawn_ship_img,ship_rect = rot_center(current_ship_img, ship_rect, ship_angle)
    
    #decelerate player
    if ship_delta_x != 0:   
        ship_delta_x *= ship_friction

    if ship_delta_y !=0:  
        ship_delta_y *= ship_friction
    
    #move missiles
    for missile in missile_list:
        missile[MISSILE_RECT].move_ip(int(missile[MISSILE_DX]), int(missile[MISSILE_DY]) )

    #move asteroids
    for asteroid in asteroid_list:
        asteroid[AST_RECT].move_ip(int(asteroid[AST_DX]), int(asteroid[AST_DY]))
    
    #move explosions
    for explosion in explosion_list:
        explosion[EXP_RECT].move_ip(int(explosion[EXP_DX]), int(explosion[EXP_DY]))
    return
    
    
def check_bounds():
    global ship_delta_x, ship_delta_y, missile_list, asteroid_list
    
    if ship_rect.top <35:
        ship_rect.top = 36
        ship_delta_y = -(ship_delta_y)
        
    if ship_rect.bottom > SCREEN_HEIGHT:
        ship_rect.bottom = SCREEN_HEIGHT-1
        ship_delta_y = -(ship_delta_y)
        
    if ship_rect.left < 0:
        ship_rect.left = 0
        ship_delta_x = -(ship_delta_x)
    
    if ship_rect.right > SCREEN_WIDTH:
        ship_rect.right = SCREEN_WIDTH-1
        ship_delta_x = -(ship_delta_x)
       
    for missile in reversed(missile_list):
        if missile[MISSILE_RECT].x < 0 or missile[MISSILE_RECT].x > SCREEN_WIDTH \
        or missile[MISSILE_RECT].y < 35 or missile[MISSILE_RECT].y > SCREEN_HEIGHT:
            missile_list.remove(missile)
            
    for asteroid in asteroid_list:
        x = asteroid[AST_RECT].x
        y = asteroid[AST_RECT].y
        width = asteroid[AST_RECT].width
        height = asteroid[AST_RECT].height
        if x <= 0 or x > SCREEN_WIDTH-width:
            asteroid[AST_DX] = -asteroid[AST_DX]
        if y < 35:
             asteroid[AST_RECT].y = 36
             asteroid[AST_DY] = -asteroid[AST_DY]
        if y > SCREEN_HEIGHT - height:
            asteroid[AST_DY] = -asteroid[AST_DY]
   
def draw_scene():
    #screen.fill( (0,0,0,128) )
    
    screen.blit(background_image,(0,0) )
    
    rect = pygame.Rect(0,0,SCREEN_WIDTH, 31) 
    pygame.draw.rect(screen, BLACK, rect)
    #draw asteroids
    for asteroid in asteroid_list:
        if asteroid[AST_SIZE] == AST_LARGE:
            image = asteroid_large_image
        elif asteroid[AST_SIZE] == AST_MED:
            image = asteroid_medium_image
        else:
            image = asteroid_small_image
        asteroid[AST_RECT] = screen.blit(image, asteroid[AST_RECT] )
        
    #draw missiles
    for missile in missile_list:
        missile[MISSILE_RECT] = screen.blit(missile_image, missile[MISSILE_RECT])      

    #draw player
    screen.blit(drawn_ship_img,ship_rect)
    #pygame.draw.rect(screen, (255,0,0), ship_rect, 2)
    
    #draw explpsions
    for explosion in explosion_list:
        image_num = explosion[EXP_FRAME]
        image = explosion_graphics[image_num]
 
        rect = explosion[EXP_RECT]
        if explosion[EXP_SIZE] == EXP_SMALL:
            image = pygame.transform.scale(image, (rect.width//3, rect.height//3))
        elif explosion[EXP_SIZE] == EXP_MED:
            image = pygame.transform.scale(image, (rect.width//2, rect.height//2))
        screen.blit(image, rect)
        
    #draw status text
    status_text = "SCORE: "+str(game_score)+"    LEVEL: "+str(game_level) + \
    "    SMART BOMBS: "+str(num_smart_bombs)+"    SHIP ENERGY: "+str(ship_energy)
    
    status_line = font.render(status_text,1, GREEN)
    
    screen.blit(status_line, (0,3) )
    
    pygame.draw.line(screen, GREEN, (0, 33), (SCREEN_WIDTH, 33), 3)
    """
    width = ship_img_no_thrust.get_width()
    height = ship_img_no_thrust.get_height()
    left = player_lives* width+(player_lives*10)
    left = SCREEN_WIDTH-left
    for x in range(player_lives):
        rect = (left,10,width,height)
        screen.blit(ship_img_no_thrust, rect)
        left = left + width + 10
    """
    return
    
def reset_game():
    global missile_list, asteroid_list, ship_rect, ship_delta_x, ship_delta_y
    global ship_angle, game_score, player_lives, game_level, ship_energy

    #make sure missle and asteroid lists are set to 0
    missile_list = []
    asteroid_list = []
    explosion_list = []
    #reset the ships position
    ship_rect.x = SCREEN_WIDTH//2
    ship_rect.y = SCREEN_HEIGHT//2
    ship_delta_x = 0
    ship_delta_y = 0
    ship_angle = 0
    game_level = 1
    game_score = 0
    game_level = 1
    player_lives = 3
    ship_energy = 100
    start_level(game_level)
    pygame.event.clear()
    time.sleep(1)
    pygame.event.clear()
    
def start_level(level):
    print("start level")
    global game_state
    
    num_asteroids = level*2+10
    for x in range(num_asteroids):
        spawn_random_asteroid()
        pygame.mixer.music.play(-1)
    game_state = GAME_STATE_RUNNING

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

def do_level_end():
    print ("level end!!")
    global game_level, missile_list, ship_rect, asteroid_list, ship_energy
    global ship_delta_x, ship_delta_y, game_state, explosion_list
    global ship_energy
    screenshot = screen.copy()
    start_time = time.time()
    
    font = pygame.font.Font("./zorque.ttf", 72, bold=True)
    level_end_text = font.render("LEVEL "+str(game_level)+" CLEARED", 1, GREEN)
    
    x = SCREEN_WIDTH//2 - level_end_text.get_width()//2
    y = SCREEN_HEIGHT//2 - level_end_text.get_height()//2
    
    while time.time() - start_time < 4:
        screen.blit(screenshot,(0,0))
        screen.blit(level_end_text, (x,y) )
        pygame.display.update()
    
    new_energy = game_level*2+10
    ship_energy += new_energy
    ship_energy = clamp(ship_energy, 1,100)
    
    #make sure missle and asteroid lists are set to 0
    missile_list = []
    asteroid_list = []
    explosion_list = []
    #reset the ships position
    ship_rect.x = SCREEN_WIDTH//2
    ship_rect.y = SCREEN_HEIGHT//2
    ship_delta_x = 0
    ship_delta_y = 0
    
    #inrement the next game level
    game_level += 1
    pygame.event.clear()
    start_level(game_level)
    
    return

def update_game_state():
    global game_state
    
    if len(asteroid_list) == 0 and game_state == GAME_STATE_RUNNING:
        game_state = GAME_STATE_LEVEL_OVER
        
    if ship_energy <= 0 and game_state == GAME_STATE_RUNNING:
        game_state = GAME_STATE_GAME_OVER
            
def do_game_over():
    global game_level, missile_list, ship_rect, asteroid_list, game_state
    global ship_energy, game_score

    screenshot = screen.copy()
    start_time = time.time()
    
    font = pygame.font.Font("./zorque.ttf", 72, bold=True)
    level_end_text = font.render("GAME OVER!!!", 1, GREEN)
    score_end_text = font.render("SCORE: "+str(game_score),1, GREEN )
    
    
    level_x = SCREEN_WIDTH//2 - level_end_text.get_width()//2
    level_y = SCREEN_HEIGHT//2 - level_end_text.get_height()
    score_x = SCREEN_WIDTH//2 - score_end_text.get_width()//2
    score_y = level_y + score_end_text.get_height()+20
    
    while time.time() - start_time < 6:
        screen.blit(screenshot,(0,0))
        screen.blit(level_end_text, (level_x,level_y) )
        screen.blit(score_end_text, (score_x, score_y) )
        pygame.display.update()
        
    #make sure missle and asteroid lists are set to 0
    missile_list = []
    asteroid_list = []
    #reste the ships position
    ship_rect.x = SCREEN_WIDTH//2
    ship_rect.y = SCREEN_HEIGHT//2
    #inrement the next game level
    game_level = 0
    game_score = 0
    game_state = GAME_STATE_TITLE
    pygame.mixer.music.stop()
    pygame.event.clear()
    return
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

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900

# Init pygame and set up the drawing window
#pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init()
pygame.key.set_repeat(1,1)
clock = pygame.time.Clock()
#font = pygame.font.SysFont("Arial", 28)
font = pygame.font.Font("./zorque.ttf", 28, bold=True)
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.SRCALPHA, 32)

#init the joysticks
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()

if joystick_count >0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    name = joystick.get_name()
    print("Joystick name: {} initialized".format(name))


#LOAD GRAPHICS
print("Loading graphics......")
ship_img_no_thrust = pygame.image.load('spaceship8.png')
ship_img_thrust = pygame.image.load('spaceship8_thrust.png')
missile_image=pygame.image.load("missile.png")
asteroid_small_image = pygame.image.load("asteroid_small.png")
asteroid_medium_image = pygame.image.load("asteroid_medium.png")
asteroid_large_image = pygame.image.load("asteroid_large.png")
title_image = pygame.image.load('asteroidback.png')
background_image = pygame.image.load('background2.png')

explosion_graphics =[]
for i in range(7):
    filename = "explosion"+str(i+1)+".png"
    print(filename)
    explosion =  pygame.image.load(filename)
    explosion_graphics.append(explosion)
    
#LOAD SOUNDS
print("Loading sounds......")
fire_sound = pygame.mixer.Sound("fire.wav")
fire_sound.set_volume(.1)

bang_small = pygame.mixer.Sound("bangSmall.wav")
bang_med = pygame.mixer.Sound("bangMedium.wav")
bang_large = pygame.mixer.Sound("bangLarge.wav")

extra_ship_sound = pygame.mixer.Sound("extraShip.wav")
extra_ship_sound.set_volume(1)

game_music = pygame.mixer.music.load('music.ogg')
thrust_sound = pygame.mixer.Sound("thrust.wav")
thrust_sound.set_volume(1)

#setup player/ship variables and information

current_ship_img = ship_img_no_thrust
ship_rect = current_ship_img.get_rect(topleft=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
ship_angle = 0
ship_delta_x = 0
ship_delta_y = 0
ship_friction = .98
ship_accel = 1.001
ship_energy = 100
num_smart_bombs = 400
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
explosion_list = []

#======================================================================#
#                        MAIN GAME LOOP                                #
#======================================================================#
while game_state != GAME_STATE_QUIT:
    check_pygame_events()
    if game_state == GAME_STATE_RUNNING:
        move_objects()
        detect_collisions()
        update_explosions()
        check_bounds()        
        draw_scene()
        pygame.display.update()
        update_game_state()
    elif game_state == GAME_STATE_TITLE:
        title_screen()
        pygame.display.update()
    elif game_state == GAME_STATE_PAUSED:
        game_paused()
    elif game_state == GAME_STATE_LEVEL_OVER:
        do_level_end()
    elif game_state == GAME_STATE_GAME_OVER:
        do_game_over()
    clock.tick(30)

print("Thanks for playing!")
pygame.quit()
sys.exit()

