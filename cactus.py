import pygame
import os

# Load images
CACTI_IMGS = [pygame.image.load(os.path.join("data", "cactusBig0000.png")).convert_alpha(),
              pygame.image.load(os.path.join("data", "cactusSmall0000.png")).convert_alpha(),
              pygame.image.load(os.path.join("data", "cactusSmallMany0000.png")).convert_alpha()]


class Cactus:
    VEL = 14 # Initial velocity

    def __init__(self, x, type):
        self.x = x
        self.y = 495
        self.height = 0
        self.passed = False

        # Determines the type of the cactus
        if type == 0:
            self.IMG = CACTI_IMGS[0]
            self.y = 475
        elif type == 1:
            self.IMG = CACTI_IMGS[1]
            self.y = 515
        elif type == 2:
            self.IMG = CACTI_IMGS[2]
            self.y = 515

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))

    def select_draw(self, win, man):
        # Draws the line between the dino and the cactus for visualization purposes
        pygame.draw.rect(win, (0, 0, 255), (round(self.x), round(self.y),
                                            self.IMG.get_width(), self.IMG.get_height()), 3)
        pygame.draw.line(win, (0, 0, 255), (man.x + 96, man.y), (self.x, self.y))

    def collide(self, man):
        # Gets the masks from the images
        man_mask = man.get_mask()
        cactus_mask = pygame.mask.from_surface(self.IMG)

        # Calculates an offset necessary for the collision
        offset = (self.x - man.x, self.y - round(man.y))

        # Detects if the masks overlaps
        collision = man_mask.overlap(cactus_mask, offset)

        if collision:
            return True

        return False
