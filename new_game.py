import pygame 
import os
from grid import Grid

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (400, 100)

surface = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("Sudoku Victor")


pygame.font.init()

game_font = pygame.font.SysFont(name='Comic Sans MS', size=50)

grid = Grid(game_font)
running = True

while running:
#check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    surface.fill((255,255,255))
    grid.draw_lines(pygame, surface)
    pygame.display.flip()