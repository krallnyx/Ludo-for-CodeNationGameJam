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
ROLL_MENU_POSITIONS = [(22, 502), (22, 22), (503, 22), (503, 502)]


class Player(pygame.sprite.Sprite):
    """Defines a player with his pawns. Need to be given a color"""
    def __init__(self, color):
        super().__init__()
        self.pawns = [
            Pawn(color, YARD_POSITIONS[color][0]),
            Pawn(color, YARD_POSITIONS[color][1]),
            Pawn(color, YARD_POSITIONS[color][2]),
            Pawn(color, YARD_POSITIONS[color][3])
        ]
        self.pawns_on_board = []
        self.current_pawn = 3
        self.game_over = False
        self.color = color


    def one_button_menu(self, screen, current_player, font_size, text):
        """Asks the player to roll the dice, seems better than automatically rolling for him, feels more interactive"""
        screen.blit(pygame.image.load(f"Assets/mid_button_off.png"),
                    (ROLL_MENU_POSITIONS[current_player][0], ROLL_MENU_POSITIONS[current_player][1]))
        text = pygame.font.SysFont('Times New Roman', font_size).render(text, False, (255, 255, 255))
        screen.blit(text, (ROLL_MENU_POSITIONS[current_player][0]+10, ROLL_MENU_POSITIONS[current_player][1]+20))
        pygame.display.update()
        return ROLL_MENU_POSITIONS[current_player][0], ROLL_MENU_POSITIONS[current_player][1]

    def two_buttons_menu(self, screen, current_player, font_size, text1, text2):
        """Asks the player to chose between 2 different possible actions"""
        screen.blit(pygame.image.load(f"Assets/mid_button_off.png"),
                    (ROLL_MENU_POSITIONS[current_player][0], ROLL_MENU_POSITIONS[current_player][1]))
        screen.blit(pygame.image.load(f"Assets/mid_button_off.png"),
                    (ROLL_MENU_POSITIONS[current_player][0] + 138, ROLL_MENU_POSITIONS[current_player][1]))
        text1 = pygame.font.SysFont('Times New Roman', font_size).render(text1, False, (255, 255, 255))
        text2 = pygame.font.SysFont('Times New Roman', font_size).render(text2, False, (255, 255, 255))
        screen.blit(text1, (ROLL_MENU_POSITIONS[current_player][0] + 10, ROLL_MENU_POSITIONS[current_player][1] + 20))
        screen.blit(text2, (ROLL_MENU_POSITIONS[current_player][0] + 148, ROLL_MENU_POSITIONS[current_player][1] + 20))
        pygame.display.update()
        return [(ROLL_MENU_POSITIONS[current_player][0], ROLL_MENU_POSITIONS[current_player][1]),
                (ROLL_MENU_POSITIONS[current_player][0]+138, ROLL_MENU_POSITIONS[current_player][1])
        ]


    def roll_menu(self, screen, current_player):
        """Asks the player to roll the dice, seems better than automatically rolling for him, feels more interactive"""
        return self.one_button_menu(screen, current_player, 21, 'Roll the dice')

    def pawn_out_menu(self, screen, current_player):
        """Player rolled a 6, all his pawns were in yard so he can get one out"""
        return self.one_button_menu(screen, current_player, 20, 'Get pawn out')

    def move_pawn(self, screen, current_player):
        """Player didn't roll a 6, he has only 1 pawn out so no need to choose which one to move"""
        return self.one_button_menu(screen, current_player, 21, 'Move pawn')

    def choice_menu(self, screen, current_player):
        """Displays a menu of actions a player can do"""
        return self.two_buttons_menu(screen, current_player, 20, 'Get pawn out', 'Move pawn')

    def draw_pawns(self, surface):
        """Draws the four pawns of the player on the surface at their respective locations"""
        for pawn in self.pawns:
            pawn.draw(surface)
