import pygame
from settings import settings

class Enemy:
    enemy_sprites = {
        'goblin': 'supply/Goblins/Torch/Blue/Torch_Blue.png',
        'goblin_bomber': 'supply/Goblins/TNT/Red/TNT_Red.png',
        'minotaur': 'supply/Goblins/minotaur.png',
        'eyeball': 'supply/Goblins/eyeball.png',
    }

    def __init__(self, grid_x, grid_y, enemy_type='goblin', radius=30, health=150, damage=10):
        self.world_x, self.world_y = settings.iso_projection(grid_x, grid_y)
        self.radius = radius
        self.health = health
        self.max_health = health
        self.original_speed = 100
        self.speed = 100
        self.scale = 0.6
        self.enemy_type = enemy_type
        self.damage = damage
        self.sprite_sheet, self.flipped_sprite_sheet = self.load_sprite_sheet(self.enemy_sprites[enemy_type], 7, 5)
        self.current_frame = 0
        self.frame_update_time = pygame.time.get_ticks()
        self.frame_rate = 100
        self.combat_row = 4
        self.animation_row = 1
        self.is_destroyed = False
        self.mark_for_removal = False
        self.last_x = self.world_x
        self.flipped = False
        self.combat_finished = False
        self.in_combat = False  # State to determine if the enemy is in combat

    def update(self, towers, delta_time, main_tower, soldiers):
        current_time = pygame.time.get_ticks()
        nearest_target, nearest_distance = self.find_nearest_target(towers, main_tower, soldiers)
        
        if nearest_target:
            if self.check_in_combat(nearest_distance):  # Check if the enemy is in combat
                self.handle_combat(nearest_target)

        if not self.in_combat:
            self.move_towards(main_tower.world_x, main_tower.world_y, delta_time)
            self.animation_row = 1

        if current_time - self.frame_update_time > self.frame_rate:
            self.update_animation()

    def find_nearest_target(self, towers, main_tower, soldiers):
        targets = towers + [main_tower] + soldiers
        nearest_target, nearest_distance = None, float('inf')
        for target in targets:
            distance = ((self.world_x - target.world_x) ** 2 + (self.world_y - target.world_y) ** 2) ** 0.5
            if distance < self.radius and distance < nearest_distance:
                nearest_target, nearest_distance = target, distance
        return nearest_target, nearest_distance

    def check_in_combat(self, nearest_distance):
        self.in_combat = nearest_distance < self.radius
        return self.in_combat

    def handle_combat(self, target):
        self.animation_row = self.combat_row
        self.speed = 0
        if self.current_frame == len(self.sprite_sheet[self.combat_row]) - 1 and not self.combat_finished:
            target.take_damage(self.damage)
            self.combat_finished = True
        if target.health <= 0:
            self.in_combat = False
            self.speed = self.original_speed

    def move_towards(self, target_x, target_y, delta_time):
        direction = (target_x - self.world_x, target_y - self.world_y)
        norm = max((direction[0] ** 2 + direction[1] ** 2) ** 0.5, 1)
        movement = (direction[0] / norm * self.speed * (delta_time / 1000.0),
                    direction[1] / norm * self.speed * (delta_time / 1000.0))
        self.world_x += movement[0]
        self.world_y += movement[1]

    def update_animation(self):
        if self.in_combat:
            self.current_frame = (self.current_frame + 1) % len(self.sprite_sheet[self.animation_row])
            self.frame_update_time = pygame.time.get_ticks()
            self.combat_finished = self.current_frame == 0
        else:
            self.current_frame = (self.current_frame + 1) % len(self.sprite_sheet[self.animation_row])
            self.frame_update_time = pygame.time.get_ticks()
            self.combat_finished = self.current_frame == 0
            new_x = self.world_x
            self.flipped = new_x < self.last_x
            self.last_x = new_x
            
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.mark_for_removal = True

    def draw_health_bar(self, screen, camera):
        if self.health < self.max_health:
            screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
            bar_length, bar_height = 50, 5
            fill = (self.health / self.max_health) * bar_length
            pygame.draw.rect(screen, (255, 0, 0), (screen_x - bar_length // 2, screen_y - 20, bar_length, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (screen_x - bar_length // 2, screen_y - 20, fill, bar_height))

    def draw(self, screen, camera):
        if not self.is_destroyed:
            screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
            frame = self.flipped_sprite_sheet[self.animation_row][self.current_frame] if self.flipped else self.sprite_sheet[self.animation_row][self.current_frame]
            screen.blit(frame, (screen_x - frame.get_width() // 2, screen_y - frame.get_height() // 2))
            self.draw_health_bar(screen, camera)

    def load_sprite_sheet(self, file_path, num_columns, num_rows):
        sprite_sheet_image = pygame.image.load(file_path).convert_alpha()
        frame_width = sprite_sheet_image.get_width() // num_columns
        frame_height = sprite_sheet_image.get_height() // num_rows
        frames, flipped_frames = [], []
        for row in range(num_rows):
            frames.append([])
            flipped_frames.append([])
            for col in range(num_columns - 1):
                rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
                frame_image = pygame.transform.scale(sprite_sheet_image.subsurface(rect), 
                                                     (int(frame_width * self.scale), int(frame_height * self.scale)))
                frames[row].append(frame_image)
                flipped_frames[row].append(pygame.transform.flip(frame_image, True, False))
        return frames, flipped_frames
