from Dice import Dice
from Player import Player
import pygame

GRID_POSITIONS = [
    (400, 775), (347, 775), (347, 720), (347, 667), (347, 614), (347, 561), (347, 506), (347, 454),
    (293, 454), (239, 454), (186, 454), (132, 454), (79, 454), (25, 454),
    (25, 400), (25, 347), (79, 347), (132, 347), (186, 347), (239, 347), (293, 347),
    (347, 347), (347, 293), (347, 238), (347, 185), (347, 133), (347, 79), (347, 25), (400, 25),
    (454, 25), (454, 79), (454, 133), (454, 185), (454, 238), (454, 293), (454, 347),
    (507, 347), (561, 347), (614, 347), (668, 347), (721, 347), (775, 347), (775, 400),
    (775, 454), (721, 454), (668, 454), (614, 454), (561, 454), (507, 454),
    (454, 454), (454, 506), (454, 561), (454, 614), (454, 667),  (454, 720), (454, 775)
                  ]


class Game:
    """Event management for the game"""
    def __init__(self, screen):
        self.current_player = 0
        self.dice_result = 0
        self.players = [Player("green"), Player("yellow"), Player("blue"), Player("red")]
        self.dice = Dice(6)
        self.screen = screen
        self.game_over = False
        self.roll_pressed = False

    def events(self):
        """Check which event is running"""
        if not self.game_over:
            if self.dice_result == 0 and not self.roll_pressed:
                button = self.players[self.current_player].roll_menu(self.screen, self.current_player)
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            click = pygame.mouse.get_pos()
                            if (button[0] <= click[0] <= button[0] + 128) and (button[1] <= click[1] <= button[1] + 64):
                                self.roll_pressed = True
                                return 0
            elif self.roll_pressed:
                self.dice_result = self.dice.animate(self.screen)
                self.roll_pressed = False
                return 0
            elif self.dice_result != 0:
                # we display the choices to the player and wait for his action if any possible
                if self.dice_result == 6:
                    print("You can get a pawn out or move 6 and play twice if you have no pawn in the yard")
                    if self.players[self.current_player].pawns_in_yard == 4:
                        self.players[self.current_player].pawns_in_yard -= 1
                        self.players[self.current_player].pawn4.move(
                            GRID_POSITIONS[self.players[self.current_player].pawn4.starting_point])
                elif self.players[self.current_player].pawns_in_yard == 4:
                    print(f"I'm sorry {self.players[self.current_player].color}"
                          f", you have to get a 6 to get out of the yard")
                else:
                    print(
                        f"Player {self.players[self.current_player].color},"
                        f" you rolled {self.dice_result}, what do you want to do?")
                self.dice_result = 0
                self.current_player += 1
                if self.current_player == 4:
                    self.current_player = 0
