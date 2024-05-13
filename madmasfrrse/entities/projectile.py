import pygame
import math

class Projectile:
    def __init__(self, start_pos, target, damage, sprite_path='supply/Defense/Archer/arrow.png'):
        self.x, self.y = start_pos
        self.target = target
        self.damage = damage
        self.active = True
        self.speed = 5
        self.gravity = 0.2
        self.vertical_velocity = -5
        self.load_and_scale_image(sprite_path, 0.75)

    def load_and_scale_image(self, sprite_path, scale_factor):
        self.image = pygame.image.load(sprite_path).convert_alpha()
        new_size = (int(self.image.get_rect().width * scale_factor), int(self.image.get_rect().height * scale_factor))
        self.image = pygame.transform.scale(self.image, new_size)
        self.rect = self.image.get_rect()

    def update(self):
        if not self.active:
            return
        dx, dy = self.target.world_x - self.x, self.target.world_y - self.y
        distance = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)
        if distance < self.speed:
            self.target.take_damage(self.damage)
            self.active = False
        else:
            self.x += self.speed * dx / distance
            self.y += self.speed * dy / distance + self.vertical_velocity
            self.vertical_velocity += self.gravity
        self.rotated_image = pygame.transform.rotate(self.image, -math.degrees(angle) - 90)
        self.rect = self.rotated_image.get_rect(center=(self.x, self.y))

    def draw(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.x, self.y)
        screen.blit(self.rotated_image, self.rect.move(screen_x - self.rect.centerx, screen_y - self.rect.centery))
