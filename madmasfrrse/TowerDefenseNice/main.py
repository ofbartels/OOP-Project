import sys
import time
import pygame

from environment.initializer import TileMapInitializer
from events.currency_handler import CurrencyHandler
from events.input_handler import InputHandler
from events.phase_handler import PhaseHandler
from events.state_handler import StateHandler
from game_context import GameContext
from entities.main_tower.main_tower import MainTower
from ui.ui_manager import UIManager
from utils.camera import Camera

def main():
    pygame.init()
    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    fps = 60

   # Initialize Singleton Game Context...
    initializer = TileMapInitializer(25, 25)
    tilemap = initializer.initialize_tilemap()
    currency_handler = CurrencyHandler()
    state_handler = StateHandler()
    game_context = GameContext(screen, tilemap, currency_handler, state_handler, None, None)
    phase_handler = PhaseHandler(game_context)
    game_context.phase_handler = phase_handler
    main_tower = MainTower(game_context)
    game_context.main_tower = main_tower
    camera = Camera(0, 0, game_context)
    game_context.camera = camera
    ui_manager = UIManager(screen, game_context)
    game_context.tower_placement_handler = ui_manager.tower_placement_handler
    input_handler = InputHandler(camera)
    input_handler.register_listener(ui_manager.ui_event_handler)
    game_context.enemies = phase_handler.get_enemies()
    # Main
    running = True
    last_time = time.time()
    while running:
        current_time = pygame.time.get_ticks()
        delta_time = current_time - last_time
        last_time = current_time

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            input_handler.handle_events([event])

        screen.fill((0, 0, 0))
        updated_rects = tilemap.draw(game_context)
        entities = tilemap.objects + game_context.towers + main_tower.parts + game_context.enemies
        entities.sort(key=lambda x: x.z_index)

        # Draw all entities
        entities = game_context.tile_map.objects + game_context.towers + game_context.main_tower.parts + game_context.enemies
        entities.sort(key=lambda x: x.z_index)
        for entity in entities:
            entity.draw(game_context)

        # Update enemies
        enemies_to_remove = []
        for enemy in game_context.enemies:
            if enemy.mark_for_removal:
                enemies_to_remove.append(enemy)
            else:
                enemy.update(game_context, delta_time)

        # Remove marked enemies
        for enemy in enemies_to_remove:
            game_context.enemies.remove(enemy)

        # Update towers
        towers_to_remove = []
        for tower in game_context.towers:
            if tower.mark_for_removal:
                towers_to_remove.append(tower)
            else:
                tower.update(current_time, game_context)

        # Remove marked towers
        for tower in towers_to_remove:
            game_context.towers.remove(tower)

        # Update game phases
        phase_handler.update(current_time)

        ui_updated_rects = ui_manager.draw(screen) or []
        updated_rects.extend(ui_updated_rects)
        ui_manager.tower_placement_handler.draw_tower_preview(screen)
        
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
