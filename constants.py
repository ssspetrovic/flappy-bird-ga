import os
import pygame

WINDOW_DIM = (800, 600)
FPS = 60

IMAGE_PATH = "assets/img"

def load_image2x(filename: str) -> pygame.Surface:
    """
    Load and return an image scaled two times from the specified filename.

    Args:
        filename (str): The name of the image file to load.

    Returns:
        pygame.Surface: The loaded image as a pygame Surface object.
    """
    return pygame.transform.scale2x(pygame.image.load(os.path.join(IMAGE_PATH, filename)))

# Loading the background image
BG_IMAGE = pygame.image.load(os.path.join(IMAGE_PATH, "background_city.png"))

# We have 3 different bird images for each of the wing positions, so we load all 3 in a list
BIRD_IMAGE = load_image2x("bird.png")

# Here, we load the pipe image that will be used as the obstacle
PIPE_BOTTOM_IMAGE = load_image2x("obstacle.png")

# We flip the pipe image vertically to get the top pipe image
PIPE_TOP_IMAGE = pygame.transform.flip(PIPE_BOTTOM_IMAGE, False, True)

TERMINAL_VELOCITY = 15
BIRD_DEFAULT_X = 100
BIRD_DEFAULT_Y = 300

MAX_ROTATION = 25
TILT_SPEED = 2

GENERATIONS = 20
