import pygame
import random
from environment.objects.game_object import GameObject
from environment.tile import Tile

class Stone(GameObject):
    def __init__(self, tile: Tile):
        super().__init__(tile)
        self._occupied = True
        self._type = 'stone'
        self._sprite_cache = {}  # Cache to store different zoom levels of the sprite
        self._base_offsets = (0, 0)  # Example fixed offset
        self._load_sprite()  # Pre-load and cache sprites at various scales if necessary

    def _load_sprite(self):
        """Load and cache the sprite for various zoom levels."""
        stone_sprites = [
            'assets/sprites/environment/stones/stone(1).png',
            'assets/sprites/environment/stones/stone(2).png',
            'assets/sprites/environment/stones/stone(3).png',
            'assets/sprites/environment/stones/stone(4).png',
        ]
        sprite_path = random.choice(stone_sprites)
        base_sprite = pygame.image.load(sprite_path).convert_alpha()
        for zoom in [0.5, 0.75, 1, 1.5, 2]:  # Example zoom levels
            self._sprite_cache[zoom] = pygame.transform.smoothscale(base_sprite, (int(base_sprite.get_width() * zoom), int(base_sprite.get_height() * zoom)))

    def draw(self, game_context):
        current_zoom = round(game_context.camera.zoom, 2)
        # Choose the closest zoom level available in the cache, default to base sprite
        sprite_to_draw = self._sprite_cache.get(current_zoom, self._sprite_cache[min(self._sprite_cache.keys(), key=lambda k: abs(k-current_zoom))])

        screen_x, screen_y = game_context.camera.world_to_screen(self.world_x + self._base_offsets[0], self.world_y + self._base_offsets[1])
        # Adjust sprite position to center it on its coordinates
        game_context.screen.blit(sprite_to_draw, (screen_x - sprite_to_draw.get_width() // 2, screen_y - sprite_to_draw.get_height() // 2))

    @property
    def occupied(self):
        return self._occupied

    @property
    def type(self):
        return self._type