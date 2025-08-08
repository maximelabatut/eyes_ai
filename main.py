#!/usr/bin/env python3
import pygame
import random
import time

from eye import Eye
from mouth import Mouth
from expressions import expressions
import rectangular_glow  # <-- Import ruban lumineux

pygame.init()

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Assistant Kawaii")

font = pygame.font.SysFont(None, 24)

iris_color = (
    random.randint(50, 255),
    random.randint(50, 255),
    random.randint(50, 255)
)

left_eye = Eye(screen, SCREEN_WIDTH, SCREEN_HEIGHT, is_left_eye=True, iris_color=iris_color)
right_eye = Eye(screen, SCREEN_WIDTH, SCREEN_HEIGHT, is_left_eye=False, iris_color=iris_color)
mouth = Mouth(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

clock = pygame.time.Clock()

time_to_next_blink = time.time() + random.uniform(2, 5)
time_to_next_expression_change = time.time() + random.uniform(5, 10)
time_to_next_pupil_move = time.time() + random.uniform(0.5, 2.0)

current_expression = "normal"
expression_data = expressions[current_expression]

left_eye.set_target_pupil_position(expression_data["left_eye"]["pupil_pos"][0],
                                   expression_data["left_eye"]["pupil_pos"][1])
right_eye.set_target_pupil_position(expression_data["right_eye"]["pupil_pos"][0],
                                    expression_data["right_eye"]["pupil_pos"][1])
mouth.set_expression(expression_data["mouth"])

# Variables pour mode "listening"
listening_mode = False
listening_start_time = 0
LISTENING_DURATION = 5  # secondes

# Couleurs ruban ruban orange-violet-bleu comme dans rectangular_ribbon.py
ribbon_colors = [
    (0.0, (238, 75, 43)),  # orange
    (0.33, (140, 0, 255)),  # violet
    (0.66, (0, 200, 255)),  # bleu
    (1.0, (238, 75, 43))  # boucle orange
]


def enter_listening_mode():
    global listening_mode, listening_start_time
    listening_mode = True
    listening_start_time = time.time()
    print("Mode écoute activé")


running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            enter_listening_mode()

    current_time = time.time()

    # Sortir du mode écoute après délai
    if listening_mode and (current_time - listening_start_time > LISTENING_DURATION):
        listening_mode = False
        # Revenir à l'expression normale
        expression_data = expressions[current_expression]
        left_eye.set_target_pupil_position(expression_data["left_eye"]["pupil_pos"][0],
                                           expression_data["left_eye"]["pupil_pos"][1])
        right_eye.set_target_pupil_position(expression_data["right_eye"]["pupil_pos"][0],
                                            expression_data["right_eye"]["pupil_pos"][1])
        mouth.set_expression(expression_data["mouth"])
    screen.fill((230, 230, 235))  # Un gris très clair légèrement bleuté

    if listening_mode:
        # Appliquer mode écoute sur yeux et bouche (si tu as cette logique dans tes classes)
        left_eye.set_listening_mode(listening_mode, expressions)
        right_eye.set_listening_mode(listening_mode, expressions)
        mouth.set_listening_mode(listening_mode, expressions)

        # Dessiner le ruban lumineux autour de toute la fenêtre
        rectangular_glow.draw_rectangular_ribbon(
            screen,
            pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
            thickness=5,
            colors=ribbon_colors,
            speed=0.4
        )
    else:
        left_eye.set_listening_mode(False, expressions)
        right_eye.set_listening_mode(False, expressions)

        # Mouvement pupilles
        if current_time > time_to_next_pupil_move:
            time_to_next_pupil_move = current_time + random.uniform(0.5, 2.0)
            pupil_x = random.randint(-15, 15)
            pupil_y = random.randint(-15, 15)
            left_eye.set_target_pupil_position(pupil_x, pupil_y)
            right_eye.set_target_pupil_position(pupil_x, pupil_y)

        # Clignement des yeux
        if current_time > time_to_next_blink:
            time_to_next_blink = current_time + random.uniform(2, 5)
            left_eye.start_blink()
            right_eye.start_blink()

        # Changement d'expression
        if current_time > time_to_next_expression_change:
            time_to_next_expression_change = current_time + random.uniform(3, 8)
            new_expression = random.choice(list(expressions.keys()))
            print(f"Nouvelle expression : {new_expression}")

            current_expression = new_expression
            expression_data = expressions[new_expression]

            left_eye.set_target_pupil_position(expression_data["left_eye"]["pupil_pos"][0],
                                               expression_data["left_eye"]["pupil_pos"][1])
            right_eye.set_target_pupil_position(expression_data["right_eye"]["pupil_pos"][0],
                                                expression_data["right_eye"]["pupil_pos"][1])
            mouth.set_expression(expression_data["mouth"])

    left_eye.update(dt)
    right_eye.update(dt)
    mouth.update(dt)

    left_eye.draw()
    right_eye.draw()
    mouth.draw()

    #if listening_mode:
        # Afficher un texte d'indication
        #text_surface = font.render("Je t'écoute...", True, (0, 0, 0))
        #screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT - 30))

    pygame.display.flip()

pygame.quit()
