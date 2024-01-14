import os
import random

import pygame
import neat

pygame.font.init()


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


# Loading the background image
BG_IMAGE = pygame.image.load(os.path.join(IMAGE_PATH, "background_city.png"))

# We have 3 different bird images for each of the wing positions, so we load all 3 in a list
BIRD_IMAGE = load_image("bird.png")

# Here, we load the pipe image that will be used as the obstacle
PIPE_BOTTOM_IMAGE = load_image("obstacle.png")
# We flip the pipe image vertically to get the top pipe image
PIPE_TOP_IMAGE = pygame.transform.flip(PIPE_BOTTOM_IMAGE, False, True)

TERMINAL_VELOCITY = 8


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
        self.velocity = -5
        self.clicked = False

    def flap(self) -> None:
        """
        Flaps the bird, causing it to jump upwards.
        """
        self.velocity = -15
        self.height = self.y
        self.clicked = True

    def handle_gravity(self) -> None:
        """
        Handles the gravity.
        """
        self.velocity += 0.75

        if self.velocity >= TERMINAL_VELOCITY:
            self.velocity = TERMINAL_VELOCITY

        self.y += self.velocity

    def handle_click(self) -> None:
        """
        Handles the click event.
        """
        if pygame.mouse.get_pressed()[0] and not self.clicked:
            self.flap()

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

    def update(self) -> None:
        self.handle_gravity()
        self.handle_click()

    def render(self, surface) -> None:
        """
        Renders the bird on the specified surface.

        Args:
            surface (pygame.Surface): The surface to render the bird on.
        """
        surface.blit(BIRD_IMAGE, (self.x, self.y))

    def get_mask(self) -> pygame.mask.Mask:
        """
        Gets the mask of the bird.

        Returns:
            pygame.mask.Mask: The mask of the bird.
        """
        return pygame.mask.from_surface(BIRD_IMAGE)


class Obstacle:
    """
    Represents an obstacle (pipe) object.

    Attributes:
        x (int): The x-coordinate of the obstacle.
        y_bottom (int): The y-coordinate of the bottom of the pipe.
        y_top (int): The y-coordinate of the top of the pipe.
        passed (bool): Indicates whether the bird has passed through the obstacle.
        gap (int): The gap between the top and bottom pipes.
        velocity (int): The velocity of the obstacle.
        height (int): The height of the gap.
    """

    def __init__(self, x) -> None:
        """
        Initializes a new instance of the Obstacle class.

        Args:
            x (int): The initial x-coordinate of the obstacle.
        """
        self.x = x
        self.y_bottom = 0
        self.y_top = 0
        self.width = PIPE_BOTTOM_IMAGE.get_width()

        self.passed = False

        self.gap = 215
        self.velocity = 5

        self.update_y()

    def update_y(self):
        """
        Updates the y-coordinates of the top and bottom pipes.
        """
        self.height = random.randrange(100, 300)
        self.y_bottom = self.height + self.gap
        self.y_top = self.height - PIPE_TOP_IMAGE.get_height()

    def update(self) -> None:
        """
        Updates the x-coordinate of the obstacle based on its velocity.
        """
        self.x -= self.velocity

    def render(self, surface) -> None:
        """
        Renders the top and bottom pipe images on the given surface.

        Args:
            surface (pygame.Surface): The game surface.

        This method renders the top pipe image at the coordinates (self.x, self.y_top)
        and the bottom pipe image at the coordinates (self.x, self.y_bottom) on the given surface.
        """
        surface.blit(PIPE_BOTTOM_IMAGE, (self.x, self.y_bottom))
        surface.blit(PIPE_TOP_IMAGE, (self.x, self.y_top))

    def get_mask_top(self) -> pygame.mask.Mask:
        """
        Gets the mask of the top part of the pipe.

        Returns:
            pygame.mask.Mask: The mask of the top part of the pipe.
        """
        return pygame.mask.from_surface(PIPE_TOP_IMAGE)

    def get_mask_bottom(self) -> pygame.mask.Mask:
        """
        Gets the mask of the bottom part of the pipe.

        Returns:
            pygame.mask.Mask: The mask of the bottom part of the pipe.
        """
        return pygame.mask.from_surface(PIPE_BOTTOM_IMAGE)

    def check_collision(self, bird: Bird) -> bool:
        """
        Checks for collision between the bird and the pipe.

        Args:
            bird (Bird): The bird object.

        Returns:
            bool: True if there is a collision, False otherwise.
        """
        bird_mask = bird.get_mask()

        bottom_mask = self.get_mask_bottom()
        top_mask = self.get_mask_top()

        bottom_offset = (self.x - bird.x, self.y_bottom - round(bird.y))
        top_offset = (self.x - bird.x, self.y_top - round(bird.y))

        # Check for collision with the bottom pipe
        bottom_collision_point = bird_mask.overlap(bottom_mask, bottom_offset)

        # Check for collision with the top pipe
        top_collision_point = bird_mask.overlap(top_mask, top_offset)

        return bottom_collision_point or top_collision_point


def render_window(surface: pygame.Surface, bird: Bird, obstacles: list[Obstacle], score: int) -> None:
    """
    Renderds the bird, obstacles, and updates the display.

    Args:
        surface (pygame.Surface): The game surface.
        bird (Bird): The bird object to be rendered.
        obstacles (list[Obstacle]): The list of obstacles (pipes).
        score (int): The current score.

    This function first renders the background image at the top-left corner (0, 0) of the surface.
    Then it calls the render method of each obstacle in the obstacles list, passing the surface as an argument.
    After that, it renders the bird on the surface. Finally, it updates the entire display.
    """
    surface.blit(BG_IMAGE, (0, 0))

    for obstacle in obstacles:
        obstacle.render(surface)

    bird.render(surface)

    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    surface.blit(text, (10, 10))

    pygame.display.update()


def restart_game():
    return Bird(200, 200), [Obstacle(800)], 0


def run_game():
    surface = pygame.display.set_mode(WINDOW_DIM)
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    bird, obstacles, score = restart_game()

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        bird.update()

        if bird.y > WINDOW_DIM[1] or bird.y < -150:
            # Bird went out of the top or bottom of the window - end the game
            bird, obstacles, score = restart_game()

        for obstacle in obstacles:
            obstacle.update()
            if obstacle.x < bird.x and not obstacle.passed:
                obstacle.passed = True
                score += 1

            if obstacle.check_collision(bird):
                bird, obstacles, score = restart_game()
                break

        # Check if it's time to spawn a new pipe
        if obstacles[-1].x < WINDOW_DIM[0] - 300:
            obstacles.append(Obstacle(WINDOW_DIM[0]))

        # Remove obstacles that are off the screen
        obstacles = [
            obstacle for obstacle in obstacles if obstacle.x > -obstacle.width]

        render_window(surface, bird, obstacles, score)

    # Game over - restart the game
    bird, obstacles, score = restart_game()
    run_game(surface, clock, bird, obstacles, score)


def run_neat():
    neat_cfg = neat.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        "config/neat_cfg.txt"
    )

    population = neat.Population(neat_cfg)
    
    # best_genome = population.run(run_game_neat, 50)

if __name__ == "__main__":
    run_game()
