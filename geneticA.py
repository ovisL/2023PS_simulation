import random
import numpy as np
import pygame
import time

FPS = 100
SCREEN_SIZE = 10
PIXEL_SIZE = 20
LINE_WIDTH = 1

items = [
        [1, 2],
        [2, 4],
        [3, 4],
        [4, 5],
        [5, 7],
        [6, 9]
]
# items = [[7, 1000],
#          [1000, 10],
#          [500, 1],
#          [100, 9],
#          [100, 8],
#          [90, 8],
#          [80, 6],
#          [70, 4]]


class geneticA():
    def __init__(self, s):
        self.s = s
        self.max_weight = 10
        self.population_size = 10
        self.mutation_probability = 0.2
        self.generations = 10

    def generate_population(self, size):
        population = []
        for _ in range(size):
            genes = [0, 1]
            chromosome = []
            for _ in range(len(items)):
                chromosome.append(random.choice(genes))
            population.append(chromosome)
        print("Generated a random population of size", size)
        return population

    def calculate_fitness(self, chromosome):
        total_weight = 0
        total_value = 0
        for i in range(len(chromosome)):
            if chromosome[i] == 1:
                total_weight += items[i][0]
                total_value += items[i][1]
        if total_weight > self.max_weight:
            return 0
        else:
            return total_value

    def select_chromosomes(self, population):
        fitness_values = []
        for chromosome in population:
            fitness_values.append(self.calculate_fitness(chromosome))

        # fitness_values = [float(i)/sum(fitness_values) for i in fitness_values]
        new = []
        for i in fitness_values:
            if i == 0:
                new.append(float(i)+0.01)
            else:
                new.append(i)

        fitness_values = new

        parent1 = random.choices(population, weights=fitness_values, k=1)[0]
        parent2 = random.choices(population, weights=fitness_values, k=1)[0]

        print("Selected two chromosomes for crossover")
        return parent1, parent2

    def crossover(self, parent1, parent2, a, b):
        crossover_point = random.randint(0, len(items)-1)
        child1 = parent1[0:crossover_point] + parent2[crossover_point:]
        child2 = parent2[0:crossover_point] + parent1[crossover_point:]

        for i in range(crossover_point):
            self.s.blit(self.par1, (i*PIXEL_SIZE, b*PIXEL_SIZE))

        for i in range(crossover_point):
            self.s.blit(self.par2, (i*PIXEL_SIZE, a*PIXEL_SIZE))

        pygame.display.update()
        time.sleep(3)

        print("Performed crossover between two chromosomes")
        return child1, child2

    def mutate(self, chromosome, x):
        mutation_point = random.randint(0, len(items)-1)
        chromosome[mutation_point] = 1-chromosome[mutation_point]

        print("Performed mutation on a chromosome")
        self.s.blit(self.mut, (mutation_point*PIXEL_SIZE, x*PIXEL_SIZE))

        return chromosome

    def get_best(self, population):
        fitness_values = []
        for chromosome in population:
            fitness_values.append(self.calculate_fitness(chromosome))

        max_value = max(fitness_values)
        max_index = fitness_values.index(max_value)
        return population[max_index]

    def run(self):
        print("Available items:\n", items)

        print("\nGenetic algorithm parameters:")
        print("Max weight:", self.max_weight)
        print("Population:", self.population_size)
        print("Mutation probability:", self.mutation_probability)
        print("Generations:", self.generations, "\n")
        print("Performing genetic evolution:")

        image = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
        image.fill((0, 255, 0))
        self.img1 = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE), 1)
        self.img1.fill((255, 255, 255))
        # clock = pygame.time.Clock()
        self.par1 = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE), 1)
        self.par1.fill((255, 255, 0))

        self.par2 = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE), 1)
        self.par2.fill((0, 255, 255))
        self.mut = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE), 1)
        self.par2.fill((0, 0, 255))

        population = self.generate_population(self.population_size)
        # pos = [[]*6 for i in range(self.population_size)]
        # for i in range(population) :
        # 	for j in population[i] :
        # 		pos.append([i,j])

        # a = np.array(items)
        # record = []
        for i in range(len(population)):
            for j in range(6):
                self.s.blit(self.img1, (j*PIXEL_SIZE, i*PIXEL_SIZE))
                pygame.display.update()

        time.sleep(3)
        for num in range(self.generations):

            print(f"========gen {num+1}============")
            parent1, parent2 = self.select_chromosomes(population)
            a = population.index(parent1)
            b = population.index(parent2)
            for i in range(6):
                self.s.blit(self.par1, (i*PIXEL_SIZE, a*PIXEL_SIZE))

            for i in range(6):
                self.s.blit(self.par2, (i*PIXEL_SIZE, b*PIXEL_SIZE))
                pygame.display.update()
            time.sleep(3)

            child1, child2 = self.crossover(parent1, parent2, a, b)

            if random.uniform(0, 1) < self.mutation_probability:
                child1 = self.mutate(child1, a)
            if random.uniform(0, 1) < self.mutation_probability:
                child2 = self.mutate(child2, b)
            pygame.display.update()
            time.sleep(3)

            population = [child1, child2] + population[2:]
            self.s.fill((0, 0, 0))
            for i in range(len(population)):
                for j in range(6):
                    self.s.blit(self.img1, (j*PIXEL_SIZE, i*PIXEL_SIZE))
                    # pygame.display.update()
            pygame.display.update()
            time.sleep(3)

            # temp = []
            # for i in population:
            # 	temp1 = np.array(i)
            # 	temp2 = a[:, 1]*temp1
            # 	temp_weight = a[:, 0]
            # 	summ = sum(temp2)
            # 	temp.append([temp2, temp_weight, summ])
            # 	print(temp2, summ)
            # record.append(temp)

        # print(record[0])
        best = self.get_best(population)

        total_weight = 0
        total_value = 0
        for i in range(len(best)):
            if best[i] == 1:
                total_weight += items[i][0]
                total_value += items[i][1]

        print("\nThe best solution:")
        print("Weight:", total_weight)
        print("Value:", total_value)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    s = pygame.display.set_mode(
        (SCREEN_SIZE * PIXEL_SIZE, SCREEN_SIZE * PIXEL_SIZE))
    pygame.display.set_caption('Genetic Algorithm')

    geneticA = geneticA(s)
    geneticA.run()
