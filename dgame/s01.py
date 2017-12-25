import pygame

width = 900
height =  700

screen = None


def init_game():
    global screen
	
    pygame.init()
    
    screen = pygame.display.set_mode((width, height))
    

init_game()
