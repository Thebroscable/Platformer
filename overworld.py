import pygame
from game_data import levels
from settings import size_multiplier, tile_size
from support import import_cut_graphics
from tiles import StaticTile, AnimatedTile


class Node(StaticTile):
    def __init__(self, pos, surface, status):
        size = 7 * size_multiplier
        super().__init__(pos, size, surface)


class Cursor(AnimatedTile):
    def __init__(self, pos):
        size = 12 * size_multiplier
        path = 'data/sprites/hud/select_icon.png'
        real_size = (12, 12)
        pos = (pos[0]-tile_size, pos[1]-10)
        super().__init__(pos, size, path, real_size)

    def change_pos(self, new_pos):
        self.rect.x = new_pos[0]-tile_size
        self.rect.y = new_pos[1]-10


class Overworld:
    def __init__(self, start_level, max_level, surface, create_level):
        self.create_level = create_level

        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level

        self.level_sprites = self.setup_nodes()
        self.cursor_sprite = pygame.sprite.GroupSingle()

        pos = levels[self.current_level]['node_pos']
        cursor = Cursor(pos)
        self.cursor_sprite.add(cursor)

    def setup_nodes(self):
        level_sprites = pygame.sprite.Group()
        nodes = import_cut_graphics('data/sprites/hud/fonts.png', (7, 7))
        step = tile_size - 30

        for i, level in enumerate(levels):
            status = 1 if self.max_level >= i else 0
            # L
            node = Node((level['node_pos'][0], level['node_pos'][1]), nodes[21], status)
            level_sprites.add(node)
            # E
            node = Node((level['node_pos'][0]+step, level['node_pos'][1]), nodes[14], status)
            level_sprites.add(node)
            # V
            node = Node((level['node_pos'][0]+step*2, level['node_pos'][1]), nodes[31], status)
            level_sprites.add(node)
            # E
            node = Node((level['node_pos'][0]+step*3, level['node_pos'][1]), nodes[14], status)
            level_sprites.add(node)
            # L
            node = Node((level['node_pos'][0]+step*4, level['node_pos'][1]), nodes[21], status)
            level_sprites.add(node)
            # number
            node = Node((level['node_pos'][0]+step*5, level['node_pos'][1]), nodes[i+1], status)
            level_sprites.add(node)

        return level_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        prev_level = self.current_level

        if keys[pygame.K_RIGHT]:
            if prev_level == 0:
                self.current_level = 1
            elif prev_level == 2:
                self.current_level = 3
        elif keys[pygame.K_LEFT]:
            if prev_level == 1:
                self.current_level = 0
            elif prev_level == 3:
                self.current_level = 2
        elif keys[pygame.K_UP]:
            if prev_level == 2:
                self.current_level = 0
            elif prev_level == 3:
                self.current_level = 1
        elif keys[pygame.K_DOWN]:
            if prev_level == 0:
                self.current_level = 2
            elif prev_level == 1:
                self.current_level = 3
        elif keys[pygame.K_RETURN]:
            self.create_level(levels[self.current_level])

        if self.current_level > self.max_level:
            self.current_level = prev_level

        pos = levels[self.current_level]['node_pos']
        self.cursor_sprite.sprite.change_pos(pos)

    def draw_dark_rect(self):
        step = tile_size - 30

        if self.max_level < 3:
            pygame.draw.rect(self.display_surface,
                             'black',
                             pygame.rect.Rect(levels[3]['node_pos'][0], levels[3]['node_pos'][1], step*6, 30))
        if self.max_level < 2:
            pygame.draw.rect(self.display_surface,
                             'black',
                             pygame.rect.Rect(levels[2]['node_pos'][0], levels[2]['node_pos'][1], step * 6, 30))
        if self.max_level < 1:
            pygame.draw.rect(self.display_surface,
                             'black',
                             pygame.rect.Rect(levels[1]['node_pos'][0], levels[1]['node_pos'][1], step * 6, 30))

    def run(self):
        self.input()

        self.level_sprites.draw(self.display_surface)
        self.draw_dark_rect()

        self.cursor_sprite.draw(self.display_surface)
        self.cursor_sprite.update()
