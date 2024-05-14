import pygame

class ResourceManager:
    def __init__(self):
        self.images = self.load_resources()

    def load_resources(self):
        resource_paths = {
            'build_button': 'assets/ui/Yellow_Button.png',
            'play_button': 'assets/ui/Play_Button.png',
            'edit_button': 'assets/ui/Yellow_Button.png',
            'tile': 'assets/ui/Button_Tile.png',
            'economy_button': 'assets/ui/Blue_Ribbon.png',
            'defense_button': 'assets/ui/Blue_Ribbon.png',
        }
        images = {}
        for key, path in resource_paths.items():
            try:
                images[key] = pygame.image.load(path)
            except pygame.error as e:
                print(f"Failed to load {path}: {e}")
                images[key] = None
        return images

    def get_image(self, key):
        return self.images.get(key)