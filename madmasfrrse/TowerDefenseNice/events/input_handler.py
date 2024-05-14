import pygame

class InputHandler:
    def __init__(self, camera):
        self.camera = camera
        self.event_listeners = []

    def register_listener(self, listener):
        if listener not in self.event_listeners:
            self.event_listeners.append(listener)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_button_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_button_up(event)
            elif event.type == pygame.MOUSEMOTION:
                self._handle_mouse_motion(event)

            self._notify_listeners(event)

    def _notify_listeners(self, event):
        for listener in self.event_listeners:
            listener.on_event(event)

    def _handle_mouse_button_down(self, event):
        if not self.camera.game_context.tower_placement_handler.dragging_building:
            if event.button == 1:  # Left mouse button
                self.camera.start_dragging(event.pos)
            elif event.button in (4, 5):  # Mouse wheel scroll
                zoom_factor = 0.1 if event.button == 4 else -0.1
                self.camera.adjust_zoom(zoom_factor)

    def _handle_mouse_button_up(self, event):
        if not self.camera.game_context.tower_placement_handler.dragging_building:
            if event.button == 1:  # Left mouse button
                self.camera.stop_dragging()

    def _handle_mouse_motion(self, event):
        if not self.camera.game_context.tower_placement_handler.dragging_building:
            if event.buttons[0]:  # Left mouse button pressed
                self.camera.update_drag(event.pos)