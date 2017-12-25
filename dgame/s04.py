import pygame

width = 900
height =  700

screen = None
img_top = None
img_down = None

def init_game():
    global screen
    global img_top, img_down
    
    pygame.init()
    
    screen = pygame.display.set_mode((width, height))
    
    img_top = pygame.image.load("bg_top.jpg")
    img_down = pygame.image.load("bg_bottom.jpg")
    img_down = pygame.transform.scale( img_down, (width, 100))
	
    pygame.mixer.init()
    pygame.mixer.music.load("bg_music.mp3")
    pygame.mixer.music.play(-1)


def run_game():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0, 0, 0))
        screen.blit(img_top, (0,0))
        screen.blit(img_down, (0,620))
        pygame.display.update()
    
    return


init_game()

run_game()

pygame.quit()
