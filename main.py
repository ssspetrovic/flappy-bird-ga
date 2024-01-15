import os
import random

import pygame
import neat

from constants import *

generations_count = 0

pygame.font.init()
SURFACE = pygame.display.set_mode(WINDOW_DIM)
pygame.display.set_caption("Flappy Bird")


class Bird:
    """
    Represents a bird object.

    Attributes:
        x (int): The x-coordinate of the bird.
        y (int): The y-coordinate of the bird.
        height (int): The initial height of the bird, same as y.
        velocity (int): The current velocity of the bird, initially 0.
        tick_count (int): A counter used for tracking time from the last bird jump, initially 0.
        clicked (bool): Indicates whether the bird has been clicked to flap.
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
        self.velocity += 0.8

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
        """
        Updates the bird's position and handles user input.
        """
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
        self.velocity = 3

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


def draw_info(surface: pygame.Surface, birds: list[Bird], obstacles: list[Obstacle], score: int, generations_count: int) -> None:
    """
    Draws score and generation information on the game surface.

    Args:
        surface (pygame.Surface): The game surface.
        birds (list[Bird]): List of bird objects.
        obstacles (list[Obstacle]): List of obstacle objects.
        score (int): The current score.
        generations_count (int): The current generation count.
    """
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    surface.blit(text, (10, 500))
    text = font.render(f"Current generation: {
                       generations_count}", True, (0, 0, 0))
    surface.blit(text, (10, 530))
    text = font.render(f"Population size: {len(birds)}", True, (0, 0, 0))
    surface.blit(text, (10, 560))


def render_surface(birds: list[Bird], obstacles: list[Obstacle], score: int) -> None:
    """
    Renders the bird, obstacles, and updates the display.

    Args:
        surface (pygame.Surface): The game surface.
        birds (list[Bird]): List of bird objects.
        obstacles (list[Obstacle]): List of obstacle objects.
        score (int): The current score.
    """
    global generations_count
    SURFACE.blit(BG_IMAGE, (0, 0))

    for obstacle in obstacles:
        obstacle.render(SURFACE)

    for bird in birds:
        bird.render(SURFACE)

    draw_info(SURFACE, birds, obstacles, score, generations_count)

    pygame.display.update()


def get_obstacle_index(birds, obstacles):
    """
    Gets the index of the active obstacle based on the bird's position.

    Args:
        birds: List of bird objects.
        obstacles: List of obstacle objects.

    Returns:
        int: The index of the active obstacle.
    """
    if len(birds) > 0:
        return 1 if len(obstacles) > 1 and birds[0].x > obstacles[0].x + PIPE_TOP_IMAGE.get_width() else 0


def remove_data(birds: list[Bird], ges: list[neat.DefaultGenome], networks: list[neat.nn.FeedForwardNetwork], i: int, bird: Bird):
    """
    Removes data related to a bird from lists.

    Args:
        birds (list[Bird]): List of bird objects.
        ges (list[neat.DefaultGenome]): List of genomes.
        networks (list[neat.nn.FeedForwardNetwork]): List of neural networks.
        i (int): Index of the bird to be removed.
        bird (Bird): The bird object to be removed.
    """
    birds.remove(bird)
    ges[i].fitness -= 1
    networks.pop(i)
    ges.pop(i)


def evaluate_genomes(genomes, config):
    """
    Evaluates the fitness of each genome in a generation.

    Args:
        genomes: List of genomes.
        config: NEAT configuration.

    Returns:
        None
    """

    global generations_count
    generations_count += 1

    ges = []
    networks = []

    obstacles = [Obstacle(WINDOW_DIM[0])]
    birds = []
    score = 0

    clock = pygame.time.Clock()

    for _, genome in genomes:
        genome.fitness = 0
        ges.append(genome)
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        birds.append(Bird(BIRD_DEFAULT_X, BIRD_DEFAULT_Y))

    run = True
    while run and len(birds) > 0:
        render_surface(birds, obstacles, score)
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        obstacle_index = get_obstacle_index(birds, obstacles)

        for i, bird in enumerate(birds):
            bird.update()

            input_data = (
                bird.y,
                abs(bird.y - obstacles[obstacle_index].height),
                abs(bird.y - obstacles[obstacle_index].y_bottom)
            )

            output = networks[i].activate(input_data)[0]

            if output > 0.4:
                bird.flap()

            ges[i].fitness += 0.1

        increase_score = False

        for obstacle in obstacles:
            for i, bird in enumerate(birds):
                if bird.y > WINDOW_DIM[1] or bird.y < 0:
                    remove_data(birds, ges, networks, i, bird)

                if obstacle.x < bird.x and not obstacle.passed:
                    obstacle.passed = True
                    increase_score = True

                if obstacle.check_collision(bird):
                    remove_data(birds, ges, networks, i, bird)
                    break

            obstacle.update()

            if increase_score:
                increase_score = False
                score += 1
                for genome in ges:
                    genome.fitness += 5

        # Check if it's time to spawn a new obstacle
        if obstacles[-1].x < WINDOW_DIM[0] - 300:
            obstacles.append(Obstacle(WINDOW_DIM[0]))

        # Remove obstacles that are off the screen
        obstacles = [
            obstacle for obstacle in obstacles if obstacle.x > -obstacle.width]


def run_neat(config_file):
    """
    Runs NEAT algorithm with the provided configuration file.

    Args:
        config_file (str): Path to the NEAT configuration file.

    Returns:
        None
    """
    neat_cfg = neat.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_file
    )

    # Creating the population
    population = neat.Population(neat_cfg)

    # Performance tracker for the generations
    population.add_reporter(neat.StdOutReporter(True))

    # Performing the training
    population.run(evaluate_genomes, GENERATIONS)


if __name__ == "__main__":
    config_file = os.path.join('config', 'neat_cfg.txt')
    run_neat(config_file)
