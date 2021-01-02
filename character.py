import pygame
import os

pygame.init()  # Initialize pygaem
WIN_WIDTH = 1000
WIN_HEIGHT = 720
win = pygame.display.set_mode()  # Set up display for converting images

# Load images
RUN_IMGS = [pygame.image.load(os.path.join(
    "data", "dinorun000" + str(x) + ".png")).convert_alpha() for x in range(2)]
DINO_IMGS = [pygame.image.load(os.path.join("data", "dino0000.png")).convert_alpha(),
             pygame.image.load(os.path.join("data", "dinoJump0000.png")).convert_alpha()]
DUCK_IMGS = [pygame.image.load(os.path.join("data", "dinoduck000" +
                                            str(x) + ".png")).convert_alpha() for x in range(2)]


class Character:
    IMG = DINO_IMGS[0] # Controls current image
    isJump = False # Is the dino jumping or not
    JUMPCOUNT = 10 # Used to simulate gravity
    walkCount = 0 # Used to animate the dino
    isSlide = False # Is the dino ducking or not
    slideCount = 0 # Used to animate the sliding

    def __init__(self, x):
        self.x = x
        self.y = 470
        self.vel = 0
        self.jumpCount = self.JUMPCOUNT
        self.alive = True

    def jump(self):
        if self.isJump:
            self.y -= self.jumpCount * 4
            self.jumpCount -= 1
        if self.jumpCount < -self.JUMPCOUNT:
            self.isJump = False
            self.jumpCount = self.JUMPCOUNT

    def walk(self, win):
        if self.walkCount + 1 >= 6:
            self.walkCount = 0
        if self.isJump:
            win.blit(DINO_IMGS[1], (round(self.x), round(self.y)))
        else:
            self.IMG = RUN_IMGS[self.walkCount // 3]
            win.blit(self.IMG, (round(self.x), round(self.y)))
        self.walkCount += 1

    def duck(self, win):
        if self.slideCount + 2 <= 20:
            self.y = 500
            win.blit(DUCK_IMGS[self.slideCount // 10], (round(self.x), round(self.y)+10))
            self.slideCount += 1
        else:
            self.y = 470
            self.isSlide = False
            self.slideCount = 0

    def get_mask(self):
        # Used for collision detection
        return pygame.mask.from_surface(self.IMG)
