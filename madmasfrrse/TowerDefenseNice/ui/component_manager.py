from settings import settings
from ui.components.button import Button
from ui.components.text_display import TextDisplay  # Ensure you have this import

class ComponentManager:
    def __init__(self, screen, resource_manager, game_context):
        self.screen = screen
        self.resource_manager = resource_manager
        self.game_context = game_context  # Pass GameContext to access currency
        self.components = []
        self.setup_ui_components()

    def setup_ui_components(self):
        build_button = Button(
            settings.SCREEN_WIDTH - 100, 20, 100, 50, 'Build', settings.GREEN, 'toggle_build_menu',
            self.resource_manager, 'build_button', visible=True
        )
        self.components.append(build_button)

        play_button = Button(
            20, settings.SCREEN_HEIGHT - 70, 100, 50, 'Play', settings.BLUE, 'on_play_pressed',
            self.resource_manager, 'play_button', visible=True
        )
        self.components.append(play_button)

        edit_button = Button(
            settings.SCREEN_WIDTH - 160, 20, 100, 50, 'Edit', settings.GREEN, 'on_edit_pressed',
            self.resource_manager, 'edit_button', visible=True
        )
        self.components.append(edit_button)

        # Initialize currency display
        self.currency_display = TextDisplay(
            20, 20, f"Currency: {self.game_context.currency_handler.get_currency()}", settings.GREEN, 24
        )
        self.components.append(self.currency_display)

    def update_ui(self):
        """Update the UI components based on changes in game context."""
        # Update the currency display with the current currency
        current_currency = self.game_context.currency_handler.get_currency()
        self.currency_display.update_text(f"Currency: {current_currency}")

    def draw(self, screen):
        for component in self.components:
            component.draw(screen)
        self.update_ui()  # Ensure UI updates happen at each draw call

# Make sure you pass the game_context when initializing the ComponentManager
# component_manager = ComponentManager(screen, resource_manager, game_context)
