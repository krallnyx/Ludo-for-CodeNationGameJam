# Imports
import pygame


class Pawn(pygame.sprite.Sprite):
    """Basic moving piece on the board, need to be initialized with a color and location"""
    def __init__(self, color, location):
        super().__init__()
        if color == "green":
            self.starting_point = 1
        elif color == "yellow":
            self.starting_point = 15
        elif color == "blue":
            self.starting_point = 29
        else:
            self.starting_point = 43
        self.color = color
        self.location = location
        self.image = pygame.image.load(f"Assets/{color}2.png")
        self.surf = pygame.Surface((54, 54))
        self.rect = self.surf.get_rect(center=location)
        self.yard = True

    def move(self, new_location):
        """Initiates the move from any place on the grid to the given new location (tuple)"""
        x = self.location[0]
        y = self.location[1]
        while (x, y) != new_location:
            if x > new_location[0]:
                x -= 1
                self.rect.move_ip(-1, 0)
            elif x < new_location[0]:
                x += 1
                self.rect.move_ip(1, 0)
            if y > new_location[1]:
                y -= 1
                self.rect.move_ip(0, -1)
            elif y < new_location[1]:
                y += 1
                self.rect.move_ip(0, 1)
        self.location = (x, y)

    def draw(self, surface):
        """Displays the pawn on the surface, need to be called at each update"""
        surface.blit(self.image, self.rect)