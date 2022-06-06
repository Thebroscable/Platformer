import pygame
from os import walk
from csv import reader
from settings import tile_size, size_multiplier, original_tile_size


def load_image(path):
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (image.get_size()[0]*size_multiplier, image.get_size()[1]*size_multiplier))
    return image


def import_folder(path):
    surface_list = []
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = pygame.transform.scale(image_surf,
                                                (image_surf.get_size()[0]*size_multiplier,
                                                 image_surf.get_size()[1]*size_multiplier))
            surface_list.append(image_surf)
    return surface_list


def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map


def import_cut_graphics(path, size=(original_tile_size, original_tile_size)):
    new_size = (size[0] * size_multiplier, size[1] * size_multiplier)
    surface = pygame.image.load(path).convert_alpha()
    surface = pygame.transform.scale(surface,
                                     (surface.get_size()[0]*size_multiplier, surface.get_size()[1]*size_multiplier))
    tile_num_x = int(surface.get_size()[0] / new_size[0])
    tile_num_y = int(surface.get_size()[1] / new_size[1])

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * new_size[0]
            y = row * new_size[1]
            new_surf = pygame.Surface((new_size[0], new_size[1]), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, new_size[0], new_size[1]))
            cut_tiles.append(new_surf)

    return cut_tiles
