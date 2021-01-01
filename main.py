import pygame
import neat
import os
from random import randrange
from character import Character
from cactus import Cactus
from bird import Bird
from bg import Bg
from viz.visualize import draw_net

pygame.init()
pygame.font.init()

WIN_WIDTH = 1000
WIN_HEIGHT = 720
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
GEN = 0

STAT_FONT = pygame.font.SysFont("comicsans", 50)

def redraw_window(win, base, men, cacti, score, birds, gen, alive, cactus_ind, bird_ind):
    win.fill((255, 255, 255))
    base.draw(win)
    for man in men:
        if not man.isSlide:
            man.walk(win)
        else:
            man.duck(win)
    for cactus in cacti:
        if cacti[cactus_ind] == cactus:
            cactus.draw(win)
            for man in men:
                cactus.select_draw(win, man)
        else:
            cactus.draw(win)
    for bird in birds:
        if birds[bird_ind] == bird:
            bird.fly(win)
            for man in men:
                bird.select_draw(win, man)
        else:
            bird.fly(win)

    text = STAT_FONT.render(f'Score: {score}', 1, (0, 0, 0))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render(f'Gen: {gen}', 1, (0, 0, 0))
    win.blit(text, (10, 10))

    text = STAT_FONT.render(f'Alive: {alive}', 1, (0, 0, 0))
    win.blit(text, (10, 50))

    pygame.display.update()


def fitness_function(genomes, config):
    global GEN
    GEN += 1
    FPS = 30

    run = True
    clock = pygame.time.Clock()
    score = 0

    men = []
    nets = []
    ge = []

    base = Bg()
    cacti = [Cactus(700, 0)]
    birds = [Bird(1200, 1)]
    bird_ind = 0
    cactus_ind = 0

    difficulties = []
    score_levels = []
    for i in range(20):
        difficulties.append(14 + i)
    for j in range(1, 21):
        score_levels.append(5 * j)

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        men.append(Character(50))
        g.fitness = 0
        ge.append(g)

    alive = len(men)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        cactus_ind = 0
        bird_ind = 0
        if alive > 0:
            if len(cacti) > 1 and men[0].x > cacti[0].x + cacti[0].IMG.get_width():
                cactus_ind = 1
            if len(birds) > 1 and men[0].x > birds[0].x + birds[0].IMG.get_width():
                bird_ind = 1
        else:
            run = False
            break

        redraw_window(win, base, men, cacti, score, birds, GEN, alive, cactus_ind, bird_ind)

        for x, man in enumerate(men):
            ge[x].fitness += 0.1
            output = nets[x].activate((man.x, abs(man.x - cacti[cactus_ind].x),
                                      abs(man.y - cacti[cactus_ind].y),
                                      abs(man.x - birds[bird_ind].x),
                                      abs(man.y - birds[bird_ind].y)))

            if not man.isJump:
                if output[0] > 0.5 and not man.isSlide:
                    man.isJump = True
            else:
                man.jump()

            if not man.isSlide:
                if output[1] > 0.5:
                    man.isSlide = True

        rem_cactus = []
        rem_bird = []
        add_cactus = False
        add_bird = False
        cactus_offset = 0
        bird_offset = 0

        for cactus in cacti:
            for x, man in enumerate(men):
                if cactus.collide(man):
                    ge[x].fitness -= 1
                    men.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    alive -= 1
                if not cactus.passed and cactus.x < man.x:
                    cactus.passed = True
                    if cactus.x < 500:
                        add_cactus = True

            if cactus.x + cactus.IMG.get_width() < 0:
                rem_cactus.append(cactus)

            cactus.move()

        for bird in birds:
            for x, man in enumerate(men):
                if bird.collide(man):
                    ge[x].fitness -= 1
                    men.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    alive -= 1
                if not bird.passed and bird.x < man.x:
                    bird.passed = True
                    if bird.x < 500:
                        add_bird = True

            if bird.x + bird.IMG.get_width() < 0:
                rem_bird.append(bird)

        if add_cactus:
            cactus_offset = randrange(1200, 1800)
            score += 1
            for g in ge:
                g.fitness += 5
            cacti.append(Cactus(cactus_offset, randrange(0, 3)))


        if add_bird:
            bird_offset = randrange(500, 800)
            score += 1
            for g in ge:
                g.fitness += 5
            if score <= 15:
                birds.append(Bird(cacti[0].x + bird_offset, 1))
            else:
                birds.append(Bird(cacti[0].x + bird_offset, randrange(0, 2)))

        for r in rem_cactus:
            cacti.remove(r)
        for i in rem_bird:
            birds.remove(i)

        for k in range(len(score_levels)):
            if score == score_levels[k]:
                base.VEL = difficulties[k]

        for cactus in cacti:
            cactus.VEL = base.VEL
        for bird in birds:
            bird.VEL = base.VEL

        base.move()

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(fitness_function, 50)
    #draw_net(config, winner)

if __name__ == "__main__":
    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, "config.txt")
    run(config_path)
