import random
import time
import pygame


class Dice:
    """Introduce a Dice with a defined number of sides (in case we want to add more, like a special bonus...)"""
    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        """Basic function of a dice, rolling and returning an integer from 1 to number of sides (both included)"""
        return random.randint(5, self.sides)

    def animate(self, screen):
        """While the dice is rolling, will display random results for a couple of seconds then return the result"""
        t_end = time.time() + 2
        pygame.mixer.Sound('Assets/dice.wav').play()
        while time.time() < t_end:
            num = self.roll()
            screen.blit(pygame.image.load(f"Assets/{num}.png"), (336, 336))
            pygame.display.update()
            time.sleep(0.075)
        time.sleep(3)
        return num
