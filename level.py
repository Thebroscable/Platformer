import pygame
from settings import *
from support import csv_open


class Level:
    def __init__(self, window):
        self.window = window
        self.map = pygame.Rect(0, screen_size[1] - tile_size, screen_size[0], 32)

    def draw(self):
        pygame.draw.rect(self.window, (0,255,0), self.map)
