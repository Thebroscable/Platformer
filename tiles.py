import pygame
from support import import_cut_graphics, load_image
from settings import tile_size, screen_size


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, shift):
        self.rect.x += shift


class StaticTile(Tile):
    def __init__(self, pos, size, surface):
        super().__init__(pos, size)
        self.image = surface


class AnimatedTile(Tile):
    def __init__(self, pos, size, path, real_size=(tile_size, tile_size)):
        super().__init__(pos, size)
        self.frames = import_cut_graphics(path, real_size)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift=0):
        self.animate()
        self.rect.x += shift


class Trap(StaticTile):
    def __init__(self, pos, size, surface):
        super().__init__(pos, size, surface)
        self.activate = False

    def update(self, player, shift=0):
        super().update(shift)
        if self.rect.x <= player.sprite.rect.x <= self.rect.x+tile_size:
            self.activate = True
        if self.activate:
            self.rect.y += 6
        if self.rect.y > screen_size[1]:
            self.kill()


class Door(StaticTile):
    def __init__(self, pos, size):
        surface = load_image('data/sprites/miscellaneous/door.png')
        super().__init__(pos, size, surface)
        self.rect.y -= 30


class Coin(AnimatedTile):
    def __init__(self, pos, size):
        path = 'data/sprites/coins/coin_anim.png'
        super().__init__(pos, size, path, (8, 8))
        center_x = pos[0] + int(size/2)
        center_y = pos[1] + int(size/2)
        self.rect = self.image.get_rect(center=(center_x, center_y))


class Orb(AnimatedTile):
    def __init__(self, pos, size):
        path = 'data/sprites/coins/orb_anim.png'
        super().__init__(pos, size, path, (8, 8))
        center_x = pos[0] + int(size/2)
        center_y = pos[1] + int(size/2)
        self.rect = self.image.get_rect(center=(center_x, center_y))


class Slab(StaticTile):
    def __init__(self, pos, size, surface):
        surface = load_image(surface)
        super().__init__(pos, size, surface)

