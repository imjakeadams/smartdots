import pygame
from pygame.locals import *
import sys
import Dot
import Obstactles
import Populations



# constants
size = width, height = 650, 650
goal_loc = (100, 10) # 325, 10
black = 0,0,0
white = 250,250,250



# Event loop
def main(dots: Populations.Population, obstacles,
         screen: pygame.Rect, goal):
    paused = False
    gen = 0
    count = 0
    best_step_count = 1000000
    # constant for when an obstacle is being actively moved, as well as a list
    # to contain the moving obstacle.
    dragging = False
    dragging_obs = []
    resizing = False
    resizing_obs = []
    resizing_corner = (0,0)
    goal_in_motion = False
    while 1:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()


            elif event.type == pygame.KEYDOWN:
                #pause the game if the spacebar is pressed.
                if event.key == pygame.K_SPACE:
                    paused = not paused
                # we want to spawn a new obstacle if the user presses the 's'
                # key.
                if event.key == pygame.K_s:
                    #if the 's' key is pressed, then spawn an obstacle
                    new_obs = Obstactles.Obstacle(screen, (50,50,0,0))
                    obstacles.add(new_obs)

            # if there is currently an obstacle that is being moved, this if
            # branch executes to allow for dragability (is that a word?) and
            # eventual placement. A movable obstacle is highlighted yellow
            # until positioned.

            if dragging:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if goal_in_motion:
                            # dots.goal_loc = dragging_obs[0].rect.topleft
                            for g in goal.spritedict:
                                g.loc = dragging_obs[0].rect.topleft
                            # main.goalx = dots.goal_loc[0]
                            # main.goaly = dots.goal_loc[1]
                            goal_in_motion = False

                            dragging_obs[0].rect.center = event.pos
                            dragging = False
                        else:
                            for obj in dragging_obs:
                                obj.rect.center = event.pos
                                obj.image.fill((250, 100, 0))
                                dragging = False




                        dragging_obs.clear()

                else:
                    for obj in dragging_obs:
                        obj.rect.center = pygame.mouse.get_pos()

            elif resizing:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        resizing = False
                        resizing_obs[0].image.fill((250, 100, 0))
                        resizing_obs.clear()
                else:

                    # The arrow keys can be used once in obstacle resizing mode
                    # to transform the size of a specific obstacle.
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            delta_pos = [og_size[0] + 10, og_size[1]]
                            resizing_obs[0].image = pygame.Surface(delta_pos)
                            resizing_obs[0].image.fill((250, 80, 0))
                            resizing_obs[0].rect = pygame.rect.Rect(og_pos,
                                     resizing_obs[0].image.get_rect().size)
                            og_size = resizing_obs[0].rect.size
                        if event.key == pygame.K_DOWN:
                            delta_pos = [og_size[0], og_size[1] + 10]
                            resizing_obs[0].image = pygame.Surface(delta_pos)
                            resizing_obs[0].image.fill((250, 80, 0))
                            resizing_obs[0].rect = pygame.rect.Rect(og_pos,
                                     resizing_obs[0].image.get_rect().size)
                            og_size = resizing_obs[0].rect.size
                        if event.key == pygame.K_LEFT:
                            delta_pos = [og_size[0] + - 10, og_size[1]]
                            resizing_obs[0].image = pygame.Surface(delta_pos)
                            resizing_obs[0].image.fill((250, 80, 0))
                            resizing_obs[0].rect = pygame.rect.Rect(og_pos,
                                     resizing_obs[0].image.get_rect().size)
                            og_size = resizing_obs[0].rect.size
                        if event.key == pygame.K_UP:
                            delta_pos = [og_size[0], og_size[1] - 10]
                            resizing_obs[0].image = pygame.Surface(delta_pos)
                            resizing_obs[0].image.fill((250, 80, 0))
                            resizing_obs[0].rect = pygame.rect.Rect(og_pos,
                                     resizing_obs[0].image.get_rect().size)
                            og_size = resizing_obs[0].rect.size


            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                        # check if any obstacle has been clicked on, and if so,
                        # change its color to indicate active movement as well
                        # as change the dragging constant and dragging list.
                        for gb in goal.spritedict.keys():
                            if gb.rect.collidepoint(event.pos):
                                if event.button == 1:
                                    #gb.image.fill((250, 150, 0))
                                    dragging_obs.append(gb)
                                    dragging = True
                                    goal_in_motion = True
                                # if right mouse click, resize obstacle
                                # if event.button == 3:
                                #     gb.image.fill((250, 80, 0))
                                #     resizing_obs.append(gb)
                                #     resizing = True
                                #     og_pos = gb.rect.topleft
                                #     og_size = gb.rect.size

                        for ob in obstacles.spritedict.keys():
                            if ob.rect.collidepoint(event.pos):
                                # if left mouse click, then we want to drag
                                if event.button == 1:
                                    ob.image.fill((250, 150, 0))
                                    dragging_obs.append(ob)
                                    dragging = True
                                # if right mouse click, resize obstacle
                                if event.button == 3:
                                    ob.image.fill((250, 80, 0))
                                    resizing_obs.append(ob)
                                    resizing = True
                                    og_pos = ob.rect.topleft
                                    og_size = ob.rect.size


        screen.fill(white)
        # Initialize goal and text overlay
        # pygame.draw.rect(screen, (0, 250, 0), (goalx, goaly, 20, 20))


        text_surface1 = font.render('Gen: ' + str(gen), True, black)
        text_surface2 = font.render('Best Step Count: ' + str(best_step_count), True, black)
        screen.blit(text_surface1, (500, 5))
        screen.blit(text_surface2, (500, 15))

        # check if any dot has collided with an obstacle and if so, kill it
        for dead_dots in pygame.sprite.groupcollide(obstacles,dots,
                                                    dokilla=False,
                                                    dokillb=False).values():
            for dot in dead_dots:
                dot.kill()

        if paused:
            goal.draw(screen)
            obstacles.draw(screen)

            dots.draw(screen)

            pygame.display.update()
            clock.tick(fps)
            obstacles.update()
            goal.update()
        else:
            goal.draw(screen)
            dots.draw(screen)
            obstacles.draw(screen)

            pygame.display.update()
            clock.tick(fps)
            goal.update()
            dots.update(count, gen, goal)
            obstacles.update()
            count += 1

            # if count exceeds the best dot's count, kill all dots still remaining
            if dots.goal_count != 0:
                for dot in dots:
                    if dot.alive:
                        dot.image.fill((250, 0, 0))
                        dot.alive = False

        #Here is where the genetic algo will run and determine the next gen
            if dots.genocide():
                dots.calc_fitness(goal)
                if dots.goal_count != 0:
                    # # best_dot = nlargest(1, dots.dots_fitness.keys(), key=lambda i: dots.dots_fitness[i])[0]
                    # nbest_step_count = len(best_dot.memory)
                    # print(nbest_step_count)
                    best_step_count = count

                dots = dots.genetic_algorithm()
                count = 0
                gen += 1






if __name__ == '__main__':

    # Obtain user inputted settings before window occurs
    pop_size = int(input("Population Size: "))
    obs_size = int(input("Obstacle(s)?: "))
    fps = int(input("FPS: "))

    # Initialize pygame window and configurations
    pygame.init()
    pygame.font.init()
    font = pygame.font.Font('freesansbold.ttf', 10)
    screen = pygame.display.set_mode(size)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(white)

    # Initialize Goal
    goal = Obstactles.GoalPop(1, screen)

    # Initialize dots
    first_sample = Populations.Population(pop_size, screen)

    # Initialize any obstacles
    obs = Obstactles.ObstactlePop(obs_size, screen)

    #   Blit everything to the screen

    pygame.display.update()

    # Initialise clock
    clock = pygame.time.Clock()

    main(first_sample, obs, screen, goal)
