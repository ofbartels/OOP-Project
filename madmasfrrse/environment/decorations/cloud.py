import pygame
import random

class CloudDecoration:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.images = [pygame.image.load(f'supply/clouds/Cloud({i}).png').convert_alpha() for i in range(1, 3)]
        self.current_image = random.choice(self.images)
        self.speed = random.uniform(0.03, 0.06)  

    def update(self, delta_time):
        self.x += self.speed * delta_time

    def draw(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.x, self.y) if camera else (self.x, self.y)
        screen.blit(self.current_image, (screen_x, screen_y))

class CloudManager:
    def __init__(self):
        self.clouds = [CloudDecoration(random.randint(0, 1100), random.randint(-50, 150)) for _ in range(5)]

    def update(self, delta_time):
        for cloud in self.clouds:
            cloud.update(delta_time)
            if cloud.x > 1100:  
                cloud.x = -cloud.current_image.get_width()

    def draw(self, screen, camera=None):
        for cloud in self.clouds:
            cloud.draw(screen, camera)
