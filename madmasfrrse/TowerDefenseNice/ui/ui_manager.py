from ui.component_manager import ComponentManager
from ui.menu_manager import MenuManager
from ui.resource_manager import ResourceManager
from events.ui_handler import UIEventHandler
from events.tower_placement_handler import TowerPlacementHandler

class UIManager:
    def __init__(self, screen, game_context):
        self.game_context = game_context
        self.resource_manager = ResourceManager()
        self.component_manager = ComponentManager(screen, self.resource_manager, self.game_context)
        self.menu_manager = MenuManager(self.component_manager)
        self.tower_placement_handler = TowerPlacementHandler(game_context)
        self.ui_event_handler = UIEventHandler(self.component_manager, self.menu_manager, self.tower_placement_handler, self.game_context)

    def handle_events(self, events):
        for event in events:
            self.ui_event_handler.handle_event(event)

    def draw(self, screen):
        self.component_manager.draw(screen)
        self.menu_manager.draw(screen)