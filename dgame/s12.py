import pygame
import random

width = 900
height =  700

speed_dx = 4
speed_dy = 2
max_life = 3

max_fire = 9
speed_f = 3

screen = None
img_top = None
img_down = None
img_player = None
img_dragon = None
img_fire = None
img_exp = None

music_exp = None

def init_game():
    global screen
    global img_top, img_down
    global img_player
    global img_dragon
    global img_fire
    global img_exp, music_exp
    
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
    img_exp = pygame.image.load("explosion.png")
    img_exp = pygame.transform.scale(img_exp, (120, 100))

    pygame.mixer.init()
    pygame.mixer.music.load("bg_music.mp3")
    pygame.mixer.music.play(-1)
    music_exp = pygame.mixer.Sound("explosion_music.wav")


def update_player(pos_x, pos_y, move_x, cool_time):
    pos_x += move_x
    
    if pos_x < 0:
        pos_x = width
    if pos_x > width:
        pos_x = 0
    
    if cool_time > 0:
        screen.blit(img_exp, (pos_x - 20, pos_y - 20))
        cool_time = cool_time - 1
    
    screen.blit(img_player, (pos_x, pos_y))

    return pos_x, cool_time

	
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


def check_collide(x, y, w, h, x2, y2, w2, h2):
    ret = False
    is_y = False
    is_x_left = False
    is_x_right = False

    if y2 < y < y2 + h2:
        is_y = True
    
    if x <= x2 + w2:
        is_x_left = True
    
    if x + w >= x2:
        is_x_right = True

    if is_y and is_x_left and is_x_right:
        ret = True
    
    return ret


def player_collide(x, y, fire_pos, cool_time):
    is_collide = False

    fire_rect = img_fire.get_rect()
    w2 = fire_rect[2]
    h2 = fire_rect[3]
    player_rect = img_player.get_rect()
    w = player_rect[2]
    h = player_rect[3]

    if cool_time > 0:
        return False

    for i in range(0, max_fire):
        if fire_pos[i] != (0, 0):
            x2 = fire_pos[i][0]
            y2 = fire_pos[i][1]
            is_collide = check_collide(x, y, w, h, x2, y2, w2, h2)
            if is_collide == True:
                fire_pos[i] = (0, 0)
                break

    return is_collide


def show_life(font, life):
    t1 = font.render("Player-%d" % life, True, (255, 255, 255))
    screen.blit(t1, (5, 5))
    
    return


def run_game():
    running = True
    
    pos_x = width / 2
    pos_y = height - 120
    move_x = 0
    life = max_life
        
    pos_dx = 20
    pod_dy = 30
    move_dx = speed_dx
    move_dy = speed_dy   
    
    fire_pos = []
    for i in range(0, max_fire):
        fire_pos.append((0,0))
    
    cool_time = 0
    
    font = pygame.font.SysFont("malgungothic", 25)
    
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
        is_collide = player_collide(pos_x, pos_y, fire_pos, cool_time)
        if is_collide:
            life = life - 1
            cool_time = 50
            music_exp.play()
        
        pos_x, cool_time = update_player(pos_x, pos_y, move_x, cool_time)
        
        show_life(font, life)
        
        pygame.display.update()

        if life <= 0:
            running = False
    
    return


def game_over():
    is_restart = False

    font1 = pygame.font.SysFont("malgungothic", 60)
    font2 = pygame.font.SysFont("malgungothic", 25)

    screen.fill((0, 0, 0))
    screen.blit(img_top, (0, 0))
    screen.blit(img_down, (0, 620))

    t1 = font1.render("Game Over", True, (255, 255, 255))
    screen.blit(t1, (20, 100))

    t2 = font2.render("게임을 다시 하시려면 'Y'를, 끝내시려면 'N'을 누르세요", True, (255, 255, 255))
    screen.blit(t2, (20, 300))

    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_restart = False
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_restart = False
                    running = False
                elif event.key == pygame.K_y:
                    is_restart = True
                    running = False
                elif event.key == pygame.K_n:
                    is_restart = False
                    running = False

    return is_restart


init_game()

main_running = True
while main_running:
    run_game()
    main_running = game_over()

pygame.quit()
