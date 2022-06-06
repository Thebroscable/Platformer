import pygame
from support import load_image, import_cut_graphics


class UI:
    def __init__(self, surface):
        self.display_surface = surface

        # health
        self.heart = load_image('data/sprites/hud/hearts_hud.png')

        # coins
        self.coin = load_image('data/sprites/hud/coins_hud.png')

        # numbers
        self.numbers = import_cut_graphics('data/sprites/hud/fonts.png', (7, 7))[0:10]

    def show_heath(self, current_heath):
        for i in range(current_heath):
            self.display_surface.blit(self.heart, (5+(i*70), 5))

    def show_coins(self, amount):
        self.display_surface.blit(self.coin, (15, 96))

        amount = str(amount)
        for i, num in enumerate(amount):
            self.display_surface.blit(self.numbers[int(num)], (60+(i*32), 100))
