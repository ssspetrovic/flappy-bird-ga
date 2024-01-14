import os
import time
import random

import pygame
import neat

WINDOW_DIM = (800, 600)

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
# BG_IMAGE = load_image("background_city2.png")
BG_IMAGE = pygame.image.load(os.path.join(IMAGE_PATH, "background_city2.png"))

# We have 3 differeng bird images for each of the wing positions, so we load all 3 in a list
BIRD_IMAGE = load_image("bird.png")

# Here, we load the pipe image that will be used as the obstacle
PIPE_IMAGE = load_image("pipe.png")

print(BIRD_IMAGE)
print(BG_IMAGE)
print(GROUND_IMAGE)


TERMINAL_VELOCITY = 20


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
        self.velocity = -15
        self.clicked = False

    def flap(self) -> None:
        """
        Flaps the bird, causing it to jump upwards.
        """
        self.velocity = -25  # The velocity is set to -10, which will cause the bird to move upwards because of the pygame coordinate system.
        # The height is set to the current y-coordinate of the bird.
        self.height = self.y
        self.clicked = True

    def handle_gravity(self) -> None:
        """
        Handles the gravity.
        """
        self.velocity += 2.0  # Increment the t by 1.

        # If the velocity is greater than the terminal velocity, set it to the terminal velocity.
        if self.velocity >= TERMINAL_VELOCITY:
            self.velocity = TERMINAL_VELOCITY

        # Update the y-coordinate of the bird.
        self.y += self.velocity

    def handle_click(self) -> None:
        """
        Handles the click event.
        """
        if pygame.mouse.get_pressed()[0] and self.clicked == False:
            self.flap()

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

    def update(self) -> None:
        self.handle_gravity()
        self.handle_click()

    def draw(self, window) -> None:
        """
        Draws the bird on the specified window.

        Args:
            window (pygame.Surface): The window to draw the bird on.
        """
        window.blit(BIRD_IMAGE, (self.x, self.y))

    def get_mask(self) -> pygame.mask.Mask:
        """
        Gets the mask of the bird.

        Returns:
            pygame.mask.Mask: The mask of the bird.
        """
        return pygame.mask.from_surface(BIRD_IMAGE)


def draw_window(window, bird) -> None:
    """
    Draws the bird and updates the display.

    Args:
        window (pygame.Surface): The game window.
        bird (Bird): The bird object to be drawn.

    This function first draws the bird image at the top-left corner (0, 0) of the window.
    Then it calls the draw method of the bird object, passing the window as an argument.
    Finally, it updates the entire display.
    """
    window.blit(BG_IMAGE, (0, 0))
    bird.draw(window)
    pygame.display.update()


def run():
    window = pygame.display.set_mode(WINDOW_DIM)
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    bird = Bird(200, 200)

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        bird.update()
        draw_window(window, bird)

    pygame.quit()
    quit()


if __name__ == "__main__":
    run()
