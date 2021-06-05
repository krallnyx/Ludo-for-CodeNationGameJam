# Imports
import pygame
from Pawn import Pawn

#  the Yard positions are the starting positions for each pawn, before they enter the game
YARD_POSITIONS = {
    "green": [(108, 687), (108, 597), (207, 687), (207, 597)],
    "yellow": [(108, 227), (108, 117), (207, 227), (207, 117)],
    "red": [(593, 687), (593, 597), (692, 687), (692, 597)],
    "blue": [(593, 227), (593, 117), (692, 227), (692, 117)]
}
ROLL_MENU_POSITIONS = [(102, 602), (102, 122), (583, 122), (583, 602)]


class Player(pygame.sprite.Sprite):
    """Defines a player with his pawns. Need to be given a color"""
    def __init__(self, color):
        super().__init__()
        self.pawn1 = Pawn(color, YARD_POSITIONS[color][0])
        self.pawn2 = Pawn(color, YARD_POSITIONS[color][1])
        self.pawn3 = Pawn(color, YARD_POSITIONS[color][2])
        self.pawn4 = Pawn(color, YARD_POSITIONS[color][3])
        self.pawns_in_yard = 4
        self.game_over = False
        self.color = color

    def roll_menu(self, screen, current_player):
        """Asks the player to roll the dice, seems better than automatically rolling for him, feels more interactive"""
        screen.blit(pygame.image.load(f"Assets/mid_button_off.png"), (ROLL_MENU_POSITIONS[current_player][0]-80, ROLL_MENU_POSITIONS[current_player][1]-100))
        text = pygame.font.SysFont('Times New Roman', 21).render('Roll the dice', False, (255, 255, 255))
        screen.blit(text, (ROLL_MENU_POSITIONS[current_player][0]-70, ROLL_MENU_POSITIONS[current_player][1]-80))
        pygame.display.update()
        return ROLL_MENU_POSITIONS[current_player][0]-80, ROLL_MENU_POSITIONS[current_player][1]-100

    def choice_menu(self):
        """Displays a menu of actions a player can do"""

    def draw_pawns(self, surface):
        """Draws the four pawns of the player on the surface at their respective locations"""
        self.pawn1.draw(surface)
        self.pawn2.draw(surface)
        self.pawn3.draw(surface)
        self.pawn4.draw(surface)