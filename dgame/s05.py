import pygame

width = 900
height =  700

screen = None
img_top = None
img_down = None
img_player = None

def init_game():
    global screen
    global img_top, img_down
    global img_player
    
    pygame.init()
    
    screen = pygame.display.set_mode((width, height))
    
    img_top = pygame.image.load("bg_top.jpg")
    img_down = pygame.image.load("bg_bottom.jpg")
    img_down = pygame.transform.scale( img_down, (width, 100))
    img_player = pygame.image.load("boy.png")
    img_player = pygame.transform.scale(img_player, (80, 106))
	
    pygame.mixer.init()
    pygame.mixer.music.load("bg_music.mp3")
    pygame.mixer.music.play(-1)


def update_player(pos_x, pos_y):
    screen.blit(img_player, (pos_x, pos_y))

    return

	
def run_game():
    running = True
    
    pos_x = width / 2
    pos_y = height - 120
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0, 0, 0))
        screen.blit(img_top, (0,0))
        screen.blit(img_down, (0,620))
        
        update_player(pos_x, pos_y)
        
        pygame.display.update()
    
    return


init_game()

run_game()

pygame.quit()
