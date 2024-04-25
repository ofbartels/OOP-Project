from settings import settings

class Camera:
    def __init__(self, x, y, zoom=1.0):
        self.offset_x = x
        self.offset_y = y
        self.zoom = zoom
        self.is_dragging = False
        self.last_drag_pos = (0, 0)

    def world_to_screen(self, world_x, world_y):
        # Apply zoom scaling to the coordinates
        screen_x = int(round((world_x - self.offset_x) * self.zoom))
        screen_y = int(round((world_y - self.offset_y) * self.zoom))
        return screen_x, screen_y

    def screen_to_world(self, screen_x, screen_y):
        # Reverse the zoom scaling to convert back to world coordinates
        return (screen_x / self.zoom) + self.offset_x, (screen_y / self.zoom) + self.offset_y

    def move(self, dx, dy):
        self.offset_x -= dx / self.zoom
        self.offset_y -= dy / self.zoom

    def adjust_zoom(self, amount):
        # Adjust the zoom level
        new_zoom = self.zoom + amount
        if 0.8 <= new_zoom <= 1:  # Limits zoom range between 0.5x and 2x
            self.zoom = new_zoom

    def follow(self, entity):
        self.offset_x = (entity.world_x - settings.SCREEN_WIDTH // 2) / self.zoom
        self.offset_y = (entity.world_y - settings.SCREEN_HEIGHT // 2) / self.zoom
