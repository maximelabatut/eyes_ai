import pygame
import math

class Mouth:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color = (0, 0, 0)
        self.position = (self.screen_width // 2, self.screen_height * 3 // 4)

        self.width = 80.0
        self.height = 1.0
        self.shape_type = "arc"
        self.start_angle = 0.0
        self.end_angle = math.pi

        self._target_width = 80.0
        self._target_height = 1.0
        self._target_shape_type = "arc"
        self._target_start_angle = 0.0
        self._target_end_angle = math.pi

    def set_expression(self, expression_data):
        self._target_width = float(expression_data.get("width", 80))
        self._target_height = float(expression_data.get("height", 5))
        shape = expression_data.get("shape", "straight")

        if shape == "smile":
            self._target_shape_type = "arc"
            self._target_start_angle = math.pi  # <-- inversé ici
            self._target_end_angle = 2 * math.pi  # <-- et ici
        elif shape == "frown":
            self._target_shape_type = "arc"
            self._target_start_angle = 0.0
            self._target_end_angle = math.pi
        elif shape == "straight":
            self._target_shape_type = "straight"
            self._target_height = 0.0
        elif shape == "oval":
            self._target_shape_type = "oval"

    def update(self, dt):
        lerp_rate = 0.1
        self.width += (self._target_width - self.width) * lerp_rate
        self.height += (self._target_height - self.height) * lerp_rate

        self.start_angle += (self._target_start_angle - self.start_angle) * lerp_rate
        self.end_angle += (self._target_end_angle - self.end_angle) * lerp_rate

        # IMPORTANT : utiliser le type cible et non forcer arc
        self.shape_type = self._target_shape_type

    def set_listening_mode(self, on: bool, expressions_dict=None):
        if expressions_dict is None:
            return

        if on and "happy" in expressions_dict:
            self.set_expression(expressions_dict["happy"]["mouth"])
        else:
            if "normal" in expressions_dict:
                self.set_expression(expressions_dict["normal"]["mouth"])

    def draw(self):
        x, y = self.position
        half_width = self.width / 2

        # Si la hauteur est très faible, on dessine une ligne droite au lieu d'un arc
        if self.height < 2:
            pygame.draw.line(self.screen, self.color, (x - half_width, y), (x + half_width, y), 3)
        else:
            rect = pygame.Rect(x - half_width, y - self.height, self.width, self.height * 2)
            max_width = min(rect.width, rect.height) // 2
            width = min(5, max_width)
            pygame.draw.arc(self.screen, self.color, rect, self.start_angle, self.end_angle, width)
