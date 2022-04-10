import sys
import pygame
from player import Player
from level import Level
from settings import *

# inicjalizacja
pygame.init()
window = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Michal Platformowiec")

# zegar
clock = pygame.time.Clock()

# deklaracja klas
player = Player()
level = Level(window)

# sprites
sprite_group = pygame.sprite.Group()
sprite_group.add(player)

# pętla gry
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] is True:
        player.move_up()
    if keys[pygame.K_DOWN] is True:
        pass
    if keys[pygame.K_LEFT] is True:
        player.move_left()
    if keys[pygame.K_RIGHT] is True:
        player.move_right()

    # aktualizacja klas
    player.update()

    # rysowanie    
    window.fill((0, 100, 255))

    sprite_group.draw(window)
    level.draw()

    pygame.display.flip()
    clock.tick(60)
