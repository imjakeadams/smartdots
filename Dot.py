import pygame
import random
import Obstactles

black = (0, 0, 0)


class Dot(pygame.sprite.DirtySprite):

    def __init__(self, screen):
        pygame.sprite.DirtySprite.__init__(self)
        self.acc = 1
        self.image = pygame.Surface([5, 5])
        self.image.fill(black)
        # self.pos = pygame.math.Vector2((325,525))
        self.rect = pygame.rect.Rect((325, 550), self.image.get_rect().size)
        self.memory = []
        self.screen = screen
        self.alive = True
        self.reachedgoal = False
        self.fit = 0

    def fitness(self):
        if not self.reachedgoal:

            distancetogoal = (self.rect.centerx - 325)**2 + \
                             (self.rect.centery - 100)**2
            fitness = 1.0 / (distancetogoal) ** 2

        else:
            # if this dot has reached the goal, then it should have a higher
            # fitness value
            fitness = (1.0 / 16.0) + (10000.0 / (len(self.memory) ** 2))
        self.fit = fitness
        return self.fit

    # def interval_fitness(self):
    #
    #     distancetogoal = (self.rect.centerx - 325) ** 2 + \
    #                      (self.rect.centery - 100) ** 2
    #     fitness = 1.0 / (distancetogoal)
    #
    #     return fitness

    def kill(self):
        self.image.fill((250, 0, 0))
        self.alive = False

    def update(self, count: int, gen: int):
        self.dirty = True
        canvas_rect = pygame.Rect((0, 0), (650, 650))
        screen_rect = pygame.Rect((1, 1), (648, 648))

        dir = random.randint(0, 3)

        # if the dot has reached the goal, it must be killed
        if not self.reachedgoal and self.alive:

            if count < len(self.memory) and gen != 0:
                self.rect.move_ip(
                    tuple([self.acc * i for i in self.memory[count]]))
                self.rect.clamp_ip(canvas_rect)
            else:

                if dir == 0:
                    self.rect.move_ip(self.acc * 2, 0)
                    self.rect.clamp_ip(canvas_rect)
                    self.memory.append((2, 0))
                elif dir == 1:
                    self.rect.move_ip(self.acc * -2, 0)
                    self.rect.clamp_ip(canvas_rect)
                    self.memory.append((-2, 0))
                elif dir == 2:
                    self.rect.move_ip(0, self.acc * 2)
                    self.rect.clamp_ip(canvas_rect)
                    self.memory.append((0, 2))
                else:
                    self.rect.move_ip(0, self.acc * -2)
                    self.rect.clamp_ip(canvas_rect)
                    self.memory.append((0, -2))

            if self.acc < 10:
                self.acc += 0.1

            # if a dot touches the window border, it dies
            if not screen_rect.contains(self):
                self.kill()

            # if dot touches obstacle, it dies



            # check if dot has reached the goal
            goal_rect = pygame.Rect((325, 100), (20, 20))
            if self.rect.colliderect(goal_rect):
                self.image.fill((0, 250, 250))
                self.reachedgoal = True
                self.alive = False
            # else:
            #     # calculate the fitness of this move selection
            #     self.fit += self.interval_fitness()
