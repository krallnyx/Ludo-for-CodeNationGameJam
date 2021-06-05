# Imports
import pygame
from pygame.locals import *
import sys
from Game import Game
import time

# Initializing
pygame.init()

#  Other Variables for use in the program
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

#  Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

# displaying a window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    time.sleep(0.5)
