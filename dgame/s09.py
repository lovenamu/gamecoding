import pygame
import random

width = 900
height =  700

speed_dx = 4
speed_dy = 2

max_fire = 9
speed_f = 3

screen = None
img_top = None
img_down = None
img_player = None
img_dragon = None
img_fire = None

def init_game():
    global screen
    global img_top, img_down
    global img_player
    global img_dragon
    global img_fire
    
    pygame.init()
    
    screen = pygame.display.set_mode((width, height))
    
    img_top = pygame.image.load("bg_top.jpg")
    img_down = pygame.image.load("bg_bottom.jpg")
    img_down = pygame.transform.scale( img_down, (width, 100))
    img_player = pygame.image.load("boy.png")
    img_player = pygame.transform.scale(img_player, (80, 106))
    img_dragon = pygame.image.load("dragon.png")
    img_dragon = pygame.transform.scale(img_dragon, (400, 160))
    img_fire = pygame.image.load("dragon_fire.png")
    img_fire = pygame.transform.scale(img_fire, (40, 30))
    
    pygame.mixer.init()
    pygame.mixer.music.load("bg_music.mp3")
    pygame.mixer.music.play(-1)


def update_player(pos_x, pos_y, move_x):
    pos_x += move_x
    
    if pos_x < 0:
        pos_x = width
    if pos_x > width:
        pos_x = 0
    
    screen.blit(img_player, (pos_x, pos_y))

    return pos_x

	
def update_dragon(pos_dx, pod_dy, move_dx, move_dy):
    if pos_dx <= 0:
        move_dx = speed_dx
    
    if pos_dx >= width - 400:
        move_dx = -1 * speed_dx
    
    if pod_dy < 20:
        move_dy = speed_dy
    
    if pod_dy > 300:
        move_dy = -1 * speed_dy

    pos_dx = pos_dx + move_dx * (random.random() * 4)
    pod_dy = pod_dy + move_dy

    screen.blit(img_dragon, (pos_dx, pod_dy))

    return pos_dx, pod_dy, move_dx, move_dy
    

def update_fire(fire_pos, pos_dx, pod_dy):
    do_fire = random.random()

    if do_fire < 0.07:
        for j in range(0, max_fire):
            if fire_pos[j] == (0, 0):
                addition = random.random() * 10
                fire_pos[j] = (pos_dx + 60 * addition, pod_dy + 90)
                break

    for i in range(0, max_fire):
        if fire_pos[i] != (0, 0):
            screen.blit(img_fire, fire_pos[i])
            fire_pos[i] = (fire_pos[i][0], fire_pos[i][1] + speed_f)
            if fire_pos[i][1] >= height:
                fire_pos[i] = (0, 0)


def run_game():
    running = True
    
    pos_x = width / 2
    pos_y = height - 120
    move_x = 0
    
    pos_dx = 20
    pod_dy = 30
    move_dx = speed_dx
    move_dy = speed_dy   
    
    fire_pos = []
    for i in range(0, max_fire):
        fire_pos.append((0,0))
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_x = -5
                if event.key == pygame.K_RIGHT:
                    move_x = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    move_x = 0
        
        screen.fill((0, 0, 0))
        screen.blit(img_top, (0,0))
        screen.blit(img_down, (0,620))
        
        (pos_dx, pod_dy, move_dx, move_dy) = update_dragon(pos_dx, pod_dy, move_dx, move_dy)
        
        update_fire(fire_pos, pos_dx, pod_dy)
        
        pos_x = update_player(pos_x, pos_y, move_x)
        
        pygame.display.update()
    
    return


init_game()

run_game()

pygame.quit()
