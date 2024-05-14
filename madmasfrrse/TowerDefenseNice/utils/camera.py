class Camera:
    def __init__(self, x, y, game_context, zoom=1.0):
        self._offset_x = x
        self._offset_y = y
        self._zoom = zoom
        self._is_dragging = False
        self._last_drag_pos = (0, 0)
        self.game_context = game_context

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        if 0.8 <= value <= 1.3:
            self._zoom = value

    def world_to_screen(self, world_x, world_y):
        screen_x = int(round((world_x - self._offset_x) * self._zoom))
        screen_y = int(round((world_y - self._offset_y) * self._zoom))
        return screen_x, screen_y

    def screen_to_world(self, screen_x, screen_y):
        world_x = (screen_x / self._zoom) + self._offset_x
        world_y = (screen_y / self._zoom) + self._offset_y
        return world_x, world_y

    def move(self, dx, dy):
        self._offset_x -= dx / self._zoom
        self._offset_y -= dy / self._zoom

    def adjust_zoom(self, amount):
        self.zoom += amount

    def start_dragging(self, pos):
        self._is_dragging = True
        self._last_drag_pos = pos

    def stop_dragging(self):
        self._is_dragging = False

    def is_dragging(self):
        return self._is_dragging

    def update_drag(self, pos):
        if self._is_dragging:
            dx = pos[0] - self._last_drag_pos[0]
            dy = pos[1] - self._last_drag_pos[1]
            self.move(dx, dy)
            self._last_drag_pos = pos