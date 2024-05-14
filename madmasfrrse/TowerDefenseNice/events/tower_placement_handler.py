import pygame
from settings import settings
from entities.towers.tower_factories import EconomyTowerFactory, DefenseTowerFactory

class TowerPlacementHandler:
    def __init__(self, game_context):
        self.game_context = game_context
        self.dragging_building = False
        self.building_type = None
        self.tower_sprite_path = None
        self.tower_preview_pos = None
        self.is_mouse_pressed = False
        self.mouse_press_position = (0, 0)

    @property
    def tile_map(self):
        return self.game_context.tile_map

    @property
    def towers(self):
        return self.game_context.towers

    @property
    def currency_handler(self):
        return self.game_context.currency_handler

    @property
    def state_handler(self):
        return self.game_context.state_handler

    def start_dragging(self, building_type, sprite_path, price):
        self.dragging_building = True
        self.building_type = building_type
        self.tower_sprite_path = sprite_path
        self.building_price = price
        print(f"Started dragging: {building_type}")

    def cancel_dragging(self):
        if self.dragging_building:
            print("Dragging cancelled. No currency was charged.")
            self.dragging_building = False
            self.building_type = None
            self.tower_preview_pos = None
            self.building_price = 0

    def place_tower(self, pos):
        world_x, world_y = self.game_context.camera.screen_to_world(*pos)
        grid_x, grid_y = settings.inverse_iso_projection(world_x, world_y)
        clicked_tile = self.tile_map.get_clicked_tile(pos[0], pos[1], self.game_context)

        if clicked_tile is None or clicked_tile.occupied:
            print("Cannot place a tower here, tile is occupied.")
            return False

        if self.building_type in ['wheat', 'corn', 'house', 'mill', 'smith']:
            factory = EconomyTowerFactory()
        elif self.building_type in ['archer', 'ballista', 'barracks', 'wizard']:
            factory = DefenseTowerFactory()
        else:
            raise ValueError(f"Invalid building type: {self.building_type}")

        new_tower = factory.create_tower(grid_x, grid_y, self.building_type, 1)
        self.towers.append(new_tower)
        clicked_tile.occupied = True
        self.currency_handler.spend_currency(self.building_price)
        self.cancel_dragging()
        print(f"Tower placed at: {grid_x}, {grid_y}")
        return True

    def handle_drag_release(self, pos):
        if not self.place_tower(pos):
            self.cancel_dragging()

    def update_tower_preview_position(self, pos):
        world_pos = self.game_context.camera.screen_to_world(*pos)
        self.tower_preview_pos = world_pos

    def draw_tower_preview(self, screen):
        if self.tower_preview_pos:
            screen_pos = self.game_context.camera.world_to_screen(*self.tower_preview_pos)
            pygame.draw.circle(screen, (100, 100, 100), screen_pos, 15)