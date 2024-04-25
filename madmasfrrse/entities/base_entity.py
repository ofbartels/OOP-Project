import pygame
from settings import settings

# This honestly just complicates some inheritance stuff and is no longer needed, will delete.

class BaseEntity:
    def __init__(self, world_x, world_y):
        self.world_x = world_x
        self.world_y = world_y

class MovingEntity(BaseEntity):
    def __init__(self, world_x, world_y, health, radius):
        super().__init__(world_x, world_y)
        self.health = 1000
        self.radius = radius

    def reduce_health(self, amount):
        self.health = max(self.health - amount, 0)

    def draw_health(self, screen):
        screen_x, screen_y = settings.camera.world_to_screen(self.world_x, self.world_y - 20)
        health_text = pygame.font.SysFont("Arial", 14).render(str(self.health), True, (255, 255, 255))
        screen.blit(health_text, (screen_x, screen_y))
    
    def rect_at_position(self, x, y):
        screen_x, screen_y = settings.camera.world_to_screen(x, y)
        return pygame.Rect(screen_x - self.radius, screen_y - self.radius, self.radius * 2, self.radius * 2)