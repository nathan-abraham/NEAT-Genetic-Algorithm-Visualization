import pygame
import os

BASE_IMG = pygame.image.load(os.path.join("data", "Track.png")).convert_alpha()

class Bg:
    VEL = 14
    IMG = BASE_IMG
    WIDTH = BASE_IMG.get_width()

    def __init__(self):
        self.x1 = 0
        self.y = 562
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
