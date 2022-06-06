import pygame
from tiles import AnimatedTile


class Enemy(AnimatedTile):
    def __init__(self, pos, size, path, resize=(32, 32)):
        super().__init__(pos, size, path, resize)
        self.speed = 3

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()


class Slime(Enemy):
    def __init__(self, pos, size):
        path = 'data/sprites/enemies/slime/slime_walk.png'
        super().__init__(pos, size, path)


class Goblin(Enemy):
    def __init__(self, pos, size):
        path = 'data/sprites/enemies/goblin/goblin_run.png'
        super().__init__(pos, size, path, (16, 16))
        self.speed = 5


class Worm(Enemy):
    def __init__(self, pos, size):
        path = 'data/sprites/enemies/worm/worm_walk.png'
        super().__init__(pos, size, path, (16, 8))
        self.rect.y += size - self.image.get_size()[1]


class Mushroom(Enemy):
    def __init__(self, pos, size):
        path = 'data/sprites/enemies/mushroom/mushroom_walk.png'
        super().__init__(pos, size, path, (16, 16))
        self.speed = 4
