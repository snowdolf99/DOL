import pygame

class mover:
    def __init__(self, size, speed, life, nx, ny):
        self.size = size
        self.speed = speed
        self.life = life
        self.nx = nx
        self.ny = ny

        self.rect = pygame.Rect(self.nx, self.ny, self.size, self.size)
