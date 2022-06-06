import pygame
from settings import tile_size, screen_size
from tiles import StaticTile, Coin, Slab, Orb, Tile, Door, Trap
from enemy import Goblin, Worm, Mushroom
from player import Player
from particles import ParticleEffect
from support import import_csv_layout, import_cut_graphics, load_image


class Level:
    def __init__(self, level_data, window, create_overworld, change_coins, reduce_life, create_level):
        self.create_overworld = create_overworld
        self.display_surface = window
        self.world_shift = 0

        # UI
        self.change_coins = change_coins
        self.reduce_life = reduce_life
        self.create_level = create_level
        self.level_data = level_data
        self.current_health = 3

        # player
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.attack_sprite = pygame.sprite.Group()
        self.hit_sprite = pygame.sprite.Group()
        player_layout = import_csv_layout(level_data['player'])
        self.player_setup(player_layout)

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # terrain
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # slabs
        slabs_layout = import_csv_layout(level_data['slabs'])
        self.slabs_sprites = self.create_tile_group(slabs_layout, 'slabs')

        # decorations
        decorations_layout = import_csv_layout(level_data['decorations'])
        self.decorations_sprites = self.create_tile_group(decorations_layout, 'decorations')

        # coins
        self.coin_pickup = pygame.sprite.Group()
        coins_layout = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coins_layout, 'coins')

        # enemies
        enemies_layout = import_csv_layout(level_data['enemies'])
        self.enemies_sprites = self.create_tile_group(enemies_layout, 'enemies')

        # constraints
        constraints_layout = import_csv_layout(level_data['constraints'])
        self.constraints_sprites = self.create_tile_group(constraints_layout, 'constraints')

        # traps
        traps_layout1 = import_csv_layout(level_data['traps1'])
        traps_layout2 = import_csv_layout(level_data['traps2'])
        self.traps_sprites = self.create_tile_group(traps_layout1, 'traps1')
        self.traps_spike_sprites = self.create_tile_group(traps_layout2, 'traps2')

        # background
        bg1 = pygame.image.load('data/sprites/tiles/background.png').convert_alpha()
        bg2 = pygame.image.load('data/sprites/tiles/bg_2.png').convert_alpha()
        self.bg1 = pygame.transform.scale(bg1, screen_size)
        self.bg2 = pygame.transform.scale(bg2, screen_size)

        # sounds
        self.coin_sound = pygame.mixer.Sound('data/sounds/pickup.wav')
        self.land_sound = pygame.mixer.Sound('data/sounds/land.wav')
        self.hit_sound = pygame.mixer.Sound('data/sounds/hit.wav')

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Door((x, y), tile_size)
                    self.goal.add(sprite)
                if val == '1':
                    sprite = Player((x, y), self.create_jump_particles, self.create_attack_particles)
                    self.player.add(sprite)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        tile_list = import_cut_graphics('data/sprites/tiles/tileset.png')
                        tile_surface = tile_list[int(val)]
                        sprite = StaticTile((x, y), tile_size, tile_surface)
                    if type == 'decorations':
                        tile_list = import_cut_graphics('data/sprites/decorations/decorations.png')
                        tile_surface = tile_list[int(val)]
                        sprite = StaticTile((x, y), tile_size, tile_surface)
                    if type == 'coins':
                        if val == '0':
                            sprite = Coin((x, y), tile_size)
                        elif val == '1':
                            sprite = Orb((x, y), tile_size)
                    if type == 'slabs':
                        if val == '2':
                            sprite = Slab((x, y), tile_size, 'data/sprites/miscellaneous/wood_slab_left.png')
                        elif val == '1':
                            sprite = Slab((x, y), tile_size, 'data/sprites/miscellaneous/wood_slab_middle.png')
                        elif val == '0':
                            sprite = Slab((x, y), tile_size, 'data/sprites/miscellaneous/wood_slab_right.png')
                    if type == 'enemies':
                        if val == '0':
                            sprite = Goblin((x, y), tile_size)
                        elif val == '1':
                            sprite = Mushroom((x, y), tile_size)
                        elif val == '3':
                            sprite = Worm((x, y), tile_size)
                    if type == 'constraints':
                        sprite = Tile((x, y), tile_size)
                    if type == 'traps1' and val == '0':
                        tile_surface = load_image('data/sprites/miscellaneous/spikes_trap.png')
                        sprite = StaticTile((x, y), tile_size, tile_surface)
                    if type == 'traps2' and val == '1':
                        tile_surface = load_image('data/sprites/miscellaneous/spikes.png')
                        sprite = Trap((x, y), tile_size, tile_surface)

                    sprite_group.add(sprite)

        return sprite_group

    def check_coin_collision(self):
        for sprite in self.coins_sprites.sprites():
            if sprite.rect.colliderect(self.player.sprite.rect):

                pos = (sprite.rect.x+16, sprite.rect.y)
                p_coin = ParticleEffect(pos, 'coin')
                self.coin_pickup.add(p_coin)

                self.change_coins()
                sprite.kill()

                self.coin_sound.play()

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_land_particles(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            pos = self.player.sprite.rect.midbottom
            if self.player.sprite.facing_right:
                pos -= pygame.math.Vector2(0, 32)
            else:
                pos += pygame.math.Vector2(0, -32)
            land_particle_sprite = ParticleEffect(pos, 'land')
            self.dust_sprite.add(land_particle_sprite)

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(0, 32)
        else:
            pos += pygame.math.Vector2(0, -32)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def create_attack_particles(self, pos):

        if self.player.sprite.facing_right:
            pos += pygame.math.Vector2(89, 25)
        else:
            pos += pygame.math.Vector2(-25, 25)

        attack_particle_sprite = ParticleEffect(pos, 'attack')

        if not self.player.sprite.facing_right:
            attack_particle_sprite.flip()

        self.attack_sprite.add(attack_particle_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_size[0] / 2 and direction_x < 0:
            self.world_shift = 4
            player.speed = 0
        elif player_x > screen_size[0] - (screen_size[0] / 2) and direction_x > 0:
            self.world_shift = -4
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 4

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0 and not player.on_right:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0 and not player.on_left:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    if not player.on_ground:
                        self.land_sound.play()
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        for sprite in self.slabs_sprites.sprites()+self.traps_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    if not player.on_ground:
                        self.land_sound.play()
                    player.on_ground = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def enemy_collision(self):
        for enemy in self.enemies_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraints_sprites, False):
                enemy.reverse()

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.create_overworld(0, 0)
        if keys[pygame.K_DOWN]:
            if pygame.sprite.collide_rect(self.player.sprite, self.goal.sprite):
                self.create_overworld(0, self.level_data['unlock'])

    def hit_collision(self):
        for enemy in self.enemies_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.attack_sprite, False):
                hit = ParticleEffect(enemy.rect.topleft, 'hit')
                self.hit_sprite.add(hit)
                enemy.kill()
                self.hit_sound.play()

    def enemy_player_collision(self):
        if self.player.sprite.invincibility > 0:
            return
        for enemy in self.enemies_sprites.sprites():
            if enemy.rect.colliderect(self.player.sprite.rect):
                self.current_health = self.reduce_life()
                self.player.sprite.status = 'hit'
                self.player.sprite.frame_index = 0
                self.player.sprite.invincibility = 60
                self.hit_sound.play()
                break
        if self.player.sprite.invincibility > 0:
            return
        for trap in self.traps_spike_sprites.sprites():
            if pygame.sprite.collide_rect_ratio(0.85)(trap, self.player.sprite):
                self.current_health = self.reduce_life()
                self.player.sprite.status = 'hit'
                self.player.sprite.frame_index = 0
                self.player.sprite.invincibility = 60
                self.hit_sound.play()
                break
        if self.player.sprite.invincibility > 0:
            return
        for trap in self.traps_sprites.sprites():
            if pygame.sprite.collide_rect_ratio(1.05)(trap, self.player.sprite):
                self.current_health = self.reduce_life()
                self.player.sprite.status = 'hit'
                self.player.sprite.frame_index = 0
                self.player.sprite.invincibility = 60
                self.hit_sound.play()
                break

    def check_end(self):
        if self.player.sprite.rect.y > screen_size[1] or self.current_health <= 0:
            self.create_level(self.level_data)

    def run(self):
        #background
        self.display_surface.blit(self.bg1, (0, 0))
        self.display_surface.blit(self.bg2, (0, 0))

        # traps
        self.traps_sprites.update(self.world_shift)
        self.traps_spike_sprites.update(self.player, self.world_shift)
        self.traps_sprites.draw(self.display_surface)
        self.traps_spike_sprites.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # slabs
        self.slabs_sprites.update(self.world_shift)
        self.slabs_sprites.draw(self.display_surface)

        # decorations
        self.decorations_sprites.update(self.world_shift)
        self.decorations_sprites.draw(self.display_surface)

        # particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # player
        self.enemy_player_collision()

        self.goal.update(self.world_shift)
        self.player.update()
        self.attack_sprite.update()
        self.horizontal_movement_collision()

        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_land_particles()

        self.check_coin_collision()

        self.scroll_x()
        self.goal.draw(self.display_surface)
        self.player.draw(self.display_surface)

        # hit
        self.attack_sprite.draw(self.display_surface)

        self.hit_collision()
        self.hit_sprite.update()
        self.hit_sprite.draw(self.display_surface)

        # enemies
        self.enemies_sprites.update(self.world_shift)
        self.constraints_sprites.update(self.world_shift)
        self.enemy_collision()
        self.enemies_sprites.draw(self.display_surface)

        # coins
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)

        self.coin_pickup.update(self.world_shift)
        self.coin_pickup.draw(self.display_surface)

        self.input()
        self.check_end()
