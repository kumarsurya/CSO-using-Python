import random
import matplotlib.pyplot as plt
import math

class particle:
    def __init__(self,dim=3,posit=[0,0,0],veloc=[0,0,0]):
        self.dimension = dim
        if posit == None or veloc == None:
            self.position=[0 for i in range(dim)]
            self.velocity=[0 for i in range(dim)]
        else:
            self.position=posit
            self.velocity=veloc

    def display(self):
        print("position:",self.position)
        print("velocity:",self.velocity)

    def fitness(self):
        # sum=0          #.......... Griewank function
        # prod=1
        # for i in range(self.dimension):
        #     sum+=(self.position[i]**2)/4000
        #     prod*=math.cos(self.position[i]/math.sqrt(i+1))
        # return sum-prod+1

        sum=0     # ............for Rastrigin function 
        for i in range(self.dimension):
            sum+=self.position[i]**2-10*math.cos(2*math.pi*self.position[i])
        return 10*self.dimension+sum
        #return sum([x**2 for x in self.position]) # ............for sphere function

    def update(self,winner,x_mean):

        phi=0.3
        R1=[random.uniform(0,1) for i in range(self.dimension)]
        R2=[random.uniform(0,1) for i in range(self.dimension)]
        R3=[random.uniform(0,1) for i in range(self.dimension)]
        phi_x_R3=[phi*y for y in R3]

        s1=vector_sum(dot_product(R1,self.velocity),dot_product(R2,vector_difference(winner.position,self.position)))
        s2=vector_sum(s1,dot_product(phi_x_R3,vector_difference(x_mean,self.position)))
        self.velocity=s2
        s3=vector_sum(s2,self.position)
        self.position=s3


def vector_sum(V1,V2):
    return [x+y for x,y in zip(V1,V2)]

def dot_product(V1,V2):
    return [x*y for x,y in zip(V1,V2)]

def vector_difference(V1,V2):
    return [x-y for x,y in zip(V1,V2)]

def vector_division(vec,s):
    return [x/s for x in vec]

def find_mean_position(swarm):
    x_mean=[]

    s1=swarm[0].position
    i=1
    for  i in range(len(swarm)):
        s1=vector_sum(s1,swarm[i].position)
    x_mean=vector_division(s1,len(swarm))
    # print(x_mean)
    return x_mean

def populate_initial_swarm(swarm_size,dim):
    # initialize initial swarm particle features
    swarm=[]
    lower_limit=-5.12
    upper_limit=5.12

    for i in range(swarm_size):
        vel=[0 for  i in range(dim)]
        pos=[random.uniform(lower_limit,upper_limit) for i in range(dim)]

        p=particle(dim,pos,vel)
        swarm.append(p)

        # p.display()

    return swarm


def print_swarm(swarm):
    for p in swarm:
        p.display()

def find_best_particle(swarm):
    cur_minimum=1000000
    for par in swarm:

        cur_minimum=min(par.fitness(),cur_minimum)
    return cur_minimum

if __name__ == "__main__":
    # rest code goes here
    dimensions=5
    max_iteration=100
    init_swarm_size=50
    t=0
    p=[[] for i in range(max_iteration)]
    # print(len(p))
    p[0]=populate_initial_swarm(init_swarm_size,dimensions)

    generation=[i for i in range(max_iteration)]
    best_fitness=[]
    while t<max_iteration-1:

        min_fit=find_best_particle(p[t])
        best_fitness.append(min_fit)

        swarm_size = len(p[t])
        u=p[t]
        print("generation no.",t,"size:",swarm_size)
        while swarm_size>0:
            first_index=random.randrange(0,swarm_size)
            second_index=random.randrange(0,swarm_size)

            while second_index==first_index:
                second_index=random.randrange(0,swarm_size)
            print("first",first_index,"second",second_index)
            first_particle=u[first_index]
            second_particle=u[second_index]

            first_particle.display()
            second_particle.display()

            if first_particle.fitness() < second_particle.fitness():
                winner_index=first_index
                loser_index=second_index
            else:
                winner_index=second_index
                loser_index=first_index
            print("the winner is ")
            u[winner_index].display()
            print(t+1,"is the new gen*************************")
            p[t+1].append(u[winner_index])

            x_mean=find_mean_position(u)


            u[loser_index].update(u[winner_index],x_mean)
            u[loser_index].display()
            print("above is the loser")
            p[t+1].append(u[loser_index])
            # print(len(p[t+1]),"is the next gen*********************")
            # print_swarm(p[t+1])
            print(winner_index,loser_index,"****")
            if loser_index>winner_index:
                u.pop(winner_index)
                u.pop(loser_index-1)
            else:
                u.pop(loser_index)
                u.pop(winner_index-1)

            swarm_size=swarm_size-2

        t=t+1
    min_fit=find_best_particle(p[max_iteration-1])
    best_fitness.append(min_fit)
    print(generation,best_fitness)
    plt.plot(generation,best_fitness)
    plt.show()