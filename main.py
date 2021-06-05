# Imports
import pygame
from pygame.locals import *
import sys
from Game import Game

# Initializing
pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#  Other Variables for use in the program
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

#  Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

# displaying a window
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
screen.fill(BLACK)
background = pygame.image.load("Assets/wood.jpg")
board = pygame.image.load("Assets/board.png")
pygame.display.set_caption("Ludo")

game = Game(screen)

# keep game running
while True:
    screen.blit(background, (0, 0))
    screen.blit(board, (0, 0))

    for player in game.players:
        player.draw_pawns(screen)
    game.events()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    FramePerSec.tick(FPS)
