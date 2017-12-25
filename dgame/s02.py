import pygame

width = 900
height =  700

screen = None


def init_game():
    global screen
	
    pygame.init()
    
    screen = pygame.display.set_mode((width, height))
    

def run_game():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
	
    return


init_game()

run_game()

pygame.quit()
