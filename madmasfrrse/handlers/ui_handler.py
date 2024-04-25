import pygame
from ui.ui_components import Button, TextDisplay
from settings import settings
from handlers.state_handler import GameStates

class UIManager:
    def __init__(self, screen, currency_handler, event_handler, state_handler, phase_handler):
        self.screen = screen
        self.currency_handler = currency_handler
        self.event_handler = event_handler
        self.state_handler = state_handler
        self.phase_handler = phase_handler
        self.components = []
        self.load_resources()
        self.setup_ui_components()
        self.initialize_menu_options()
        self.edit_mode_active = False

    def load_resources(self):
        self.resources = {
            'build_button': pygame.image.load('supply/UI/Ribbons/Ribbon_Yellow_Connection_Down.png'),
            'play_button': pygame.image.load('supply/UI/Ribbons/Ribbon_Red_Connection_Right.png'),
            'edit_button': pygame.image.load('supply/UI/Ribbons/Ribbon_Yellow_Connection_Down.png'),
            'tile': pygame.image.load('supply/UI/Buttons/Button_Disable.png'),
            'economy_button': pygame.image.load('supply/UI/Ribbons/Ribbon_Blue_Connection_Left.png'),
            'defense_button': pygame.image.load('supply/UI/Ribbons/Ribbon_Red_Connection_Left.png'),
            'wood_toggle': pygame.image.load('supply/UI/Buttons/Button_blue.png'),
            'stone_toggle': pygame.image.load('supply/UI/Buttons/Button_blue.png'),
            'text_background': pygame.image.load('supply/UI/Buttons/Button_Blue_Pressed.png')
        }

    def setup_ui_components(self):
        font_size = 24

        self.play_button = Button(20, settings.SCREEN_HEIGHT - 70, 100, 50, '', settings.BLUE, self.on_play_pressed, self.resources['play_button'])
        self.build_button = Button(settings.SCREEN_WIDTH - 80, 20, 100, 50, 'Build', settings.BLUE, self.toggle_build_menu, self.resources['build_button'])
        self.edit_button = Button(settings.SCREEN_WIDTH - 150, 20, 100, 50, 'Edit', settings.BLUE, self.toggle_edit_mode, self.resources['edit_button'])
        self.economy_button = Button(settings.SCREEN_WIDTH - 80, 90, 100, 50, 'Economy', settings.GREY, self.toggle_economy_menu, self.resources['economy_button'])
        self.defense_button = Button(settings.SCREEN_WIDTH - 80, 150, 100, 50, 'Defense', settings.GREY, self.toggle_defense_menu, self.resources['defense_button'])

        self.currency_display = TextDisplay(
            20, 20,
            f'Currency: {self.currency_handler.get_currency()}',
            settings.GREEN,
            self.resources.get('text_background'),
            font_size=font_size
        )

        self.resource_displays = {
            'currency': TextDisplay(20, 20, 'Currency: ' + str(self.currency_handler.get_currency()), settings.GREEN, self.resources['text_background'], font_size),
            'wood': TextDisplay(20, 50, 'Wood: ' + str(self.currency_handler.wood), settings.GREEN, self.resources['text_background'], font_size),
            'stone': TextDisplay(20, 80, 'Stone: ' + str(self.currency_handler.stone), settings.GREY, self.resources['text_background'], font_size),
            'iron': TextDisplay(20, 110, 'Iron: ' + str(self.currency_handler.iron), settings.GREY, self.resources['text_background'], font_size),
            'magica': TextDisplay(20, 140, 'Magica: ' + str(self.currency_handler.magica), settings.BLUE, self.resources['text_background'], font_size)
        }

        self.components.extend([
            self.play_button, self.build_button, self.edit_button, self.economy_button, self.defense_button, self.currency_display,
        ])

    def initialize_menu_options(self):
        self.economy_options = [
            Button(settings.SCREEN_WIDTH - 80, 210, 100, 50, 'Wheat', settings.GREY, lambda: self.select_building('wheat'), self.resources['tile']),
            Button(settings.SCREEN_WIDTH - 80, 270, 100, 50, 'Corn', settings.GREY, lambda: self.select_building('corn'), self.resources['tile']),
            Button(settings.SCREEN_WIDTH - 80, 330, 100, 50, 'Mill', settings.GREY, lambda: self.select_building('mill'), self.resources['tile']),
            Button(settings.SCREEN_WIDTH - 80, 390, 100, 50, 'House', settings.GREY, lambda: self.select_building('house'), self.resources['tile']),
            Button(settings.SCREEN_WIDTH - 80, 450, 100, 50, 'Smith', settings.GREY, lambda: self.select_building('smith'), self.resources['tile'])
        ]
        self.defense_options = [
            Button(settings.SCREEN_WIDTH - 80, 210, 100, 50, 'Archer', settings.GREY, lambda: self.select_building('archer'), self.resources['tile']),
            Button(settings.SCREEN_WIDTH - 80, 270, 100, 50, 'Barrack', settings.GREY, lambda: self.select_building('barrack'), self.resources['tile']),
            Button(settings.SCREEN_WIDTH - 80, 330, 100, 50, 'Ballista', settings.GREY, lambda: self.select_building('ballista'), self.resources['tile']),
            Button(settings.SCREEN_WIDTH - 80, 390, 100, 50, 'Wizard', settings.GREY, lambda: self.select_building('wizard'), self.resources['tile'])
        ]

    def on_play_pressed(self):
        if not self.phase_handler.phase_active:
            self.phase_handler.start_next_wave()
            self.state_handler.change_state(GameStates.GAME_PLAY)
        else:
            print("A wave is currently active.")

    def toggle_build_menu(self):
        if self.economy_button not in self.components:
            self.components.extend([self.economy_button, self.defense_button])
        else:
            self.hide_submenus()
            self.components.remove(self.economy_button)
            self.components.remove(self.defense_button)

    def toggle_edit_mode(self):
        if not self.state_handler.current_state == GameStates.GAME_PLAY:
            self.edit_mode_active = not self.edit_mode_active
            if self.edit_mode_active:
                self.state_handler.change_state(GameStates.EDIT_MODE)
            else:
                self.state_handler.change_state(GameStates.BUILD_MODE)
        else:
            print("You can't edit now, monsters are here.")

    def toggle_economy_menu(self):
        self.hide_submenus()
        self.toggle_menu_options(self.economy_options)

    def toggle_defense_menu(self):
        self.hide_submenus()
        self.toggle_menu_options(self.defense_options)

    def toggle_menu_options(self, options):
        if options[0] not in self.components:
            self.components.extend(options)
        else:
            for option in options:
                self.components.remove(option)

    def toggle_wood(self):
        pass

    def toggle_stone(self):
        pass

    def hide_submenus(self):
        all_options = self.economy_options + self.defense_options
        for option in all_options:
            if option in self.components:
                self.components.remove(option)

    def handle_event(self, event):
        for component in self.components:
            if isinstance(component, Button) and component.is_clicked(event):
                component.action()

    def update(self):
        current_currency = self.currency_handler.get_currency()
        currency_text = f'Currency: {current_currency}'
        if self.currency_display.text != currency_text:
            self.currency_display.update_text(currency_text)

        for key, display in self.resource_displays.items():
            new_text = f'{key.capitalize()}: {getattr(self.currency_handler, key)}'
            if display.text != new_text:
                display.update_text(new_text)

    def draw(self):
        for component in self.components:
            component.draw(self.screen)
            
    def select_building(self, building_type):
        from entities.base_tower import Tower
        
        price = Tower.get_price(building_type)
        if self.currency_handler.can_afford(price):
            sprite_path = Tower.tower_sprites[building_type]
            self.event_handler.start_dragging(building_type, sprite_path, price)
            self.update()
        else:
            print("Not enough currency to build this tower")
