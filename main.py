import os
import time
import random

import pygame
import neat

WIND_WIDTH = 800
WIND_HEIGHT = 600

IMAGE_PATH = "assets/img"


def load_image(filename: str) -> pygame.Surface:
    """
    Load and return an image from the specified filename.

    Args:
        filename (str): The name of the image file to load.

    Returns:
        pygame.Surface: The loaded image as a pygame Surface object.
    """
    return pygame.transform.scale2x(pygame.image.load(os.path.join(IMAGE_PATH, filename)))


# Loading the ground image
GROUND_IMAGE = load_image("ground.png")

# Loading the backgorund image
BG_IMAGE = load_image("background.png")

# We have 3 differeng bird images for each of the wing positions, so we load all 3 in a list
BIRD_IMAGE = load_image("bird.png")

# Here, we load the pipe image that will be used as the obstacle
PIPE_IMAGE = load_image("pipe.png")

print(BIRD_IMAGE)
print(BG_IMAGE)
print(GROUND_IMAGE)


class Bird:
    """
    Represents a bird object.

    Attributes:
        x (int): The x-coordinate of the bird.
        y (int): The y-coordinate of the bird.
        height (int): The initial height of the bird, same as y.
        velocity (int): The current velocity of the bird, initially 0.
        tick_count (int): A counter used for tracking time from the last bird jump, initially 0.
    """

    def __init__(self, x, y) -> None:
        """
        Initializes a new instance of the Bird class.

        Args:
            x (int): The initial x-coordinate of the bird.
            y (int): The initial y-coordinate of the bird.
        """
        self.x = x
        self.y = y
        self.height = self.y
        self.velocity = 0
        self.tick_count = 0

    def flap(self) -> None:
        """
        Flaps the bird, causing it to jump upwards.
        """
        self.velocity = -10 # The velocity is set to -10, which will cause the bird to move upwards because of the pygame coordinate system.
        self.tick_count = 0 # The tick_count is set to 0, which will be used to track the time from the last jump.
        self.height = self.y # The height is set to the current y-coordinate of the bird.
        
    def move(self) -> None:
        pass
    
bird = Bird(200, 200)

while True:
    bird.move()
    