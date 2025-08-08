import pygame
import math
import random
import time

class Eye:
    def __init__(self, screen, screen_width, screen_height, is_left_eye=True, iris_color=(0, 128, 255)):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_left_eye = is_left_eye

        self.sclera_radius = 50
        self.iris_radius = 35
        self.pupil_radius = 15
        self._normal_pupil_radius = 15
        self._listening_pupil_radius = 25  # pupille plus grande en mode écoute

        self.eyelid_color = (0, 0, 0)
        self.sclera_color = (255, 255, 255)
        self.iris_color = iris_color
        self.pupil_color = (0, 0, 0)

        self.x = screen_width // 4 if self.is_left_eye else screen_width * 3 // 4
        self.y = screen_height // 2

        self.pupil_position = [0.0, 0.0]         # position relative du centre pupille/iris
        self._target_pupil_pos = [0.0, 0.0]      # cible à interpoler

        self.is_blinking = False
        self.blink_progress = 0.0
        self.blink_duration = 0.2
        self.blink_timer = 0.0

        self.last_blink_time = time.time()
        self.next_blink_delay = random.uniform(2.0, 5.0)  # min 2s, max 5s

        self.listening_mode = False

        self.pupil_radius_current = self._normal_pupil_radius
        self._target_pupil_radius = self._normal_pupil_radius

    def set_target_pupil_position(self, x, y):
        # Ne fonctionne plus en mode écoute : on force centre
        if not self.listening_mode:
            self._target_pupil_pos = [float(x), float(y)]

    def start_blink(self):
        if not self.is_blinking:
            self.is_blinking = True
            self.blink_progress = 0.0
            self.blink_timer = 0.0

    def set_listening_mode(self, on: bool, expressions_dict=None):
        self.listening_mode = on
        if on:
            self._target_pupil_pos = [0.0, 0.0]  # centre iris + pupille
            self._target_pupil_radius = self._listening_pupil_radius
        else:
            self._target_pupil_radius = self._normal_pupil_radius

    def update(self, dt):
        lerp_rate = 0.1

        # Interpolation position pupille, centrée en mode écoute
        self.pupil_position[0] += (self._target_pupil_pos[0] - self.pupil_position[0]) * lerp_rate
        self.pupil_position[1] += (self._target_pupil_pos[1] - self.pupil_position[1]) * lerp_rate

        # Limiter pupille dans blanc de l’œil
        max_offset = self.sclera_radius - self.iris_radius
        dist = math.hypot(self.pupil_position[0], self.pupil_position[1])
        if dist > max_offset:
            scale = max_offset / dist
            self.pupil_position[0] *= scale
            self.pupil_position[1] *= scale

        # Animation clignement
        if self.is_blinking:
            self.blink_timer += dt
            t = self.blink_timer / self.blink_duration
            self.blink_progress = math.sin(t * math.pi)
            if t >= 1.0:
                self.is_blinking = False
                self.blink_progress = 0.0
                self.last_blink_time = time.time()
                self.next_blink_delay = random.uniform(2.0, 5.0)

        # Interpolation taille pupille
        self.pupil_radius_current += (self._target_pupil_radius - self.pupil_radius_current) * lerp_rate

    def draw_eyelashes(self, count=6, length=15, thickness=2, spread=60):
        """
        Dessine des cils en éventail uniquement sur le côté gauche pour l’œil gauche,
        et uniquement sur le côté droit pour l’œil droit.
        """
        center_x, center_y = self.x, self.y
        radius = self.sclera_radius

        def draw_fan(center_angle_deg):
            start_angle = center_angle_deg - spread / 2
            angle_step = spread / max(count - 1, 1)

            for i in range(count):
                angle_deg = start_angle + i * angle_step
                angle_rad = math.radians(angle_deg)

                start_x = center_x + radius * math.cos(angle_rad)
                start_y = center_y - radius * math.sin(angle_rad)

                end_x = start_x + length * math.cos(angle_rad)
                end_y = start_y - length * math.sin(angle_rad)

                pygame.draw.line(self.screen, self.eyelid_color,
                                 (start_x, start_y), (end_x, end_y), thickness)

        if self.is_left_eye:
            # Cils à gauche, angle central 180°
            draw_fan(180)
        else:
            # Cils à droite, angle central 0°
            draw_fan(0)

    def draw(self):
        # 1. Blanc de l'œil
        pygame.draw.circle(self.screen, self.sclera_color, (self.x, self.y), self.sclera_radius)

        # 2. Iris + pupille centrés sur la position actuelle de la pupille
        iris_center_x = self.x + self.pupil_position[0]
        iris_center_y = self.y + self.pupil_position[1]
        pygame.draw.circle(self.screen, self.iris_color, (int(iris_center_x), int(iris_center_y)), self.iris_radius)
        pygame.draw.circle(self.screen, self.pupil_color, (int(iris_center_x), int(iris_center_y)), int(self.pupil_radius_current))
        pygame.draw.circle(self.screen, (255, 255, 255), (int(iris_center_x + 10), int(iris_center_y - 10)), 5)

        # 3. Paupières (clignement)
        if self.blink_progress > 0.0:
            size = self.sclera_radius * 2
            lid_surface = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(lid_surface, self.eyelid_color, (self.sclera_radius, self.sclera_radius), self.sclera_radius)

            cover = int(size * (1.0 - self.blink_progress) * 0.5)
            pygame.draw.rect(lid_surface, (0, 0, 0, 0),
                             pygame.Rect(0, self.sclera_radius - cover, size, cover * 2))

            self.screen.blit(lid_surface, (self.x - self.sclera_radius, self.y - self.sclera_radius))

        self.draw_eyelashes()

        # 4. Contour
        pygame.draw.circle(self.screen, self.eyelid_color, (self.x, self.y), self.sclera_radius, 5)
