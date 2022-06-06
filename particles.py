import pygame
from support import import_folder, import_cut_graphics


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.4

        if type == 'jump':
            self.frames = import_folder('data/sprites/hero/before_jump_p')
        elif type == 'land':
            self.frames = import_folder('data/sprites/hero/after_jump_p')
        elif type == 'attack':
            self.frames = import_folder('data/sprites/hero/sword_effect_p')
        elif type == 'heart_loss':
            self.frames = import_cut_graphics('data/sprites/hud/lost_hearts.png')
        elif type == 'coin':
            self.frames = import_cut_graphics('data/sprites/coins/coin_pickup.png', (8, 16))
        elif type == 'hit':
            self.frames = import_folder('data/sprites/hero/hit_sparkle_p')

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def flip(self):
        for i, image in enumerate(self.frames):
            self.frames[i] = pygame.transform.flip(image, True, False)

    def update(self, x_shift=0):
        self.animate()
        self.rect.x += x_shift
