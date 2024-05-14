import pygame
from .state_handler import GameStates
from ui.components.text_display import TextDisplay
class UIEventHandler:
    def __init__(self, component_manager, menu_manager, tower_placement_handler, game_context):
        self.component_manager = component_manager
        self.menu_manager = menu_manager
        self.tower_placement_handler = tower_placement_handler
        self.game_context = game_context
    def on_event(self, event):
        self.handle_event(event)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click_event(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self.handle_mouse_motion_event(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_button_up_event(event.pos)

    def handle_click_event(self, pos):
        for component in self.component_manager.components:
            if not isinstance(component, TextDisplay) and component.is_hovered(pos) and component.visible:
                self.process_action(component.action)

        for button in self.menu_manager.build_menu:
            if button.is_hovered(pos) and button.visible:
                self.process_action(button.action)

        for button in self.menu_manager.economy_submenu + self.menu_manager.defense_submenu:
            if button.is_hovered(pos) and button.visible:
                self.process_action(button.action)

    def handle_mouse_motion_event(self, pos):
        if self.tower_placement_handler.dragging_building:
            self.tower_placement_handler.update_tower_preview_position(pos)

    def handle_mouse_button_up_event(self, pos):
        if self.tower_placement_handler.dragging_building:
            self.tower_placement_handler.handle_drag_release(pos)

    def process_action(self, action):
        if action == 'toggle_economy':
            self.menu_manager.toggle_submenu('economy')
        elif action == 'toggle_defense':
            self.menu_manager.toggle_submenu('defense')
        elif action == 'toggle_build_menu':
            self.toggle_build_menu()
        elif action == 'on_play_pressed':
            self.on_play_pressed()
        elif action == 'on_edit_pressed':
            self.on_edit_pressed()
        elif action.startswith('start_dragging'):
            building_type = action.split('_')[2]
            sprite_path = 'assets/sprites/economy_towers/wheat_tower/wheat(1).png'
            price = 100
            self.tower_placement_handler.start_dragging(building_type, sprite_path, price)

    def toggle_build_menu(self):
        build_menu_visible = self.menu_manager.build_menu[0].visible
        for button in self.menu_manager.build_menu:
            button.visible = not build_menu_visible
        if build_menu_visible:
            for button in self.menu_manager.economy_submenu + self.menu_manager.defense_submenu:
                button.visible = False

    def on_play_pressed(self):
        print("Play button pressed!")
        self.game_context.state_handler.change_state(GameStates.GAME_PLAY)
        self.game_context.phase_handler.start_next_wave()

    def on_edit_pressed(self):
        print("Edit button pressed!")
        for tower in self.game_context.towers:
            tower.show_edit_buttons = not tower.show_edit_buttons