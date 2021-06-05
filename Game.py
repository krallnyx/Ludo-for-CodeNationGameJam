from Dice import Dice
from Player import Player
import pygame
from pygame.locals import *
import sys

GRID_POSITIONS = [
    (400, 775), (347, 775), (347, 720), (347, 667), (347, 614), (347, 561), (347, 506), (347, 454),
    (293, 454), (239, 454), (186, 454), (132, 454), (79, 454), (25, 454),
    (25, 400), (25, 347), (79, 347), (132, 347), (186, 347), (239, 347), (293, 347),
    (347, 347), (347, 293), (347, 238), (347, 185), (347, 133), (347, 79), (347, 25), (400, 25),
    (454, 25), (454, 79), (454, 133), (454, 185), (454, 238), (454, 293), (454, 347),
    (507, 347), (561, 347), (614, 347), (668, 347), (721, 347), (775, 347), (775, 400),
    (775, 454), (721, 454), (668, 454), (614, 454), (561, 454), (507, 454),
    (454, 454), (454, 506), (454, 561), (454, 614), (454, 667), (454, 720), (454, 775)
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
        self.loc = 0
        self.moving = 0
        self.current_pawn = None
        self.finishers = []

    def game_quit(self):
        """Close game event"""
        pygame.quit()
        sys.exit()

    def get_current_grid_position(self):
        """Returns the index in the grid of the current location of a pawn"""
        pawn = self.players[self.current_player].pawns[self.players[self.current_player].current_pawn]
        if pawn.on_ladder:
            return self.players[self.current_player].ladder.index(pawn.location)
        else:
            return GRID_POSITIONS.index(pawn.location)

    def wait_for_click(self, button):
        """A button is displayed, waiting for the player to click it"""
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game_quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = pygame.mouse.get_pos()
                    if (button[0] <= click[0] <= button[0] + 128) and (
                            button[1] <= click[1] <= button[1] + 64):
                        return 0

    def wait_for_choice(self, buttons):
        """2 buttons are displayed, waiting for the player to click 1"""
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game_quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = pygame.mouse.get_pos()
                    if (buttons[0][0] <= click[0] <= buttons[0][0] + 128) and (
                            buttons[0][1] <= click[1] <= buttons[0][1] + 64):
                        return 0
                    elif (buttons[1][0] <= click[0] <= buttons[1][0] + 128) and (
                            buttons[1][1] <= click[1] <= buttons[1][1] + 64):
                        return 1

    def end_of_turn(self):
        """reset the dice_result and change the player"""
        self.current_player += 1
        if self.current_player == 4:
            self.current_player = 0
        self.dice_result = 0

    def move_pawn(self):
        self.loc = self.get_current_grid_position()
        self.moving = self.dice_result

    def move_1_pawn(self):
        button = self.players[self.current_player].move_pawn(self.screen, self.current_player, self.dice)
        self.wait_for_click(button)
        self.move_pawn()

    def spawn_pawn(self, pawn_number):
        self.players[self.current_player].pawns_on_board.append(pawn_number)
        self.players[self.current_player].current_pawn = pawn_number
        self.players[self.current_player].pawns[pawn_number].yard = False

    def click_pawn(self):
        self.players[self.current_player].choose_pawn(self.screen, self.current_player, self.dice)
        pawns = [p for p in self.players[self.current_player].pawns_on_board]
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game_quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = pygame.mouse.get_pos()
                    print(click)
                    for p in pawns:
                        pawn = self.players[self.current_player].pawns[p]
                        if (pawn.location[0]-27 <= click[0] <= pawn.location[0] + 27) and (
                                pawn.location[1]-27 <= click[1] <= pawn.location[1] + 27):
                            self.players[self.current_player].current_pawn = pawn
                            self.current_pawn = self.players[self.current_player].pawns[p]
                            if self.current_pawn.on_ladder:
                                self.loc = self.players[self.current_player].ladder.index(pawn.location)
                            else:
                                self.loc = GRID_POSITIONS.index(pawn.location)
                            self.moving = self.dice_result
                            return 0

    def player_rolled_6(self):
        """player rolling a 6 is a special event"""
        print(
            f"{self.players[self.current_player].color}, you can get a pawn out or move 6 and play twice if you have no pawn in the yard")
        try:
            self.current_pawn = self.players[self.current_player].pawns[
                self.players[self.current_player].pawns_on_board[0]]
        except IndexError:
            self.current_pawn = None
        if len(self.players[self.current_player].pawns_on_board) == 0:
            print("Careful, it will need to be check if there is already a pawn on starting point")
            button = self.players[self.current_player].pawn_out_menu(self.screen, self.current_player, self.dice)
            self.wait_for_click(button)
            self.roll_pressed = True
            self.players[self.current_player].pawns_on_board.append(3)
            self.players[self.current_player].pawns[3].yard = False
            self.players[self.current_player].pawns[
                self.players[self.current_player].current_pawn].move(
                GRID_POSITIONS[self.players[self.current_player].pawns[
                    self.players[self.current_player].current_pawn].starting_point])
        elif len(self.players[self.current_player].pawns_on_board) == 1 and GRID_POSITIONS[
                self.current_pawn.starting_point] == self.current_pawn.location:
            self.current_pawn = self.players[self.current_player].pawns[
                self.players[self.current_player].pawns_on_board[0]]
            self.move_1_pawn()
            return 0
        elif len(self.players[self.current_player].pawns_on_board) <= 3:
            buttons = self.players[self.current_player].choice_menu(self.screen, self.current_player, self.dice)
            choice = self.wait_for_choice(buttons)
            if choice == 0:
                # New pawn clicked
                if self.players[self.current_player].pawns[3].yard:
                    self.spawn_pawn(3)
                elif self.players[self.current_player].pawns[2].yard:
                    self.spawn_pawn(2)
                elif self.players[self.current_player].pawns[1].yard:
                    self.spawn_pawn(1)
                else:
                    self.spawn_pawn(0)
                self.players[self.current_player].pawns[
                    self.players[self.current_player].current_pawn].move(
                    GRID_POSITIONS[self.players[self.current_player].pawns[
                        self.players[self.current_player].current_pawn].starting_point])
            elif choice == 1:
                # move existing pawn clicked"
                if len(self.players[self.current_player].pawns_on_board) == 1:
                    self.current_pawn = self.players[self.current_player].pawns[
                        self.players[self.current_player].pawns_on_board[0]]
                    self.move_pawn()
                    return 0
                else:
                    # the player need to choose which pawn to move
                    self.click_pawn()
                    return 0
        self.roll_pressed = False
        self.end_of_turn()

    def pawns_can_move(self):
        list_pawns = []
        for pawn in self.players[self.current_player].pawns:
            if not pawn.is_centre and not pawn.yard:
                if pawn.on_ladder:
                    if (self.get_current_grid_position() + self.dice_result) < 7:
                        list_pawns.append(pawn)
                list_pawns.append(pawn)
        return list_pawns

    def events(self):
        """Check which event is running"""
        if not self.game_over:
            if self.moving != 0:
                self.loc += 1
                if self.loc == self.players[self.current_player].pawns[0].starting_point:
                    self.current_pawn.move(self.players[self.current_player].ladder[0])
                    self.current_pawn.on_ladder = True
                elif self.current_pawn.on_ladder:
                    self.current_pawn.move(self.players[self.current_player].ladder[self.get_current_grid_position()+1])
                    if self.get_current_grid_position() == 5 and self.moving == 1:
                        self.current_pawn.is_centre = True
                        self.players[self.current_player].pawns_on_centre += 1
                        if self.players[self.current_player].pawns_on_centre == 4:
                            self.players[self.current_player].game_over = True
                            print("player has finished!")
                            self.finishers.append(self.players[self.current_player].color)
                            print(f"You finished on position :{len(self.finishers)}")
                            if len(self.finishers) >= 3:
                                self.game_over = True
                                print(f"1st: {self.finishers[0]}")
                                print(f"2nd: {self.finishers[1]}")
                                print(f"3rd: {self.finishers[2]}")
                        print("pawn in centre")
                else:
                    if self.loc >= len(GRID_POSITIONS):
                        self.loc = 0
                    self.current_pawn.move(
                        GRID_POSITIONS[self.loc])
                self.moving -= 1
                if self.moving == 0:
                    self.end_of_turn()
                return 0
            if self.dice_result == 0 and not self.roll_pressed:
                button = self.players[self.current_player].roll_menu(self.screen, self.current_player, self.dice)
                self.wait_for_click(button)
                self.roll_pressed = True
                return 0
            elif self.roll_pressed:
                self.dice_result = self.dice.animate(self.screen)
                can_move = self.pawns_can_move()
                print(f"You can move {len(can_move)} pawns.")
                self.roll_pressed = False
                return 0
            elif self.dice_result != 0:
                # we display the choices to the player and wait for his action if any possible
                if self.dice_result == 6:
                    self.player_rolled_6()
                    return 0
                elif len(self.players[self.current_player].pawns_on_board) - \
                        self.players[self.current_player].pawns_on_centre <= 0:
                    print(f"I'm sorry {self.players[self.current_player].color}"
                          f", you have to get a 6 to get out of the yard")
                else:
                    print(
                        f"Player {self.players[self.current_player].color},"
                        f" you rolled {self.dice_result}, what do you want to do?")
                    if len(self.players[self.current_player].pawns_on_board) - \
                            self.players[self.current_player].pawns_on_centre == 1:
                        self.current_pawn = self.players[self.current_player].pawns[
                            self.players[self.current_player].pawns_on_board[0]]
                        self.move_1_pawn()
                        return 0
                    else:
                        self.click_pawn()
                        return 0
                self.end_of_turn()
