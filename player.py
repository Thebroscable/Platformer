import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, create_jump_particles, create_attack_particles):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.10
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # particles
        self.create_jump_particles = create_jump_particles
        self.create_attack_particles = create_attack_particles

        # movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4
        self.gravity = 0.8
        self.jump_speed = -16

        # stats
        self.attack_cooldown = 0
        self.invincibility = 0

        # state
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # sound
        self.sword_sound = pygame.mixer.Sound('data/sounds/sword.wav')
        self.jump_sound = pygame.mixer.Sound('data/sounds/jump.wav')

    def import_character_assets(self):
        character_path = 'data/sprites/hero/'
        self.animations = {'idle': [], 'run': [], 'jump': [],
                           'fall': [], 'attack': [],
                           'death': [], 'hit': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        # wczytanie animacji
        animation = self.animations[self.status]

        # animowanie
        if self.status == 'attack' or self.status == 'hit':
            self.frame_index += 0.4
        else:
            self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            if self.status == 'attack' or self.status == 'hit':
                self.status = 'idle'
                animation = self.animations[self.status]
            self.frame_index = 0

        # zmiana kierunku
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.status != 'attack' and self.attack_cooldown <= 0:
            self.create_attack_particles(self.rect.topleft)
            self.status = 'attack'
            self.attack_cooldown = 60
            self.sword_sound.play()

        if keys[pygame.K_UP] and self.on_ground and self.status != 'attack':
            self.jump()
            self.create_jump_particles(self.rect.midbottom)
            self.jump_sound.play()

        if keys[pygame.K_RIGHT] and self.status != 'attack':
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT] and self.status != 'attack':
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

    def get_status(self):
        prev_state = self.status

        if self.status != 'attack' and self.status != 'hit':
            if self.direction.y < 0:
                self.status = 'jump'
            elif self.direction.y > 1:
                self.status = 'fall'
            else:
                if self.direction.x != 0:
                    self.status = 'run'
                else:
                    self.status = 'idle'

        if self.status != prev_state:
            self.frame_index = 0

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def countdown(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.invincibility > 0:
            self.invincibility -= 1

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.countdown()
