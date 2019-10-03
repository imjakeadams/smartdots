import pygame
import Dot
from heapq import nlargest
import random
import Obstactles


class Population(pygame.sprite.Group):

    def __init__(self, pop: int, screen: pygame.Surface):
        pygame.sprite.Group.__init__(self)
        self.screen = screen
        self.dots_fitness = {}
        self.goal_count = 0
        self.fastest_dot = 0
        self.obstactles = {}


        for _ in range(pop):
            dot = Dot.Dot(screen)
            self.add(dot)
            self.dots_fitness[dot] = 0

    def update(self, count: int, gen: int):
        for dot in self.spritedict:
            if dot.reachedgoal or not dot.alive:
                continue
            else:
                dot.update(count, gen)
            if dot.reachedgoal:
                if self.goal_count == 0:
                    self.fastest_dot = dot
                self.goal_count += 1

            #check if dot touches an obstactle
            # for obs in Obstactles.Obstactle

    def calc_fitness(self):

        for dot in self.spritedict:
            self.dots_fitness[dot] = dot.fitness()

    def genocide(self):
        # if all the dots are dead, then the next wave can start
        for dot in self.spritedict:
            if dot.alive:
                return False
        return True

    def select_parent(self):
        fitness_sum = sum(list(self.dots_fitness.values()))
        rand_select = random.uniform(0, fitness_sum)
        running_sum = 0
        for dot in self.dots_fitness.keys():
            running_sum += self.dots_fitness[dot]
            if running_sum > rand_select:
                return dot

    def genetic_algorithm(self):
        next_gen = Population(0, self.screen)

        total_pop = len(self.spritedict) - 1

        # allow the best dot from each gen to live on
        best_dot = nlargest(1, self.dots_fitness.keys(),
                            key=lambda i: self.dots_fitness[i])[0]
        best_clone = Dot.Dot(self.screen)
        best_clone.memory = best_dot.memory
        best_clone.image.fill((250, 250, 0))
        next_gen.add(best_clone)

        while total_pop != 0:
            parent1 = self.select_parent()
            baby = Dot.Dot(self.screen)

            # create babies from the best dots and mutate babies at random
            mutation_rate = 0.05
            for move in parent1.memory:

                mutation_mod = random.uniform(0, 1)

                # mutate the baby by giving it a random move
                if mutation_mod < mutation_rate:
                    dir = random.randint(0, 3)
                    if dir == 0:
                        baby.memory.append((2, 0))
                    elif dir == 1:
                        baby.memory.append((-2, 0))
                    elif dir == 2:
                        baby.memory.append((0, 2))
                    else:
                        baby.memory.append((0, -2))
                else:
                    baby.memory.append(move)

            next_gen.add(baby)
            # next_gen.dots_fitness[baby] = baby.fitness()
            total_pop -= 1

        return next_gen

