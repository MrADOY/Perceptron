import random
import os
import pygame

RED = (255,   0,   0)
GREEN = (0, 255,   0)
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)


def sign(n):
    if n >= 0:
        return 1
    else:
        return -1


def map(n, start1, stop1, start2, stop2):
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2


class Line(object):
    """Represent the function """

    def f(self, x):
        """ return x -> ax + b"""
        return 0.1 * x + 0.2

    def draw(self, screen, width, height):
        p1 = Point(-1, self.f(-1))
        p2 = Point(1, self.f(1))
        pygame.draw.line(screen, BLACK, (p1.pixelX(width), p1.pixelY(height)),
                         (p2.pixelX(width), p2.pixelY(height)))


class Perceptron(object):
    """Represent a Perceptron ."""

    def __init__(self, n):
        self._weights = [random.uniform(-1, 1) for i in range(n)]
        self.learningrate = 0.01

    def guess(self, inputs):
        sum_ = 0
        for i in range(len(inputs)):
            sum_ += inputs[i] * self._weights[i]

        return sign(sum_)

    def guessY(self, x):

        w0 = self._weights[0]
        w1 = self._weights[1]
        w2 = self._weights[2]

        return -(w2 / w1) - (w0 / w1) * x

    def train(self, inputs, target):
        guess = self.guess(inputs)
        error = target - guess
        for i in range(len(inputs)):
            self._weights[i] = self._weights[i] + error * inputs[i] * self.learningrate

    def draw(self, screen, width, height):
        p1 = Point(-1, self.guessY(-1))
        p2 = Point(1, self.guessY(1))
        pygame.draw.line(screen, BLACK, (p1.pixelX(width), p1.pixelY(height)),
                         (p2.pixelX(width), p2.pixelY(height)))


class Point(object):
    """Represent a Point."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bias = 1

        line = Line()
        lineY = line.f(x)

        if self.y > lineY:
            self.label = 1
        else:
            self.label = -1

        self.color = BLACK

    def pixelX(self, width):
        return map(self.x, -1, 1, 0, width)

    def pixelY(self, height):
        return map(self.y, -1, 1, height, 0)

    def draw(self, screen, width, height):
        px = self.pixelX(width)
        py = self.pixelY(height)

        if self.label == 1:
            pygame.draw.circle(screen, BLACK, (int(px), int(py)), 8, 2)
            pygame.draw.circle(screen, self.color, (int(px), int(py)), 5)
        else:
            pygame.draw.circle(screen, BLACK, (int(px), int(py)), 8, 6)
            pygame.draw.circle(screen, self.color, (int(px), int(py)), 5)
