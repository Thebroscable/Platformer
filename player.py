import pygame
from settings import *
from support import resize


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        pos_x = tile_size
        pos_y = screen_size[1] - tile_size * 2

        self.sprites = self.load_sprites()
        self.current_sprite = 0
        self.image = self.sprites[0][0][self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

        self.accel = 0.25
        self.fall_accel = 1
        self.change_x = 0
        self.change_y = 0
        self.max_speed = 5
        self.max_fall_speed = 15
        self.jump_count = 1
        self.direction = 'right'
        self.status = 'idle'

    def move_right(self):
        '''Ruch w prawo gracza'''
        if self.change_x < self.max_speed:
            self.change_x += self.accel
        self.direction = 'right'
        self.status = 'run'

    def move_left(self):
        '''Ruch w lewo gracza'''
        if abs(self.change_x) < self.max_speed:
            self.change_x -= self.accel
        self.direction = 'left'
        self.status = 'run'

    def move_up(self):
        '''Skok gracza'''
        if self.is_grounded() and self.jump_count:
            self.change_y -= 15
            self.status = 'jump'
            self.jump_count -= 1
        if not self.is_grounded() and not self.is_falling():
            self.change_y -= 0.5
            self.status = 'jump'

    def idle(self):
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

    def gravity(self):
        '''Działanie grawitacji'''
        if not self.is_grounded():
            if self.change_y < self.max_fall_speed:
                self.change_y += self.fall_accel
        else:
            self.change_y = 0

    def manage_sprites(self, increment, index1, index2):
        self.current_sprite += increment
        if self.current_sprite >= len(self.sprites[index1][index2]):
            self.current_sprite = 0
        if self.direction == 'left':
            self.image = pygame.transform.flip(self.sprites[index1][index2][int(self.current_sprite)], True, False)
        else:
            self.image = self.sprites[index1][index2][int(self.current_sprite)]

    def update(self):
        '''Aktualizacja stanu gracza'''
        self.rect.top += self.change_y
        self.rect.left += self.change_x

        if self.is_grounded():
            self.jump_count = 1

        self.gravity()
        self.update_sprites()

        if self.status == 'idle':
            self.idle()
        self.status = 'idle'

    def update_sprites(self):
        if self.status == 'idle':
            self.manage_sprites(0.1, 0, 0)
        elif self.status == 'run':
            self.manage_sprites(0.2, 0, 1)

    def load_sprites(self):
        idle = [
            resize(player_sprites["without_sword"]["idle_1"]),
            resize(player_sprites["without_sword"]["idle_2"]),
            resize(player_sprites["without_sword"]["idle_3"]),
            resize(player_sprites["without_sword"]["idle_4"]),
            resize(player_sprites["without_sword"]["idle_5"])
        ]

        run = [
            resize(player_sprites["without_sword"]["run_1"]),
            resize(player_sprites["without_sword"]["run_2"]),
            resize(player_sprites["without_sword"]["run_3"]),
            resize(player_sprites["without_sword"]["run_4"]),
            resize(player_sprites["without_sword"]["run_5"]),
            resize(player_sprites["without_sword"]["run_5"])
        ]

        without_sword = [idle, run]

        return [without_sword]
