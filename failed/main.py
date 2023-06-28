import simpy
import random as rd


class indv :
    def __init__(self, env, name, selfish, friendly, revengeful,food) :
        self.env = env
        self.name = name
        self.selfish = selfish
        self.friendly = friendly
        self.food = food
        # self.revengeful = revengeful
        # self.action = env.process(self.life_cycle())
        self.action = env.process(self.eat_food())
    def eat_food(self) :
        with self.food.request() as req :
            yield req
            print(f'{self.name} eat food')
            yield env.timeout(1)
        
        
    def life_cycle() :
        ...
        
    
def simulate(env,im) :
    # foods = [simpy.Resource(env,capacity=2) for _ in range(10)]
    # organisms_selfish =[indv(env,i,1,0,0) for i in range(5)]
    # organisms_friendly = [indv(env,i,0,1,0) for i in range(5)]
    # im = indv(env,0,1,0,0)
    # a = simpy.Resource(env,capacity=2)
    # for i in range(5) :
        # env.process(organisms_selfish[i].life_cycle())
        # env.process(organisms_friendly[i].life_cycle())

    # while 1 :        
        # yield env.timeout(1)
        # for indv_selfish in organisms_selfish :
            # foodNum = rd.randint(0,9)
            # indv_selfish.eat_food(foods[foodNum])
    yield env.timeout(3)
    im.action() 
            
            
            
        # for indv_freindly in organisms_friendly :
        #     foodNum = rd.randint(0,9)
        #     indv_freindly.eat_food(foods[foodNum])
           
        

env = simpy.Environment()
a = simpy.Resource(env,capacity=2)
im = indv(env,0,1,0,0,a)
env.process(simulate(env,im))
env.run(until=10)
