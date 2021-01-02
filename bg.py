import pygame
import os

# Load image
BASE_IMG = pygame.image.load(os.path.join("data", "Track.png")).convert_alpha()

class Bg:
    VEL = 14 # Initial velocity
    IMG = BASE_IMG
    WIDTH = BASE_IMG.get_width() # Width of image

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
        # Blits two copies of the background right next to each other to give the scrolling effect
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
