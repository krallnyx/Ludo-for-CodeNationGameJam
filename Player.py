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
        self.pawns_on_centre = 0
        self.current_pawn = 3
        self.game_over = False
        self.color = color
        self.ladder = []
        self.initialise_ladder()


    def initialise_ladder(self):
        if self.color == 'green':
            self.ladder = [(400, 720), (400, 667), (400, 614), (400, 561), (400, 506), (400, 454), (400, 400)]
        elif self.color == 'yellow':
            self.ladder = [(79, 400), (132, 400), (186, 400), (239, 400), (293, 400), (347, 400), (400, 400)]
        elif self.color == 'blue':
            self.ladder = [(400, 79), (400, 133), (400, 185), (400, 238), (400, 293), (400, 347), (400, 400)]
        elif self.color == 'red':
            self.ladder = [(721, 400), (668, 400), (614, 400), (561, 400), (507, 400), (454, 400), (400, 400)]

    def one_button_menu(self, screen, current_player, font_size, text, dice, large = False):
        """Asks the player to roll the dice, seems better than automatically rolling for him, feels more interactive"""
        text = pygame.font.SysFont('Times New Roman', font_size).render(text, False, (255, 255, 255))
        if large:
            screen.blit(pygame.image.load(f"Assets/large_display.png"),
                    (ROLL_MENU_POSITIONS[current_player][0], ROLL_MENU_POSITIONS[current_player][1]))
            screen.blit(text,
                        (ROLL_MENU_POSITIONS[current_player][0] + 50, ROLL_MENU_POSITIONS[current_player][1] + 20))
        else:
            screen.blit(pygame.image.load(f"Assets/mid_button_off.png"),
                        (ROLL_MENU_POSITIONS[current_player][0], ROLL_MENU_POSITIONS[current_player][1]))
            screen.blit(text, (ROLL_MENU_POSITIONS[current_player][0]+10, ROLL_MENU_POSITIONS[current_player][1]+20))
        screen.blit(pygame.image.load(f"Assets/{dice.num}.png"), (336, 336))
        pygame.display.update()
        return ROLL_MENU_POSITIONS[current_player][0], ROLL_MENU_POSITIONS[current_player][1]

    def two_buttons_menu(self, screen, current_player, font_size, text1, text2, dice):
        """Asks the player to chose between 2 different possible actions"""
        screen.blit(pygame.image.load(f"Assets/mid_button_off.png"),
                    (ROLL_MENU_POSITIONS[current_player][0], ROLL_MENU_POSITIONS[current_player][1]))
        screen.blit(pygame.image.load(f"Assets/mid_button_off.png"),
                    (ROLL_MENU_POSITIONS[current_player][0] + 148, ROLL_MENU_POSITIONS[current_player][1]))
        text1 = pygame.font.SysFont('Times New Roman', font_size).render(text1, False, (255, 255, 255))
        text2 = pygame.font.SysFont('Times New Roman', font_size).render(text2, False, (255, 255, 255))
        screen.blit(text1, (ROLL_MENU_POSITIONS[current_player][0] + 10, ROLL_MENU_POSITIONS[current_player][1] + 20))
        screen.blit(text2, (ROLL_MENU_POSITIONS[current_player][0] + 158, ROLL_MENU_POSITIONS[current_player][1] + 20))
        screen.blit(pygame.image.load(f"Assets/{dice.num}.png"), (336, 336))
        pygame.display.update()
        return [(ROLL_MENU_POSITIONS[current_player][0], ROLL_MENU_POSITIONS[current_player][1]),
                (ROLL_MENU_POSITIONS[current_player][0]+148, ROLL_MENU_POSITIONS[current_player][1])
                ]

    def roll_menu(self, screen, current_player, dice):
        """Asks the player to roll the dice, seems better than automatically rolling for him, feels more interactive"""
        return self.one_button_menu(screen, current_player, 21, 'Roll the dice', dice)

    def pawn_out_menu(self, screen, current_player, dice):
        """Player rolled a 6, all his pawns were in yard so he can get one out"""
        return self.one_button_menu(screen, current_player, 20, 'Get pawn out', dice)

    def move_pawn(self, screen, current_player, dice):
        """Player didn't roll a 6, he has only 1 pawn out so no need to choose which one to move"""
        return self.one_button_menu(screen, current_player, 21, 'Move pawn', dice)

    def choice_menu(self, screen, current_player, dice):
        """Displays a menu of actions a player can do"""
        return self.two_buttons_menu(screen, current_player, 20, 'Get pawn out', 'Move pawn', dice)

    def choose_pawn(self, screen, current_player, dice):
        """Displays a large button asking the player to choose a pawn"""
        return self.one_button_menu(screen, current_player, 21, 'Please choose pawn', dice, large=True)

    def draw_pawns(self, surface):
        """Draws the four pawns of the player on the surface at their respective locations"""
        for pawn in self.pawns:
            pawn.draw(surface)
