try:
    import pygame
    print(f"Pygame version: {pygame.ver}")
except ImportError:
    print("Pygame is not installed.")