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
        self.frame_speed = 0.1
        self.image = self.sprites['herochar_idle_anim_strip_4'][self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

        self.accel = 0.5
        self.fall_accel = 1
        self.max_speed = 5
        self.max_fall_speed = 15
        self.change_x = 0
        self.change_y = 0
        self.jump_speed = 15
        self.jump_accel = 0.5
        self.jump_count = 1
        self.direction = 'right'
        self.state = 'herochar_idle_anim_strip_4'

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
        if self.change_x > 0:
            self.change_x -= self.accel / 2
        elif self.change_x < 0:
            self.change_x += self.accel / 2

    def is_falling(self):
        '''Czy gracz spada - return True/False'''
        if self.change_y > 0:
            return True
        else:
            return False

    def change_sprite(self):
        self.current_sprite += self.frame_speed + abs(self.change_x) * (self.frame_speed / self.max_speed)
        list_len = len(self.sprites[self.state])
        list_index = int(self.current_sprite)
        self.image = self.sprites[self.state][list_index % list_len]

    def change_direction(self):
        if self.direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)

    def change_state(self, keys):
        prev_state = self.state

        if self.change_x == 0 and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.state = 'herochar_idle_anim_strip_4'
        else:
            self.state = 'herochar_run_anim_strip_6'

        if prev_state != self.state:
            self.current_sprite = 0