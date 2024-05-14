import pygame
import random
import time
from events.state_handler import GameStates
from settings import settings

class Villager:
    def __init__(self, x, y, sprite_path, speed_range=(1, 3), scale=0.6, hangout_duration=5):
        self.world_x = x
        self.world_y = y
        self.original_sprite = pygame.image.load(sprite_path).convert_alpha()
        self.sprite = pygame.transform.scale(self.original_sprite, (int(self.original_sprite.get_width() * scale), int(self.original_sprite.get_height() * scale)))
        self.speed = random.randint(*speed_range)
        self.target_tile = None
        self.interaction_time = time.time()
        self.hangout_duration = hangout_duration
        self.visible = True

    def update(self, state_handler, enemies, tile_map):
        if state_handler.current_state == GameStates.BUILD_MODE:
            self.visible = True

        if not self.target_tile or (self.reached_target() and (time.time() - self.interaction_time > self.hangout_duration)):
            self.choose_new_target(tile_map)

        if self.target_tile and not self.reached_target():
            self.move_towards_target()
        else:
            self.move_to_safety()

        self.react_to_enemies(enemies)

    def reached_target(self):
        if self.target_tile:
            target_x, target_y = self.target_tile.world_x, self.target_tile.world_y
            return (self.world_x - target_x) ** 2 + (self.world_y - target_y) ** 2 < 25
        return False

    def choose_new_target(self, tile_map):
        potential_targets = [tile for row in tile_map.tiles for tile in row if tile.object]
        if potential_targets:
            self.target_tile = random.choice(potential_targets)
            print(f"New target selected at ({self.target_tile.world_x}, {self.target_tile.world_y})")
        else:
            print("No available targets found.")

    def move_towards_target(self):
        if self.target_tile:
            self.move_towards(self.target_tile.world_x, self.target_tile.world_y)

    def interact_with_target_tile(self):
        if self.reached_target():
            self.target_tile.object = None
            self.target_tile.occupied = False
            self.interaction_time = time.time()

    def react_to_enemies(self, enemies):
        for enemy in enemies:
            if self.distance_to(enemy) < 50:
                self.run_away_from(enemy)

    def run_away_from(self, enemy):
        self.move_towards(settings.center_x, settings.center_y)

    def move_to_safety(self):
        safety_radius = 30
        dx = settings.center_x - self.world_x
        dy = (settings.center_y - 50) - self.world_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        self.move_towards(settings.center_x, settings.center_y - 50)
        if distance < safety_radius:
            self.visible = False

    def move_towards(self, target_x, target_y):
        direction = (target_x - self.world_x, target_y - self.world_y)
        norm = max((direction[0] ** 2 + direction[1] ** 2) ** 0.5, 1)
        self.world_x += direction[0] / norm * self.speed
        self.world_y += direction[1] / norm * self.speed

    def distance_to(self, other):
        return ((self.world_x - other.world_x) ** 2 + (self.world_y - other.world_y) ** 2) ** 0.5

    def draw(self, screen, camera):
        if self.visible:
            screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
            screen.blit(self.sprite, (screen_x - self.sprite.get_width() // 2, screen_y - self.sprite.get_height() // 2))