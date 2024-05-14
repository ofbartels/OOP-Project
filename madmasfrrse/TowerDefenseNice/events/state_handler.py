from enum import Enum, auto

class GameStates(Enum):
    START_MENU = auto()
    BUILD_MODE = auto()
    GAME_PLAY = auto()
    PAUSE = auto()
    GAME_OVER = auto()
    EDIT_MODE = auto()

class StateHandler:
    def __init__(self):
        self.current_state = GameStates.START_MENU

    def change_state(self, new_state):
        self.current_state = new_state

    def start_game(self):
        if self.current_state == GameStates.START_MENU:
            self.change_state(GameStates.BUILD_MODE)
