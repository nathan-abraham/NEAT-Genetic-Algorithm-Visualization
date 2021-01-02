import pygame
import neat
import os
from random import randrange
from character import Character
from cactus import Cactus
from bird import Bird
from bg import Bg
from viz.visualize import draw_net

# Initializing pygame screen and font
pygame.init()
pygame.font.init()

# Setting dimensions and creating window
WIN_WIDTH = 1000
WIN_HEIGHT = 720
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
WHITE = (255, 255, 255) # Tuple containing white RGB values
BLACK = (0, 0, 0) # Tuple containing black RGB values
GEN = 0 # Keeps track of the number of generations
show_lines = True # Can set to false if you do not want the vision lines drawn

STAT_FONT = pygame.font.SysFont("comicsans", 50) # Font used to blit to screen

def redraw_window(win, base, men, cacti, score, birds, gen, alive, cactus_ind, bird_ind):
    win.fill(WHITE) # Fill the window with white every frame
    base.draw(win) # Draws background
    for man in men:
        if not man.isSlide:
            man.walk(win)
        else:
            man.duck(win)
    for cactus in cacti:
        if cacti[cactus_ind] == cactus:
            cactus.draw(win)
            if show_lines:
                for man in men:
                    cactus.select_draw(win, man)
        else:
            cactus.draw(win)
    for bird in birds:
        if birds[bird_ind] == bird:
            bird.fly(win)
            if show_lines:
                for man in men:
                    bird.select_draw(win, man)
        else:
            bird.fly(win)

    # Note: the use of f strings here requires python 3.6 or higher
    # Blitting score, generation, and number alive to the screen
    text = STAT_FONT.render(f'Score: {score}', 1, BLACK)
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render(f'Gen: {gen}', 1, BLACK)
    win.blit(text, (10, 10))

    text = STAT_FONT.render(f'Alive: {alive}', 1, BLACK)
    win.blit(text, (10, 50))

    pygame.display.update() # Update display


def fitness_function(genomes, config):
    global GEN
    GEN += 1 # Increase generation with every call of the fitness_function
    FPS = 30 # Increasing FPS also increases dino speed

    run = True
    clock = pygame.time.Clock() # Keeps track of framerate and main loop speed
    score = 0

    men = [] # Holds each dinosaur
    nets = [] # Holds each network associated with the dinosaur at the same index
    ge = [] # Holds each genome associated with the dinosaur at the same index

    base = Bg()
    cacti = [Cactus(700, 0)]
    birds = [Bird(1200, 1)]
    bird_ind = 0
    cactus_ind = 0

    # Used for slowly speeding up the game
    difficulties = []
    score_levels = []
    for i in range(20):
        difficulties.append(14 + i)
    for j in range(1, 21):
        score_levels.append(5 * j)

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config) # Create a feed-forward network with the genome
        nets.append(net) # Append the net to the list of networks
        men.append(Character(50)) # Append a dino to the list of dinos
        g.fitness = 0 # Set fitness to zero by default
        ge.append(g) # Append a genome

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
                cactus_ind = 1 # Figuring out the current cactus
            if len(birds) > 1 and men[0].x > birds[0].x + birds[0].IMG.get_width():
                bird_ind = 1 # Figuring out the current bird
        else:
            run = False
            break

        redraw_window(win, base, men, cacti, score, birds, GEN, alive, cactus_ind, bird_ind)

        for x, man in enumerate(men):
            ge[x].fitness += 0.1 # Increase their fitness just for surviving, but only a little bit

            '''
            Most important part of the program:
            1. Activate the neural network by passing in the following four inputs: The dino's x coordinate,
            the absolute value of the dino's x coordinate minus the cactus's x coordinate, the absolute
            value of the dino's y coordinate minus the cactus's y coordinate, the absolute value of the dino's
            x coordinate minus the bird's x coordinate, and the absolute value of the dino's y coordinate minus
            the bird's y coordinate
            2. Gets the outputs from the neural network for a specific dino
            3. If the first output is greater than a certain value, jump
            4. If the second output is greater than a certain value, slide
            '''
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

        rem_cactus = [] # List of cacti to remove
        rem_bird = [] # List of birds to remove
        add_cactus = False # Boolean value deciding whether to add a new cactus
        add_bird = False # Boolean value deciding whether to add a new bird
        cactus_offset = 0 # X coordinate difference between the current cactus and the next one
        bird_offset = 0 # X coordinate difference between the current bird and the next one

        for cactus in cacti:
            for x, man in enumerate(men):
                if cactus.collide(man):
                    ge[x].fitness -= 1 # Decrease fitness for colliding
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
                    ge[x].fitness -= 1 # Decrease fitness for colliding
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
                g.fitness += 5 # increase fitness for passing a cactus
            cacti.append(Cactus(cactus_offset, randrange(0, 3)))


        if add_bird:
            bird_offset = randrange(500, 800)
            score += 1
            for g in ge:
                g.fitness += 5 # increase fitness for adding a bird
            if score <= 15:
                birds.append(Bird(cacti[0].x + bird_offset, 1))
            else:
                birds.append(Bird(cacti[0].x + bird_offset, randrange(0, 2)))

        for r in rem_cactus:
            cacti.remove(r) # Remove all the cacti that the dinos have passed
        for i in rem_bird:
            birds.remove(i) # Remove all the birds the dinos have passed

        # Increases scroll speed slightly
        for k in range(len(score_levels)):
            if score == score_levels[k]:
                base.VEL = difficulties[k]

        # Match the background scroll speed with the obstacles' scroll speed
        for cactus in cacti:
            cactus.VEL = base.VEL
        for bird in birds:
            bird.VEL = base.VEL

        base.move() # Move background

# The following function sets up the population, reports statistics, initializes
# the config file values, and runs the fitness function
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(fitness_function, 50)

# Connects the config file to this python file using the os module
if __name__ == "__main__":
    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, "config.txt")
    run(config_path)
