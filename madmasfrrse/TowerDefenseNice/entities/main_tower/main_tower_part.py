from settings import settings
class MainTowerPart:
    def __init__(self, x, y, sprite, z_index):
        self.world_x, self.world_y = settings.iso_projection(x, y)
        self.sprite = sprite
        self.z_index = z_index
        self.is_destroyed = False

    def draw(self, game_context):
        if not self.is_destroyed:
            screen_x, screen_y = game_context.camera.world_to_screen(self.world_x, self.world_y)
            if game_context.camera.zoom < 1:
                game_context.screen.blit(self.sprite, (screen_x - self.sprite.get_width() // 2, screen_y - self.sprite.get_height() // 2 - 15))
            else:
                game_context.screen.blit(self.sprite, (screen_x - self.sprite.get_width() // 2, screen_y - self.sprite.get_height() // 2 + 5))