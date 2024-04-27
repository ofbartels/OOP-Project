import pygame, random, time
from settings import settings
from environment import TileMap
from ui.start_menu import StartMenu
from entities.main_tower import MainTower
from entities.towers import ArcherTower, BarrackTower, WheatTower, CornTower, HouseTower
from handlers import CurrencyHandler, UIManager, PhaseHandler, StateHandler, GameStates, EventHandler
from utils.camera import Camera
from environment.decorations.cloud import CloudManager
pygame.init()
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.RESIZABLE)

clock = pygame.time.Clock()
camera = Camera(0, 0)
settings.set_camera(camera)

# pygame.mixer.init()
# pygame.mixer.music.load('supply/Sounds/music.wav')
# pygame.mixer.music.set_volume(0.5)
# pygame.mixer.music.play(-1)

towers = []
soldiers = []
villagers = []
trees = []
stones = []
cloud_manager = CloudManager()

default_tile_image_path = 'supply/Enviroument/Spring/grass.png'
special_tile_image_path = 'supply/Enviroument/Spring/ground(1).png'
tile_map = TileMap(settings.ROWS, settings.COLS, default_tile_image_path, special_tile_image_path)
for row in tile_map.tiles:
    for tile in row:
        if tile.object:
            if tile.object.type == 'tree':  # Assuming each tile object has a 'type' attribute
                trees.append(tile.object)
            elif tile.object.type == 'stone':
                stones.append(tile.object)

state_handler = StateHandler()
currency_handler = CurrencyHandler()
phase_handler = PhaseHandler()
event_handler = EventHandler(camera, tile_map, towers, currency_handler, state_handler)
ui_handler = UIManager(screen, currency_handler, event_handler, state_handler, phase_handler)

main_tower = MainTower(tile_map, state_handler)

def main():
    running = True
    last_time = time.time()
    start_menu = StartMenu(screen)
    enemies = phase_handler.get_enemies()

    while running:
        current_time = pygame.time.get_ticks()
        delta_time = current_time - last_time
        last_time = current_time

        """EVENT HANDLER"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if state_handler.current_state == GameStates.START_MENU:
                start_menu.handle_event(event, state_handler)
            else:
                ui_handler.handle_event(event)
                event_handler.handle_events(event)
        if state_handler.current_state == GameStates.START_MENU:
            start_menu.draw()
        else:
            """DRAW & UPDATE METHODS"""
            screen.fill(settings.WHITE)
            tile_map.draw(screen, camera)

            # Initialize and gather all drawable entities
            entities = trees + stones + towers + main_tower.parts
            entities.sort(key=lambda x: x.z_index)  # Sort entities by z-index before drawing

            for entity in entities:
                entity.draw(screen, camera)

            for enemy in enemies:
                enemy.update(towers, delta_time, main_tower, soldiers)
                enemy.draw(screen, camera)
                if enemy.mark_for_removal:
                    enemies.remove(enemy)

            for villager in villagers:
                villager.update(state_handler, enemies, tile_map)  # Make sure to pass whatever is needed for updating
                villager.draw(screen, camera)

            phase_ended = phase_handler.update(current_time)
            for tower in towers:
                if state_handler.current_state == GameStates.EDIT_MODE:
                    tower.show_edit_buttons = True
                else:
                    tower.show_edit_buttons = False
                if state_handler.current_state == GameStates.GAME_PLAY:
                    if isinstance(tower, ArcherTower):
                        tower.combat_update(current_time, towers, enemies, camera)
                    elif hasattr(tower, 'special_update'):
                        tower.special_update(current_time, currency_handler)
                    elif hasattr(tower, 'update_effect'):
                        tower.update_effect(towers)
                if isinstance(tower, BarrackTower):
                    tower.soldier_update(screen, towers, enemies, camera, soldiers)
                elif isinstance(tower, HouseTower):
                    tower.check_villagers(villagers)
                if tower.show_edit_buttons:
                    tower.draw_edit_mode_buttons(screen, camera)
            if event_handler.dragging_building:
                event_handler.draw_tower_preview(screen)
            cloud_manager.update(delta_time)
            cloud_manager.draw(screen, camera)

            ui_handler.update()
            ui_handler.draw()

            if phase_ended:
                for tower in towers[:]:
                    tower.end_of_phase()
                main_tower.reset_health()
                state_handler.change_state(GameStates.BUILD_MODE)
            # In your game loop

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
