import pygame, random, math
from settings import settings
from entities.projectile import Projectile
from entities.soldier import Soldier

class Tower:
    tower_sprites = {
        'wheat': 'supply/Economy/wheat/wheat',
        'house': 'supply/Economy/house/Wood/wood_house',
        'smith': 'supply/Economy/house/blacksmith_blue',
        'corn': 'supply/Economy/corn/corn',
        'mill': 'supply/Economy/mill/mill_blue',
        
        'archer': 'supply/Defense/Archer/archer',
        'barrack': 'supply/Defense/Barrack/barrack',
        'ballista': 'supply/Towers/Blue/castle_tower_blue',
        'wizard': 'supply/Towers/Wizard/wizard',
        'main_tower': 'supply/Economy/Main/main_tower_image.png'
    }
    tower_prices = {
        'wheat': 100, 'house': 200, 'smith': 500,
        'corn': 250, 'mill': 400, 'archer': 200,
        'barrack': 500, 'ballista': 500, 'wizard': 1250,
    }
    @staticmethod
    def get_price(building_type):
        return Tower.tower_prices.get(building_type, 0)

    def __init__(self, grid_x, grid_y, building_type, level=1, max_level=3):
        self.world_x, self.world_y = settings.iso_projection(grid_x, grid_y)
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.building_type = building_type
        self.level = level
        self.sprite = self.load_sprite()
        self.options_visible = False
        self.upgrade_button_rect = pygame.Rect(0, 0, 100, 40)
        self.delete_button_rect = pygame.Rect(0, 0, 100, 40)
        self.mark_for_removal = False
        self.projectiles = []
        self.last_attack_time = 0
        self.attack_speed = 1000
        self.z_index = self.grid_x + self.grid_y
        self.show_edit_buttons = False
        self.max_level = max_level
        self.health = 500
        self.flipped = False

    def load_sprite(self):
        sprite_path = self.tower_sprites[self.building_type] + f"({self.level}).png"
        return pygame.image.load(sprite_path).convert_alpha()

    @staticmethod
    def create_tower(grid_x, grid_y, building_type, level=1):
        from .towers import WheatTower, HouseTower, SmithTower, CornTower, MillTower, ArcherTower, BarrackTower, BallistaTower, WizardTower
        tower_classes = {
            'wheat': WheatTower, 'house': HouseTower, 'smith': SmithTower,
            'corn': CornTower, 'mill': MillTower, 'archer': ArcherTower,
            'barrack': BarrackTower, 'ballista': BallistaTower, 'wizard': WizardTower
        }
        tower_class = tower_classes.get(building_type, Tower)
        return tower_class(grid_x, grid_y, building_type, level)

    def get_upgrade_cost(self):
        return 200  # Placeholder

    def on_destroy(self):
        # Placeholder
        pass

    def reset_health(self):
        self.health = 500

    def toggle_sprite_flip(self):
        self.flipped = not self.flipped
        self.sprite = pygame.transform.flip(self.sprite, True, False)

    def draw(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        sprite_to_draw = pygame.transform.flip(self.sprite, self.flipped, False) if self.flipped else self.sprite
        screen.blit(sprite_to_draw, (screen_x - sprite_to_draw.get_width() // 2, screen_y - sprite_to_draw.get_height() // 2))

    def end_of_phase(self):
        self.health = self.max_health

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.mark_for_removal = True

    def draw_edit_mode_buttons(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        if self.show_edit_buttons:
            button_width, button_height = 40, 20
            padding = 10

            base_x = screen_x - (2 * button_width + 3 * padding) / 2 - 35
            base_y = screen_y - button_height - padding

            self.delete_button_rect = pygame.Rect(base_x, base_y, button_width, button_height)
            self.upgrade_button_rect = pygame.Rect(base_x + button_width + padding, base_y, button_width, button_height)
            self.left_button_rect = pygame.Rect(base_x + 2 * (button_width + padding), base_y, button_width, button_height)
            self.right_button_rect = pygame.Rect(base_x + 3 * (button_width + padding), base_y, button_width, button_height)

            pygame.draw.rect(screen, (255, 255, 255), self.delete_button_rect)
            pygame.draw.rect(screen, (255, 255, 255), self.upgrade_button_rect)
            pygame.draw.rect(screen, (255, 255, 255), self.left_button_rect)
            pygame.draw.rect(screen, (255, 255, 255), self.right_button_rect)

            font = pygame.font.Font(None, 18)
            delete_text = font.render('Del', True, (0, 0, 0))
            upgrade_text = font.render('Upg', True, (0, 0, 0))
            left_text = font.render('<', True, (0, 0, 0))
            right_text = font.render('>', True, (0, 0, 0))
            
            screen.blit(delete_text, (self.delete_button_rect.x + 10, self.delete_button_rect.y + 3))
            screen.blit(upgrade_text, (self.upgrade_button_rect.x + 10, self.upgrade_button_rect.y + 3))
            screen.blit(left_text, (self.left_button_rect.x + 14, self.left_button_rect.y + 3))
            screen.blit(right_text, (self.right_button_rect.x + 14, self.right_button_rect.y + 3))

            cost_text = font.render(f"${self.get_upgrade_cost()}", True, (0, 0, 0))
            screen.blit(cost_text, (self.upgrade_button_rect.x, self.upgrade_button_rect.bottom + 5))

    def draw_health_bar(self, screen, screen_x, screen_y, sprite):
        bar_length = 40
        bar_height = 5
        health_ratio = self.health / self.max_health
        fill_length = int(bar_length * health_ratio)
        bar_x = screen_x - bar_length // 2
        bar_y = screen_y - sprite.get_height() // 2 - 10

        pygame.draw.rect(screen, (128, 128, 128), (bar_x, bar_y, bar_length, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_length, bar_height))