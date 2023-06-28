import random
import simpy

class Organism:
    def __init__(self, env, name, is_selfish, is_altruistic, is_vengeful):
        self.env = env
        self.name = name
        self.is_selfish = is_selfish
        self.is_altruistic = is_altruistic
        self.is_vengeful = is_vengeful
        self.prey_eaten = 0
        self.reproduced = False

    def compete_for_food(self, prey):
        if len(prey) == 2:
            if self.is_selfish:
                self.env.process(self.selfish_competition(prey))
            else:
                self.env.process(self.other_competition(prey))
        elif len(prey) == 1:
            self.eat_prey(prey[0])

    def eat_prey(self, prey):
        self.prey_eaten += 1
        prey.remove(prey[0])

        if self.prey_eaten == 2 and not self.reproduced:
            self.reproduced = True
            self.env.process(self.reproduction())

    def selfish_competition(self, prey):
        yield self.env.timeout(1)  # Wait for both organisms to arrive

        if random.random() < 0.5:
            self.eat_prey(prey[0])
        else:
            self.eat_prey(prey[1])

    def other_competition(self, prey):
        self.eat_prey(prey[0])
        self.eat_prey(prey[1])

    def reproduction(self):
        yield self.env.timeout(1)  # Wait for reproduction

        if random.random() < 0.5:
            new_name = f'{self.name}_child'
            new_organism = Organism(self.env, new_name, self.is_selfish, self.is_altruistic, self.is_vengeful)
            self.env.process(new_organism.life_cycle())

    def life_cycle(self):
        while True:
            yield self.env.timeout(1)  # Wait for a day

            if self.prey_eaten >= 2:
                self.prey_eaten -= 2
            elif self.prey_eaten == 1:
                self.prey_eaten -= 1
                if random.random() < 0.5:
                    self.reproduced = False
            else:
                self.env.exit()  # Organism dies

def simulate():
    # env = simpy.Environment()

    initial_prey_count = random.randint(1, 5)  # Randomly choose initial prey count
    prey = simpy.Container(env, capacity=initial_prey_count, init=initial_prey_count)
    organisms = []

    # Create two organisms (can be adjusted as per your requirements)
    organism1 = Organism(env, 'Organism 1', is_selfish=True, is_altruistic=False, is_vengeful=False)
    organism2 = Organism(env, 'Organism 2', is_selfish=True, is_altruistic=False, is_vengeful=False)

    organisms.append(organism1)
    organisms.append(organism2)

    for organism in organisms:
        env.process(organism.life_cycle())

    while True:
        yield env.timeout(1)  # Wait for a day

        if prey.level == 0:
            break

        # Randomly choose an organism to compete for prey
        organism = random.choice(organisms)
        organism.compete_for_food(prey.items)

    # Print the results
    for organism in organisms:
        print(f'{organism.name}: Prey Eaten={organism.prey_eaten}, Reproduced={organism.reproduced}')

# Run the simulation
env = simpy.Environment()
env.process(simulate())
env.run()
