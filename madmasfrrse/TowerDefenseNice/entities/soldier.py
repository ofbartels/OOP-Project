import pygame
import math

class Soldier:
    def __init__(self, world_x, world_y, soldiers, enemies, speed=2, attack_range=15, health=200, damage=30, scale=0.5):
        self.world_x = world_x
        self.world_y = world_y
        self.tower_x = world_x
        self.tower_y = world_y
        self.soldiers = soldiers
        self.enemies = enemies
        self.speed = speed
        self.attack_range = attack_range
        self.health = health
        self.max_health = health
        self.damage = damage
        self.scale = scale
        self.radius = 10 * self.scale
        self.idle_frames, self.idle_flipped_frames, self.moving_frames, self.moving_flipped_frames, self.attacking_frames, self.attacking_flipped_frames = self.load_sprites()
        self.current_frame = 0
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()
        self.mark_for_removal = False
        self.last_x = self.world_x
        self.flipped = False

    def load_sprites(self):
        sprite_sheet_image = pygame.image.load('assets/sprites/friendly/Knight.png').convert_alpha()
        frame_width = sprite_sheet_image.get_width() // 6
        frame_height = sprite_sheet_image.get_height() // 8
        idle_frames, idle_flipped_frames = self.load_frame_set(sprite_sheet_image, frame_width, frame_height, 0)
        moving_frames, moving_flipped_frames = self.load_frame_set(sprite_sheet_image, frame_width, frame_height, frame_height)
        attacking_frames, attacking_flipped_frames = self.load_frame_set(sprite_sheet_image, frame_width, frame_height, 3 * frame_height)
        return idle_frames, idle_flipped_frames, moving_frames, moving_flipped_frames, attacking_frames, attacking_flipped_frames

    def load_frame_set(self, sprite_sheet_image, frame_width, frame_height, offset_y):
        frames = [pygame.transform.scale(sprite_sheet_image.subsurface(pygame.Rect(i * frame_width, offset_y, frame_width, frame_height)),
                  (int(frame_width * self.scale), int(frame_height * self.scale))) for i in range(6)]
        flipped_frames = [pygame.transform.flip(frame, True, False) for frame in frames]
        return frames, flipped_frames

    def update(self):
        now = pygame.time.get_ticks()
        target = self.find_closest_enemy()
        if target:
            distance = self.calculate_distance(target)
            if distance <= self.attack_range:
                self.frames = self.attacking_frames if self.current_frame < len(self.attacking_frames) - 1 else self.idle_frames
                if self.current_frame == len(self.attacking_frames) - 1:
                    self.attack(target)
            else:
                self.frames = self.moving_frames
                self.move_towards(target)
        else:
            if self.calculate_distance_to_tower() > 10:
                self.move_towards_tower()
            self.frames = self.idle_frames

        self.flipped = self.last_x > self.world_x
        self.last_x = self.world_x
        self.resolve_collisions()
        self.animate_frame(now)

    def find_closest_enemy(self):
        closest = min(self.enemies, key=lambda enemy: self.calculate_distance(enemy), default=None)
        return closest

    def calculate_distance(self, other):
        return math.hypot(self.world_x - other.world_x, self.world_y - other.world_y)

    def move_towards(self, target):
        dir_x, dir_y = target.world_x - self.world_x, target.world_y - self.world_y
        norm = max(math.hypot(dir_x, dir_y), 1)
        self.world_x += dir_x / norm * self.speed
        self.world_y += dir_y / norm * self.speed

    def resolve_collisions(self):
        for other in self.soldiers:
            if other != self and self.calculate_distance(other) < self.radius + other.radius:
                overlap = self.radius + other.radius - self.calculate_distance(other)
                angle = math.atan2(other.world_y - self.world_y, other.world_x - self.world_x)
                self.world_x -= math.cos(angle) * overlap / 2
                self.world_y -= math.sin(angle) * overlap / 2

    def draw_health_bar(self, screen, screen_x, screen_y):
        bar_length = 50
        bar_height = 5
        fill_length = int(bar_length * (self.health / self.max_health))
        pygame.draw.rect(screen, (255, 0, 0), (screen_x - bar_length // 2, screen_y - 30, bar_length, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (screen_x - bar_length // 2, screen_y - 30, fill_length, bar_height))

    def draw(self, screen, camera):
        frame = self.get_flipped_frame()
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        screen.blit(frame, (screen_x - frame.get_width() // 2, screen_y - frame.get_height() // 2))
        if self.health < self.max_health:
            self.draw_health_bar(screen, screen_x, screen_y)

    def get_flipped_frame(self):
        if self.flipped:
            return self.idle_flipped_frames[self.current_frame] if self.frames == self.idle_frames else \
                   self.moving_flipped_frames[self.current_frame] if self.frames == self.moving_frames else \
                   self.attacking_flipped_frames[self.current_frame]
        return self.frames[self.current_frame]

    def move_towards_tower(self):
        self.move_towards(Position(self.tower_x, self.tower_y))

    def calculate_distance_to_tower(self):
        return math.hypot(self.tower_x - self.world_x, self.tower_y - self.world_y)

    def attack(self, enemy):
        enemy.take_damage(self.damage)
        self.frames = self.idle_frames
        self.current_frame = 0

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.mark_for_removal = True
            print("Soldier destroyed.")

    def animate_frame(self, now):
        frame_period = 1000 * self.animation_speed
        if now - self.last_update > frame_period:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now


class Position:
    def __init__(self, x, y):
        self.world_x = x
        self.world_y = y