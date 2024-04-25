import pygame
import math

class Soldier:
    def __init__(self, world_x, world_y, soldiers, enemies, tower_x, tower_y):
        self.world_x = world_x
        self.world_y = world_y
        self.tower_x = world_x
        self.tower_y = world_y
        self.soldiers = soldiers
        self.enemies = enemies
        self.speed = 2
        self.attack_range = 15
        self.health = 200
        self.max_health = 200
        self.damage = 30
        self.scale = 0.5
        self.radius = 10 * self.scale
        self.load_sprites()
        self.current_frame = 0
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()
        self.mark_for_removal = False
        self.last_x = self.world_x
        self.flipped = False

    def load_sprites(self):
        sprite_sheet_image = pygame.image.load('supply/Knights/Warrior/Red/Warrior_Red.png').convert_alpha()
        frame_width = sprite_sheet_image.get_width() // 6
        frame_height = sprite_sheet_image.get_height() // 8
        self.idle_frames, self.idle_flipped_frames = self.load_frame_set(sprite_sheet_image, frame_width, frame_height, 0)
        self.moving_frames, self.moving_flipped_frames = self.load_frame_set(sprite_sheet_image, frame_width, frame_height, frame_height)
        self.attacking_frames, self.attacking_flipped_frames = self.load_frame_set(sprite_sheet_image, frame_width, frame_height, 3 * frame_height)
        self.frames = self.idle_frames

    def load_frame_set(self, sprite_sheet_image, frame_width, frame_height, offset_y):
        frames = []
        flipped_frames = []
        for i in range(6):
            frame = pygame.transform.scale(sprite_sheet_image.subsurface(pygame.Rect(i * frame_width, offset_y, frame_width, frame_height)), (int(frame_width * self.scale), int(frame_height * self.scale)))
            frames.append(frame)
            flipped_frames.append(pygame.transform.flip(frame, True, False))
        return frames, flipped_frames

    def update(self, enemies):
        now = pygame.time.get_ticks()
        target = self.find_closest_enemy(enemies)
        if target:
            distance = self.calculate_distance(target)
            if distance <= self.attack_range:
                if self.frames == self.attacking_frames and self.current_frame == len(self.attacking_frames) - 1:
                    self.attack(target)
                    self.frames = self.idle_frames
                    self.current_frame = 0
                else:
                    self.frames = self.attacking_frames
            else:
                self.frames = self.moving_frames
            self.move_towards(target)
        else:
            if self.calculate_distance_to_tower() > 10:
                self.move_towards_tower()
                self.frames = self.moving_frames
            else:
                self.frames = self.idle_frames

        self.flipped = self.last_x > self.world_x
        self.last_x = self.world_x
        self.animate_frame(now)

    def move_towards(self, target):
        dir_x = target.world_x - self.world_x
        dir_y = target.world_y - self.world_y
        norm = max(math.sqrt(dir_x ** 2 + dir_y ** 2), 1)
        self.world_x += dir_x / norm * self.speed
        self.world_y += dir_y / norm * self.speed

    def calculate_distance_to_tower(self):
        return ((self.tower_x - self.world_x) ** 2 + (self.tower_y - self.world_y) ** 2) ** 0.5

    def animate_frame(self, now):
        frame_period = 1000 * self.animation_speed
        if now - self.last_update > frame_period:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now

    def collision_check(self, target):
        for entity in self.soldiers + self.enemies:
            if entity != self and self.calculate_distance(entity) < self.radius + entity.radius:
                angle = math.atan2(entity.world_y - self.world_y, entity.world_x - self.world_x)
                self.world_x -= math.cos(angle) * 0.5
                self.world_y -= math.sin(angle) * 0.5
                return True
        return False

    def find_closest_enemy(self, enemies):
        closest = None
        min_distance = float('inf')
        for enemy in enemies:
            distance = self.calculate_distance(enemy)
            if distance < min_distance:
                min_distance = distance
                closest = enemy
        return closest

    def calculate_distance(self, other):
        return math.sqrt((self.world_x - other.world_x) ** 2 + (self.world_y - other.world_y) ** 2)
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.mark_for_removal = True
            print("Main Tower destroyed. Game Over.")

    def draw(self, screen, camera):
        frame = self.frames[self.current_frame]
        if self.flipped:
            frame = self.get_flipped_frame(frame)
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        screen.blit(frame, (screen_x - frame.get_width() // 2, screen_y - frame.get_height() // 2))

        if self.health < self.max_health:
            self.draw_health_bar(screen, screen_x, screen_y)

    def get_flipped_frame(self, frame):
        if self.frames == self.idle_frames:
            return self.idle_flipped_frames[self.current_frame]
        elif self.frames == self.moving_frames:
            return self.moving_flipped_frames[self.current_frame]
        elif self.frames == self.attacking_frames:
            return self.attacking_flipped_frames[self.current_frame]

    def draw_health_bar(self, screen, screen_x, screen_y):
        bar_length = 50
        bar_height = 5
        fill_length = int(bar_length * (self.health / self.max_health))

        pygame.draw.rect(screen, (255, 0, 0), (screen_x - bar_length // 2, screen_y - 30, bar_length, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (screen_x - bar_length // 2, screen_y - 30, fill_length, bar_height))

    def move_towards_tower(self):
        tower_position = Position(self.tower_x, self.tower_y)
        self.move_towards(tower_position)

    def attack(self, enemy):
        if self.current_frame == len(self.attacking_frames) - 1:
            enemy.take_damage(self.damage)
            self.frames = self.idle_frames
            self.current_frame = 0

class Position:
    def __init__(self, x, y):
        self.world_x = x
        self.world_y = y
