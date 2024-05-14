from settings import settings
from ui.components.button import Button

class MenuManager:
    def __init__(self, component_manager):
        self.component_manager = component_manager
        self.build_menu = self.create_build_menu()
        self.economy_submenu = self.create_economy_submenu()
        self.defense_submenu = self.create_defense_submenu()

    def create_build_menu(self):
        return [
            Button(settings.SCREEN_WIDTH - 100, 90, 100, 50, 'Economy', settings.GREEN, 'toggle_economy', self.component_manager.resource_manager, 'economy_button', visible=False),
            Button(settings.SCREEN_WIDTH - 100, 150, 100, 50, 'Defense', settings.GREEN, 'toggle_defense', self.component_manager.resource_manager, 'defense_button', visible=False)
        ]

    def create_economy_submenu(self):
        names = ['Wheat', 'House', 'Corn', 'Smith', 'Mill']
        return [
            Button(settings.SCREEN_WIDTH - 100, 220 + i * 60, 100, 50, name, settings.GREEN, f'start_dragging_{name.lower()}', self.component_manager.resource_manager, 'tile', visible=False)
            for i, name in enumerate(names)
        ]

    def create_defense_submenu(self):
        names = ['Archer', 'Barracks', 'Ballista', 'Wizard']
        return [
            Button(settings.SCREEN_WIDTH - 100, 220 + i * 60, 100, 50, name, settings.RED, f'start_dragging_{name.lower()}', self.component_manager.resource_manager, 'tile', visible=False)
            for i, name in enumerate(names)
        ]

    def toggle_submenu(self, submenu):
        target_submenu = self.economy_submenu if submenu == 'economy' else self.defense_submenu
        other_submenu = self.defense_submenu if submenu == 'economy' else self.economy_submenu

        for button in target_submenu:
            button.visible = not button.visible

        for button in other_submenu:
            button.visible = False

    def draw(self, screen):
        for button in self.build_menu + self.economy_submenu + self.defense_submenu:
            if button.visible:
                button.draw(screen)