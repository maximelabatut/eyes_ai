import pygame
import numpy as np
import time

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def create_gradient(colors, size):
    """
    Crée un gradient linéaire horizontal de la largeur 'size' avec les couleurs 'colors'.
    colors = list of (pos [0-1], (r,g,b))
    """
    gradient = pygame.Surface((size, 1), pygame.SRCALPHA)
    for x in range(size):
        pos = x / (size - 1)
        # Trouver deux couleurs entre lesquelles interpoler
        for i in range(len(colors) -1):
            p1, c1 = colors[i]
            p2, c2 = colors[i+1]
            if p1 <= pos <= p2:
                local_t = (pos - p1) / (p2 - p1)
                col = lerp_color(c1, c2, local_t)
                gradient.set_at((x, 0), (*col, 255))
                break
    return gradient

def apply_alpha_mask(surface, mask):
    """Applique un masque alpha sur surface (surface et mask doivent être mêmes dimensions)."""
    arr_surf = pygame.surfarray.pixels_alpha(surface)
    arr_mask = pygame.surfarray.pixels_alpha(mask)
    np.minimum(arr_surf, arr_mask, out=arr_surf)
    del arr_surf
    del arr_mask

def draw_rectangular_ribbon(surface, rect, thickness, colors, speed=0.6):
    width, height = rect.width, rect.height
    perimeter = 2 * (width + height)
    t = (time.time() * speed) % 1

    ribbon_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    ribbon_surf.fill((0, 0, 0, 0))

    grad_length = perimeter
    gradient = create_gradient(colors, int(grad_length))

    def get_color_at(dist):
        pos = (dist / perimeter + t) % 1
        x = int(pos * (grad_length - 1))
        return gradient.get_at((x, 0))[:3]

    # Bord haut
    for x in range(width):
        color = get_color_at(x)
        for y in range(thickness):
            ribbon_surf.set_at((x, y), (*color, 255))

    # Bord droit
    for y in range(height):
        dist = width + y
        color = get_color_at(dist)
        for x in range(width - thickness, width):
            ribbon_surf.set_at((x, y), (*color, 255))

    # Bord bas
    for x in range(width):
        dist = width + height + (width - x)
        color = get_color_at(dist)
        for y in range(height - thickness, height):
            ribbon_surf.set_at((x, y), (*color, 255))

    # Bord gauche
    for y in range(height):
        dist = width + height + width + (height - y)
        color = get_color_at(dist)
        for x in range(thickness):
            ribbon_surf.set_at((x, y), (*color, 255))

    # *** Ici, NE PAS appliquer de flou ***
    surface.blit(fast_blur(ribbon_surf), rect.topleft)  # retirer cette ligne
    surface.blit(ribbon_surf, rect.topleft)  # afficher directement



def fast_blur(surface):
    """
    Blur rapide simple par downscale et upscale.
    """
    scale = 1/4  # réduire la taille pour effet flou
    size = surface.get_size()
    small_size = (max(1, int(size[0]*scale)), max(1, int(size[1]*scale)))

    small = pygame.transform.smoothscale(surface, small_size)
    blurred = pygame.transform.smoothscale(small, size)
    return blurred
