import pygame

class Settings:
    def __init__(self):
        # Screen dimensions...
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        
        # Color definitions...
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.GREY = (30, 30, 30)

        # Tile dimensions for grid...
        self.TILE_WIDTH = 64 + 26
        self.TILE_HEIGHT = 32 +  21

        # Grid dimensions...
        self.ROWS = 35
        self.COLS = 35

        # Button dimensions and offsets for UI...
        self.BUTTON_WIDTH = 100
        self.BUTTON_HEIGHT = 40
        self.BUTTON_X_OFFSET = 10
        self.BUTTON_Y_OFFSET = 10

        # Camera attribute to store a camera instance...
        self.camera = None

        # Central point of the grid for initial focus and main tower spawn...
        self.grid_center_x = self.COLS // 2
        self.grid_center_y = self.ROWS // 2
        self.center_x, self.center_y = self.iso_projection(self.grid_center_x, self.grid_center_y)

    def set_camera(self, camera):
        "Set the camera object for the game context."
        self.camera = camera

    def iso_projection(self, grid_x, grid_y):
        """
        Convert grid coordinates to isometric screen coordinates.
        
        Args:
            grid_x: The x-coordinate on the grid.
            grid_y: The y-coordinate on the grid.
            
        Returns:
            A tuple (screen_x, screen_y) representing the screen coordinates.
        """
        screen_x = (grid_x - grid_y) * (self.TILE_WIDTH // 2.0)
        screen_y = (grid_x + grid_y) * (self.TILE_HEIGHT // 2.0)
        return screen_x + self.SCREEN_WIDTH // 2.0, screen_y

    def inverse_iso_projection(self, screen_x, screen_y):
        """
        Convert isometric screen coordinates back to grid coordinates.
        
        Args:
            screen_x: The x-coordinate on the screen.
            screen_y: The y-coordinate on the screen.
        
        Returns:
            A tuple (grid_x, grid_y) representing the grid coordinates.
        """
        screen_x -= self.SCREEN_WIDTH // 2
        grid_x = ((screen_x / (self.TILE_WIDTH / 2)) + (screen_y / (self.TILE_HEIGHT / 2))) / 2
        grid_y = ((screen_y / (self.TILE_HEIGHT / 2)) - (screen_x / (self.TILE_WIDTH / 2))) / 2
        return int(round(grid_x)), int(round(grid_y))
    
    def scale_image(self, image, target_width, target_height):
        """
        Scale an image to a target size while maintaining the aspect ratio.
        
        Args:
            image: The pygame surface to be scaled.
            target_width: The desired width.
            target_height: The desired height.
        
        Returns:
            The scaled image as a pygame surface.
        """
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
