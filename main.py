import sys
import pygame
from settings import *
from ui import UI
from level import Level
from overworld import Overworld
from particles import ParticleEffect


class Game:
    def __init__(self):
        # game data
        self.max_level = self.load_data()

        # overworld
        self.overworld = Overworld(0, self.max_level, window, self.create_level)
        self.status = 'overworld'

        # UI
        self.ui = UI(window)
        self.current_health = 3
        self.coins = 0
        self.heart_loss_sprites = pygame.sprite.Group()

    def load_data(self):
        try:
            file = open('data/game_data.txt', 'r')
            max_level = int(file.read())
            file.close()
            return max_level
        except:
            file = open('data/game_data.txt', 'w')
            file.write('0')
            file.close()
            return 0

    def save_data(self):
        file = open('data/game_data.txt', 'w')
        file.write(str(self.max_level))
        file.close()

    def create_level(self, current_level):
        self.level = Level(current_level, window, self.create_overworld, self.change_coins, self.reduce_life, self.create_level)
        self.current_health = 3
        self.coins = 0
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, window, self.create_level)
        self.status = 'overworld'

    def change_coins(self, amount=1):
        self.coins += amount

    def reduce_life(self, amount=1):
        if self.current_health > 0:
            self.current_health -= amount
            pos = (37+(self.current_health*70), 37)
            heart_loss = ParticleEffect(pos, 'heart_loss')
            self.heart_loss_sprites.add(heart_loss)
        return self.current_health

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        elif self.status == 'level':
            self.level.run()
            self.ui.show_heath(self.current_health)
            self.ui.show_coins(self.coins)

            self.heart_loss_sprites.update()
            self.heart_loss_sprites.draw(window)


# Game
pygame.init()
window = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Michal Platformowiec")
clock = pygame.time.Clock()

game = Game()

# pętla gry
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.save_data()
            pygame.quit()
            sys.exit()

    # rysowanie
    window.fill('grey')
    game.run()

    pygame.display.update()
    clock.tick(60)
