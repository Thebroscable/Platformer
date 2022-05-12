import pygame
from settings import *
from support import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        pos_x = tile_size
        pos_y = screen_size[1] - tile_size * 8

        images = dict(image_loader(paths['hero']))
        self.sprites = image_separator(images)
        for key in self.sprites:
            for i, img in enumerate(self.sprites[key]):
                self.sprites[key][i] = image_resize(img, resize_multi)

        self.current_sprite = 0
        self.image = self.sprites['herochar_idle_anim_strip_4'][self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

        self.accel = 0.25
        self.fall_accel = 1
        self.max_speed = 5
        self.max_fall_speed = 15
        self.change_x = 0
        self.change_y = 0
        self.jump_speed = 15
        self.jump_accel = 0.5
        self.jump_count = 1
        self.direction = 'right'
        self.state = 'idle'

    def move_right(self):
        '''Ruch w prawo gracza'''
        if self.change_x + self.accel < self.max_speed:
            self.change_x += self.accel
        else:
            self.change_x = self.max_speed
        self.direction = 'right'

    def move_left(self):
        '''Ruch w lewo gracza'''
        if self.change_x - self.accel > -self.max_speed:
            self.change_x -= self.accel
        else:
            self.change_x = -self.max_speed
        self.direction = 'left'

    def jump(self):
        '''Skok gracza'''
        if self.jump_count:
            self.change_y -= self.jump_speed
            self.jump_count -= 1
        if not self.jump_count and not self.is_falling():
            self.change_y -= self.jump_accel

    def fall(self):
        '''spadek gracza'''
        if self.change_y + self.fall_accel < self.max_fall_speed:
            self.change_y += self.fall_accel
        else:
            self.change_y = self.max_fall_speed

    def friction(self):
        '''Hamowanie gracza'''
        if abs(self.change_x) < 0.5:
            self.change_x = 0
        else:
            self.change_x *= 0.9

    def is_grounded(self):
        '''Czy gracz dotyka ziemi - return True/False'''
        if self.rect.top >= (screen_size[1] - tile_size * 3):
            self.rect.top = (screen_size[1] - tile_size * 3)
            return True
        else:
            return False

    def is_falling(self):
        '''Czy gracz spada - return True/False'''
        if self.change_y > 0:
            return True
        else:
            return False
