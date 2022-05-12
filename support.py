import csv
from numpy import tile
import pygame
import os
from settings import *


def csv_open(file_name):
    file = open(file_name)

    csvreader = csv.reader(file)
    header = next(csvreader)
    rows = []
    for row in csvreader:
        rows.append(row)

    file.close()
    return rows


def image_resize(image, multi=2):
    rect = image.get_rect()
    return pygame.transform.scale(image, (rect.width*multi, rect.height*multi))


def image_loader(path: str) -> str:
    for i in os.listdir(path):
        yield ((os.path.splitext(i)[0]),
                pygame.image.load(path + i).convert_alpha())


def image_separator(dict):
    for i, key in enumerate(dict.keys()):
        temp = []
        for j in range(int(key[-1])):
            temp.append(dict[key].subsurface(j*tile_size, 0, tile_size, tile_size))
        dict[key] = temp
    return dict
