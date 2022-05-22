import pygame, sys
from settings import *
from support import *
from tiles import Tile
from settings import tile_size


class Level:
    def __init__(self,level_data, window):
        self.window = window
        self.map = pygame.Rect(0, screen_size[1] - tile_size, screen_size[0], 32)
        self.level_data = level_data

        terrain_layout = import_csv_layout(level_data['tlo'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'tlo')
        self.setup_level(level_data)

    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'objects':
                        sprite = Tile(tile_size,x,y)
                        sprite_group.add(sprite)

        return sprite_group

    def setup_level(self,layout):
        self.tiles=pygame.sprite.Group
        for row_index,row in enumerate(layout):
            for col_index, cell in enumerate(layout):
                if cell == 'X':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    tile = Tile((x,y),tile_size)
                    self.tiles.add(tile)



    # def draw(self):
    #     pygame.draw.rect(self.window, (0,255,0), self.map)

    def run(self):
        self.terrain_sprites.draw(self.window)
        self.terrain_sprites.update(self.window)
        self.tiles.update(1)
        self.tiles.draw(self.window)