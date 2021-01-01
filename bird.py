import pygame
import os

BIRD_IMGS = [pygame.image.load(os.path.join("data", "berd.png")).convert_alpha(),
             pygame.image.load(os.path.join("data", "berd2.png")).convert_alpha()]

class Bird:
    flyCount = 0
    IMG = BIRD_IMGS[0]
    VEL = 14

    def __init__(self, x, type):
        self.x = x
        self.y = 435
        self.height = 0
        self.passed = False
        if type == 0:
            self.IMG = BIRD_IMGS[0]
            self.y = 335
        elif type == 1:
            self.IMG = BIRD_IMGS[0]
            self.y = 405
        elif type == 2:
            self.IMG = BIRD_IMGS[0]
            self.y = 495

    def fly(self, win):
        self.x -= self.VEL
        if self.flyCount + 1 >= 6:
            self.flyCount = 0
        win.blit(BIRD_IMGS[self.flyCount // 3], (round(self.x), round(self.y)))
        self.flyCount += 1

    def select_draw(self, win, man):
        '''
        self.x -= self.VEL
        if self.flyCount + 1 >= 6:
            self.flyCount = 0
        '''
        pygame.draw.rect(win, (0, 0, 255), (round(self.x), round(self.y), self.IMG.get_width(), self.IMG.get_height()), 3)
        '''
        win.blit(BIRD_IMGS[self.flyCount // 3], (round(self.x), round(self.y)))
        self.flyCount += 1
        '''
        pygame.draw.line(win, (0, 0, 255), (man.x + 96, man.y), (self.x, self.y))


    def collide(self, man):
        man_mask = man.get_mask()
        bird_mask = pygame.mask.from_surface(self.IMG)
        offset = (self.x - man.x, self.y - round(man.y))
        collision = man_mask.overlap(bird_mask, offset)
        if collision:
            return True
        return False
