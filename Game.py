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

COLORS = {'green': 0, 'yellow': 1, 'blue': 2, 'red': 3}

def initialise_pawns_on_grid():
    """Create a dictionary of positions on the grid, initialised to None. It will keep track of pawns on the grid"""
    dic = {}
    for i in range(len(GRID_POSITIONS)):
        dic[i] = None
    return dic


def game_quit():
    """Close game event"""
    pygame.quit()
    sys.exit()


def wait_for_click(button):
    """A button is displayed, waiting for the player to click it"""
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                game_quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                if (button[0] <= click[0] <= button[0] + 128) and (
                        button[1] <= click[1] <= button[1] + 64):
                    return 0


def wait_for_choice(buttons):
    """2 buttons are displayed, waiting for the player to click 1"""
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                game_quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                if (buttons[0][0] <= click[0] <= buttons[0][0] + 128) and (
                        buttons[0][1] <= click[1] <= buttons[0][1] + 64):
                    return 0
                elif (buttons[1][0] <= click[0] <= buttons[1][0] + 128) and (
                        buttons[1][1] <= click[1] <= buttons[1][1] + 64):
                    return 1


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
        self.pawns_on_grid = initialise_pawns_on_grid()

    def get_current_grid_position(self, pawn):
        """Returns the index in the grid of the current location of a pawn"""
        if pawn.on_ladder:
            return self.players[self.current_player].ladder.index(pawn.location)
        else:
            return GRID_POSITIONS.index(pawn.location)

    def is_pawn_at_starting_point(self):
        for pawn in self.players[self.current_player].pawns:
            if pawn.is_centre or pawn.yard:
                pass
            else:
                if GRID_POSITIONS[pawn.starting_point] == pawn.location:
                    return True
        return False

    def end_of_turn(self):
        """reset the dice_result and change the player"""
        self.current_player += 1
        if self.players[self.current_player].game_over:
            self.end_of_turn()
        if self.current_player == len(self.players):
            self.current_player = 0
        self.dice_result = 0
        self.moving = 0
        self.current_pawn = None

    def move_pawn(self):
        if not self.current_pawn.on_ladder:
            pawn_index = GRID_POSITIONS.index(self.current_pawn.location)
            self.pawns_on_grid[pawn_index] = None
            val = self.steps_taken(pawn_index)
            # print(f"grid value :{val} > 55?")
            if val > len(GRID_POSITIONS)-1:
                pass  # we removed it from the grid, it's on the ladder anyway
            else:
                val = pawn_index + self.dice_result
                if val > 55:
                    val -= 56
                # print(f"added pawn at {val}")
                if self.pawns_on_grid[val] is not None:
                    # there is something here, if it's an opponent we have to return it to it's yard
                    if self.pawns_on_grid[val].color == self.current_pawn.color:
                        pass # never-mind it's one of us!
                    else:
                        self.return_pawn_to_yard(self.pawns_on_grid[val])
                self.pawns_on_grid[val] = self.current_pawn
        self.loc = self.get_current_grid_position(self.current_pawn)
        self.moving = self.dice_result

    def move_1_pawn(self):
        button = self.players[self.current_player].move_pawn(self.screen, self.current_player, self.dice)
        wait_for_click(button)
        self.move_pawn()

    def spawn_pawn(self, pawn_number):
        self.players[self.current_player].pawns_on_board.append(pawn_number)
        self.players[self.current_player].current_pawn = pawn_number
        self.players[self.current_player].pawns[pawn_number].yard = False
        self.current_pawn = self.players[self.current_player].pawns[pawn_number]
        self.players[self.current_player].pawns_in_yard.remove(pawn_number)

    def click_pawn(self, pawns_can_move):
        self.players[self.current_player].choose_pawn(self.screen, self.current_player, self.dice)
        pawns = [p for p in pawns_can_move]
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = pygame.mouse.get_pos()
                    for pawn in pawns:
                        if (pawn.location[0]-27 <= click[0] <= pawn.location[0] + 27) and (
                                pawn.location[1]-27 <= click[1] <= pawn.location[1] + 27):
                            self.players[self.current_player].current_pawn = pawns.index(pawn)
                            self.current_pawn = pawn
                            if self.current_pawn.on_ladder:
                                self.loc = self.players[self.current_player].ladder.index(pawn.location)
                            else:
                                self.loc = GRID_POSITIONS.index(pawn.location)
                                pawn_index = GRID_POSITIONS.index(self.current_pawn.location)
                                self.pawns_on_grid[pawn_index] = None
                                val = self.steps_taken(pawn_index)
                                # print(f"grid value :{val} > 55?")
                                if val > len(GRID_POSITIONS) - 1:
                                    pass  # we removed it from the grid, it's not on it anymore anyway
                                else:
                                    val = pawn_index + self.dice_result
                                    if val > 55:
                                        val -= 56
                                    # print(f"added pawn at {val}")
                                    if self.pawns_on_grid[val] is not None:
                                        # there is something here, if it's an opponent we have to return it to it's yard
                                        if self.pawns_on_grid[val].color == self.current_pawn.color:
                                            pass  # never-mind it's one of us!
                                        else:
                                            self.return_pawn_to_yard(self.pawns_on_grid[val])
                                    self.pawns_on_grid[val] = self.current_pawn
                            self.moving = self.dice_result
                            return 0

    def steps_taken(self, pawn_index):
        if pawn_index < self.current_pawn.starting_point:
            pawn_index += 56
        return pawn_index + self.dice_result - self.current_pawn.starting_point

    def player_rolled_6(self, pawns_can_move):
        """player rolling a 6 is a special event"""
        try:
            self.current_pawn = pawns_can_move[0]
        except IndexError:
            self.current_pawn = None
        if len(pawns_can_move) == 0 and len(self.players[self.current_player].pawns_in_yard) > 0:
            # print("none can move, pawn(s) in yard")
            # print(f"pawns in yard {self.players[self.current_player].pawns_in_yard}")
            button = self.players[self.current_player].pawn_out_menu(self.screen, self.current_player, self.dice)
            wait_for_click(button)
            self.roll_pressed = True
            self.players[self.current_player].pawns_on_board.append(self.players[self.current_player].pawns_in_yard[-1])
            self.players[self.current_player].pawns[self.players[self.current_player].pawns_in_yard[-1]].yard = False
            self.players[self.current_player].current_pawn = self.players[self.current_player].pawns_in_yard[-1]
            self.current_pawn = self.players[self.current_player].pawns_in_yard[-1]
            self.players[self.current_player].pawns_in_yard.pop()
            self.players[self.current_player].pawns[
                self.players[self.current_player].current_pawn].move(
                GRID_POSITIONS[self.players[self.current_player].pawns[
                    self.players[self.current_player].current_pawn].starting_point])
            self.current_pawn = self.players[self.current_player].pawns[self.players[self.current_player].current_pawn]
            if self.pawns_on_grid[self.current_pawn.starting_point] is not None:
                self.return_pawn_to_yard(self.pawns_on_grid[self.current_pawn.starting_point])
            self.pawns_on_grid[GRID_POSITIONS.index(self.current_pawn.location)] = \
                self.current_pawn
            # print(f"pawns in yard {self.players[self.current_player].pawns_in_yard}")
        elif len(pawns_can_move) == 1 and self.is_pawn_at_starting_point():
            # print("rolled 6, only 1 can move, there is a pawn at start")
            self.move_1_pawn()
            return 0
        elif len(pawns_can_move) == 0:
            # print("rolled 6 and 0 can move, none in yard")
            pass
        elif len(pawns_can_move) <= 3 and \
                len(self.players[self.current_player].pawns_in_yard) > 0 and \
                not self.is_pawn_at_starting_point():
            # print("rolled 6, at least 1 can move, at least 1 in yard")
            buttons = self.players[self.current_player].choice_menu(self.screen, self.current_player, self.dice)
            choice = wait_for_choice(buttons)
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
                self.current_pawn = self.players[self.current_player].pawns[
                    self.players[self.current_player].current_pawn]
                if self.pawns_on_grid[self.current_pawn.starting_point] is not None:
                    self.return_pawn_to_yard(self.pawns_on_grid[self.current_pawn.starting_point])
                self.pawns_on_grid[GRID_POSITIONS.index(self.current_pawn.location)] = \
                    self.current_pawn
            elif choice == 1:
                # move existing pawn clicked"
                if len(pawns_can_move) == 1:
                    self.current_pawn = pawns_can_move[0]
                    self.move_pawn()
                    return 0
                else:
                    # the player need to choose which pawn to move
                    self.click_pawn(pawns_can_move)
                    return 0
        elif len(pawns_can_move) <= 3:
            # print("rolled 6, at least 1 can move, 0 in yard")
            self.click_pawn(pawns_can_move)
            return 0
        self.roll_pressed = False
        self.end_of_turn()

    def pawns_can_move(self):
        list_pawns = []
        for pawn in self.players[self.current_player].pawns:
            if not pawn.is_centre and not pawn.yard:
                # print("pawn not in centre no in yard")
                if pawn.on_ladder:
                    # print(f"pawn on ladder. pos:{self.get_current_grid_position(pawn)}, dice:{self.dice_result}")
                    if (self.get_current_grid_position(pawn) + self.dice_result) < 7:
                        # print("enough room on ladder, pawn can move")
                        list_pawns.append(pawn)
                else:
                    if not self.move_is_blocked(pawn):
                        # print("pawn can move")
                        list_pawns.append(pawn)
            else:
                # print("pawn in yard or centre")
                pass
        # print(f"{len(list_pawns)} pawns can move")
        if len(list_pawns) == 1:
            self.current_pawn = list_pawns[0]
        return list_pawns

    def move_is_blocked(self, pawn):
        loc = GRID_POSITIONS.index(pawn.location)
        for i in range(loc+1, loc + self.dice_result):
            if i > 55:
                val = i-56
            else:
                val = i
            if pawn.starting_point == val:
                return False
            if self.pawns_on_grid[val] is not None:
                # print(f"move is blocked on index {i}")
                return True
        val = loc + self.dice_result
        if val > 55:
            val -= 56
        if self.pawns_on_grid[val] is not None and\
                self.pawns_on_grid[val].color == pawn.color:
            return True
        # print("path not blocked")
        return False

    def return_pawn_to_yard(self, pawn):
        pawn.yard = True
        pawn.move(self.players[self.current_player].yard_pos[pawn.color][pawn.index])
        self.players[COLORS[pawn.color]].pawns_on_board.remove(pawn.index)
        self.players[COLORS[pawn.color]].pawns_in_yard.append(pawn.index)

    def events(self):
        """Check which event is running"""
        if not self.game_over:
            if self.moving > 0:
                # print("pawn still moving")
                self.loc += 1
                if self.loc == self.players[self.current_player].pawns[0].starting_point:
                    self.current_pawn.move(self.players[self.current_player].ladder[0])
                    # print("current pawn is now on ladder")
                    self.current_pawn.on_ladder = True
                elif self.current_pawn.on_ladder:
                    self.current_pawn.move(self.players[self.current_player].ladder[self.get_current_grid_position(self.current_pawn)+1])
                    if self.get_current_grid_position(self.current_pawn) == 6 and self.moving == 1:
                        self.current_pawn.is_centre = True
                        self.players[self.current_player].pawns_on_centre += 1
                        if self.players[self.current_player].pawns_on_centre == 4:
                            self.players[self.current_player].game_over = True
                            print("player has finished!")
                            self.finishers.append(self.players[self.current_player].color)
                            print(f"You finished on position :{len(self.finishers)}")
                            if len(self.finishers) >= len(self.players)-1:
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
                if self.moving <= 0:
                    self.end_of_turn()
                return 0
            if self.dice_result == 0 and not self.roll_pressed:
                # print("displaying roll dice button")
                button = self.players[self.current_player].roll_menu(self.screen, self.current_player, self.dice)
                wait_for_click(button)
                self.roll_pressed = True
                return 0
            elif self.roll_pressed:
                # print("roll pressed")
                self.dice_result = self.dice.animate(self.screen)
                self.roll_pressed = False
                return 0
            elif self.dice_result != 0:
                # print("entering loop 'dice has a result'")
                pawns_can_move = self.pawns_can_move()
                # we display the choices to the player and wait for his action if any possible
                if self.dice_result == 6:
                    # print("launching dice = 6")
                    self.player_rolled_6(pawns_can_move)
                    return 0
                elif len(pawns_can_move) == 0:
                    # print("no action, pass")
                    pass
                else:
                    # print("dice has a result => else")
                    if len(pawns_can_move) == 1:
                        # print("1 can move")
                        self.current_pawn = self.players[self.current_player].pawns[
                            self.players[self.current_player].pawns_on_board[0]]
                        self.current_pawn = pawns_can_move[0]
                        self.move_1_pawn()
                        return 0
                    else:
                        # print("many can move")
                        self.click_pawn(pawns_can_move)
                        return 0
                self.end_of_turn()
