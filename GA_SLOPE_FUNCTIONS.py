
#The GA module is as follows:

import numpy
from math import cos,sin,pi,tan

def cal_pop_fitness(pop):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function caulcuates the sum of products between each input and its corresponding weight.
    fitness = []
    h = [] # average slice hight
    p=[] # peso da fatia
    lb = [] #largura da base
    dx = [] # largura da faixa
    gama = []
    u = [] #poropressao
    theta= []
    n_slc = 8 # total de fatias
    dx0 = 0.5875
    gama0 = 21 # peso especifico do solo
    u0 = 0
    for i in range(n_slc):
        dx.append(dx0)
        gama.append(gama0)
        u.append(u0)
        h.append(0)
        lb.append(0)
        p.append(0)
        theta.append(0)
    h[0] = 0.29
    h[1] = 0.3
    h[2] = 1.24
    h[3] = 1.59
    h[4] = 1.86
    h[5] = 2.01
    h[6] = 1.5
    h[7] = 0.63

    lb[0] = 0.59
    lb[1] = 0.6
    lb[2] = 0.61
    lb[3] = 0.64
    lb[4] = 0.69
    lb[5] = 0.77
    lb[6] = 0.91
    lb[7] = 1.27
    
    p[0] = 3.577875
    p[1] = 3.70125
    p[2] = 15.2985
    p[3] = 19.61663
    p[4] = 22.94775
    p[5] = 24.79838
    p[6] = 18.50625
    p[7] = 7.772625
      
    theta[0] = 4
    theta[1] = 11
    theta[2] = 17
    theta[3] = 25
    theta[4] = 32
    theta[5] = 40
    theta[6] = 50
    theta[7] = 62
    
    sum1 = 0
    sum2 = 0
    for n in range(len(pop)):
        #pop[n,0] = angulo de atrito
        #pop[n,1] = coesao
        
       
        for i in range(n_slc):
            thetai = (theta[i]*pi)/180
            phii = (pop[n,0]*pi)/180
            #sum1 = sum1 + pop[n,1]*lb[i]+(p[i]*cos(thetai)-u[i]*dx[i]*cos(thetai))*tan(phii)
            sum1 = sum1 + pop[n,1]*lb[i]+(p[i]*cos(thetai))*tan(phii)
           #sum1 = sum1 + 200*lb[i]+(p[i]*cos(thetai))*tan(phii)
            sum2 = sum2 + p[i]*sin(thetai)
        fitness.append(sum1/sum2)
    return fitness

def select_mating_pool(pop, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = numpy.empty((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
        #print('idx', max_fitness_idx)
        #print(parent_num)
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999999
    return parents

def crossover(parents, offspring_size):
    offspring = numpy.empty(offspring_size)
    # The point at which crossover takes place between two parents. Usually it is at the center.
    crossover_point = numpy.uint8(offspring_size[1]/2)

    for k in range(offspring_size[0]):
        # Index of the first parent to mate.
        parent1_idx = k%parents.shape[0]
        # Index of the second parent to mate.
        parent2_idx = (k+1)%parents.shape[0]
        # The new offspring will have its first half of its genes taken from the first parent.
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        # The new offspring will have its second half of its genes taken from the second parent.
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring

def mutation(offspring_crossover):
    # Mutation changes a single gene in each offspring randomly.
    for idx in range(offspring_crossover.shape[0]):
        # The random value to be added to the gene.
        random_value = numpy.random.uniform(-5.0, 5.0, 1)
        offspring_crossover[idx, 1] = offspring_crossover[idx, 1] + random_value # verificar esse 1 devido ao numero de genes
    return offspring_crossover