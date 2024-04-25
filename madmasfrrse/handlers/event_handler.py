import pygame
from settings import settings
from handlers.state_handler import GameStates

class EventHandler:
    def __init__(self, camera, tile_map, towers, currency_handler, state_handler):
        self.camera = camera
        self.tile_map = tile_map
        self.towers = towers
        self.currency_handler = currency_handler
        self.state_handler = state_handler
        self.dragging_building = False
        self.building_type = None
        self.tower_sprite_path = None
        self.tower_preview_pos = None
        self.is_mouse_pressed = False
        self.mouse_press_position = (0, 0)

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
        from entities.base_tower import Tower
        world_x, world_y = self.camera.screen_to_world(*pos)
        grid_x, grid_y = settings.inverse_iso_projection(world_x, world_y)
        clicked_tile = self.tile_map.get_clicked_tile(pos[0], pos[1], self.camera)

        if clicked_tile is None or clicked_tile.occupied:
            print("Cannot place a tower here, tile is occupied.")
            return False

        new_tower = Tower.create_tower(grid_x, grid_y, self.building_type, 1)
        self.towers.append(new_tower)
        clicked_tile.occupied = True
        self.currency_handler.spend_currency(self.building_price)
        self.cancel_dragging()
        print(f"Tower placed at: {grid_x}, {grid_y}")
        return True

    def handle_events(self, event):
        handlers = {
            pygame.MOUSEBUTTONDOWN: self._handle_mouse_button_down,
            pygame.MOUSEBUTTONUP: self._handle_mouse_button_up,
            pygame.MOUSEMOTION: self._handle_mouse_motion,
        }
        handler = handlers.get(event.type)
        if handler:
            handler(event)

    def _handle_mouse_button_down(self, event):
        self.is_mouse_pressed = True
        self.mouse_press_position = event.pos
        if event.button == 1 and not self.dragging_building:
            self.start_dragging_camera(event.pos)
        elif event.button == 4:
            self.camera.adjust_zoom(0.1)
        elif event.button == 5:
            self.camera.adjust_zoom(-0.1)

    def _handle_mouse_button_up(self, event):
        self.is_mouse_pressed = False
        if event.button == 1:
            if self.dragging_building:
                self.handle_drag_release(event.pos)
            else:
                if self.was_click(event.pos):
                    self.handle_click(event.pos)
                self.stop_dragging_camera()

    def _handle_mouse_motion(self, event):
        if self.dragging_building:
            self.update_tower_preview_position(event.pos)
        elif self.camera.is_dragging:
            self.camera.move(*event.rel)

    def handle_drag_release(self, pos):
        if not self.place_tower(pos):
            self.cancel_dragging()

    def handle_click(self, pos):
        if self.state_handler.current_state == GameStates.EDIT_MODE:
            self.check_tower_interaction(pos)
        else:
            # Handle other game states as necessary
            pass

    def was_click(self, release_position):
        press_x, press_y = self.mouse_press_position
        release_x, release_y = release_position
        move_threshold = 5
        return abs(release_x - press_x) < move_threshold and abs(release_y - press_y) < move_threshold

    def start_dragging_camera(self, pos):
        self.camera.is_dragging = True

    def stop_dragging_camera(self):
        self.camera.is_dragging = False

    def update_tower_preview_position(self, pos):
        world_pos = self.camera.screen_to_world(*pos)
        self.tower_preview_pos = world_pos

    def draw_tower_preview(self, screen):
        if self.tower_preview_pos:
            screen_pos = self.camera.world_to_screen(*self.tower_preview_pos)
            pygame.draw.circle(screen, (100, 100, 100), screen_pos, 15)

    def check_tower_interaction(self, mouse_pos):
        for tower in self.towers:
            if tower.upgrade_button_rect.collidepoint(mouse_pos):
                self.handle_upgrade(tower)
            elif tower.delete_button_rect.collidepoint(mouse_pos):
                self.handle_delete(tower)
            elif hasattr(tower, 'left_button_rect') and tower.left_button_rect.collidepoint(mouse_pos):
                self.handle_flip(tower, flip_left=True)
            elif hasattr(tower, 'right_button_rect') and tower.right_button_rect.collidepoint(mouse_pos):
                self.handle_flip(tower, flip_left=False)

    def handle_upgrade(self, tower):
        upgrade_cost = tower.get_upgrade_cost()
        if self.currency_handler.can_afford(upgrade_cost):
            tower.upgrade()
            self.currency_handler.spend_currency(upgrade_cost)
            print(f"Tower upgraded to level {tower.level}.")
        else:
            print("Not enough currency to upgrade.")

    def handle_delete(self, tower):
        self.towers.remove(tower)
        print("Tower deleted")

    def handle_flip(self, tower, flip_left):
        if not flip_left:
            tower.flipped = True
        else:
            tower.flipped = False
        print(f"Flipped {'left' if flip_left else 'right'}: {tower.flipped}")
