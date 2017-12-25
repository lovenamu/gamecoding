import pygame

width = 900
height =  700

screen = None
img_top = None
img_down = None
img_player = None
img_dragon = None

def init_game():
    global screen
    global img_top, img_down
    global img_player
    global img_dragon
    
    pygame.init()
    
    screen = pygame.display.set_mode((width, height))
    
    img_top = pygame.image.load("bg_top.jpg")
    img_down = pygame.image.load("bg_bottom.jpg")
    img_down = pygame.transform.scale( img_down, (width, 100))
    img_player = pygame.image.load("boy.png")
    img_player = pygame.transform.scale(img_player, (80, 106))
    img_dragon = pygame.image.load("dragon.png")
    img_dragon = pygame.transform.scale(img_dragon, (400, 160))
	
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

	
def update_dragon(pos_dx, pod_dy):
    screen.blit(img_dragon, (pos_dx, pod_dy))
    
    return
    
def run_game():
    running = True
    
    pos_x = width / 2
    pos_y = height - 120
    move_x = 0
    
    pos_dx = 20
    pod_dy = 30
    
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
        
        update_dragon(pos_dx, pod_dy)
        
        pos_x = update_player(pos_x, pos_y, move_x)
        
        pygame.display.update()
    
    return


init_game()

run_game()

pygame.quit()
