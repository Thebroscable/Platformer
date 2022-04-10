import csv
import pygame


def csv_open(file_name):
    file = open(file_name)

    csvreader = csv.reader(file)
    header = next(csvreader)
    rows = []
    for row in csvreader:
        rows.append(row)

    file.close()
    return rows


def resize(path, multi=2):
    sprite = pygame.image.load(path)
    rect = sprite.get_rect()
    sprite = pygame.transform.scale(sprite, (rect.width*multi, rect.height*multi))
    return sprite
