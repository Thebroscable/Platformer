import pygame
from support import *

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, frames):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.5
        '''
        if type == 'jump':
            self.frames = hero_sprites['herochar_before_jump_dust_anim_strip_4']
        elif type == 'land':
            self.frame = hero_sprites['herochar_after_jump_dust_anim_strip_4']
        elif type == 'strike':
            self.frame = hero_sprites['sword_effect_strip_4']
        elif type == 'sparkle':
            self.frame = hero_sprites['hit_sparkle_anim_strip_4']
        '''
        self.frames = frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self,x_shift):
        self.animate()
        self.rect.x += x_shift
