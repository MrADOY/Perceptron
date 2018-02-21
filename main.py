#!/usr/bin/env python3


"""This module contains the core of this application."""


import os
import pygame
import random
from contextlib import contextmanager
from entity import Perceptron
from entity import Point
from entity import Line

RED = (255,   0,   0)
GREEN = (0, 255,   0)
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)


class Core(object):

    SIZE = WIDTH, HEIGHT = 500, 500
    TITLE = "Perceptron"

    def __init__(self):
        self._screen = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption(self.TITLE)
        self._done = False
        self.line = Line()
        self.lineByPerceptron = Line()
        self._points = [Point(random.uniform(-1, 1), random.uniform(-1, 1))
                        for _ in range(50)]
        self.training_point = Point(random.uniform(-1, 1), random.uniform(-1, 1))
        self.trainingIndex = 0
        self.brain = Perceptron(3)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._done = True

    def _draw(self):
        """ Draw all the entities """

        self._screen.fill((255, 255, 255))

        # Draw all the points
        for point in self._points:
            point.draw(self._screen, self.WIDTH, self.HEIGHT)

        # draws the curve of the function
        self.line.draw(self._screen, self.WIDTH, self.HEIGHT)

        # draws the curve of the neural network

        self.brain.draw(self._screen, self.WIDTH, self.HEIGHT)

        pygame.display.flip()

    def _update(self):
        """Updates all the entities and train the neural network"""

        for point in self._points:
            inputs = [point.x, point.y, point.bias]
            guess = self.brain.guess(inputs)
            if guess == point.label:
                point.color = GREEN
            else:
                point.color = RED

        # The point that serves as a training
        input_training = [self.training_point.x,
                          self.training_point.y, self.training_point.bias]
        self.brain.train(input_training, self.training_point.label)
        self.training_point = Point(random.uniform(-1, 1), random.uniform(-1, 1))

    def run(self):
        """Run the main game loop.

        It handles the events, updates the state, draws to the screen and
        restricts the frame rate.


        """

        while not self._done:
            self._handle_events()
            self._update()
            self._draw()


@contextmanager
def pygame_context():
    """Initialize pygame, then clean up when done."""
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    try:
        yield
    finally:
        pygame.quit()


def main():
    """Prepare the environment, then launch the system."""
    with pygame_context():
        Core().run()


if __name__ == '__main__':
    main()
