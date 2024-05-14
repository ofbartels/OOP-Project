import pygame

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Settings(metaclass=SingletonMeta):
    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.GREY = (30, 30, 30)

        self.TILE_WIDTH = 64 + 26
        self.TILE_HEIGHT = 32 + 21

        self.ROWS = 25
        self.COLS = 25

        self.BUTTON_WIDTH = 100
        self.BUTTON_HEIGHT = 40
        self.BUTTON_X_OFFSET = 10
        self.BUTTON_Y_OFFSET = 10

        self.grid_center_x = self.COLS // 2
        self.grid_center_y = self.ROWS // 2
        self.center_x, self.center_y = self.iso_projection(self.grid_center_x, self.grid_center_y)

    def iso_projection(self, grid_x, grid_y):
        screen_x = (grid_x - grid_y) * (self.TILE_WIDTH // 2)
        screen_y = (grid_x + grid_y) * (self.TILE_HEIGHT // 2)
        return screen_x + self.SCREEN_WIDTH // 2, screen_y

    def inverse_iso_projection(self, screen_x, screen_y):
        screen_x -= self.SCREEN_WIDTH // 2
        grid_x = ((screen_x / (self.TILE_WIDTH / 2)) + (screen_y / (self.TILE_HEIGHT / 2))) / 2
        grid_y = ((screen_y / (self.TILE_HEIGHT / 2)) - (screen_x / (self.TILE_WIDTH / 2))) / 2
        return int(round(grid_x)), int(round(grid_y))

    def scale_image(self, image, target_width, target_height):
        original_width, original_height = image.get_size()
        aspect_ratio = original_width / original_height
        if target_width / target_height > aspect_ratio:
            new_height = target_height
            new_width = int(new_height * aspect_ratio)
        else:
            new_width = target_width
            new_height = int(new_width / aspect_ratio)
        return pygame.transform.scale(image, (new_width, new_height))

settings = Settings()