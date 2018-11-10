# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 17:45:29 2018

@author: Cliente
"""

import numpy
import GA_SLOPE_FUNCTIONS as GA
from matplotlib import pyplot as plt
"""
The y=target is to maximize this equation ASAP:
    y = w1x1+w2x2+w3x3+w4x4+w5x5+6wx6
    where (x1,x2,x3,x4,x5,x6)=(4,-2,3.5,5,-11,-4.7)
    
    What are the best values for the 6 weights w1 to w6?
    We are going to use the genetic algorithm for the best possible values after a number of generations.
"""

# Inputs of the equation. write a dictionary here
#equation_inputs = [4,-2,3.5,5,-11,-4.7]

# Number of the weights we are looking to optimize.

def savefit(generation,fitness):
    plt.clf()
    plt.xlabel("Geração")
    plt.ylabel("Fator de Segurança")
    plt.title("Função Fitness")
    #    plt.ylim(-1,1)
    plt.plot(generation,fitness)# mandar listas para definir os eixos
    # define axis limits
    plt.savefig('fitness')

def saveangle(generation,ang):
    plt.clf()
    plt.xlabel("Geração")
    plt.ylabel("Angulo de Atrito")
    plt.title("Evolução do Angulo de Atrito")
    #    plt.ylim(-1,1)
    plt.plot(generation,ang)# mandar listas para definir os eixos
    # define axis limits
    plt.savefig('Angulo')

def savecoesao(generation,coesao):
    plt.clf()
    plt.xlabel("Geração")
    plt.ylabel("Coesão do Solo")
    plt.title("Evolução da Coesão do Solo")
    #    plt.ylim(-1,1)
    plt.plot(generation,coesao)# mandar listas para definir os eixos
    # define axis limits
    plt.savefig('coesao')
    
num_weights = 2

"""
Genetic algorithm parameters:
    Mating pool size
    Population size
"""

sol_per_pop = 1000
num_parents_mating = 200

# Defining the population size.
#sol_per_po = total de individuos por populacao
# num_weights = genes por individuo
pop_size = (sol_per_pop,num_weights) # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.

#Creating the initial population.
#new_population = numpy.random.uniform(low=0.0, high=50.0, size=pop_size)


new_population = []

for i in range(sol_per_pop):
    lista = []
    angulo = numpy.random.uniform(0,45)
    coes = numpy.random.uniform(0,250)
    lista.append(angulo)
    lista.append(coes)
    new_population.append(lista)
    
new_population = numpy.asarray(new_population)
print(new_population)

num_generations = 230
gen = []
fit = []
ang = []
coesao = []
for generation in range(num_generations):
    print("Generation : ", generation)

    # Measing the fitness of each chromosome in the population.
    #fitness = GA.cal_pop_fitness(equation_inputs, new_population)
    for i in range(sol_per_pop):
        if float(new_population[i,1])>250: new_population[i,1] = 250
        
    fitness = GA.cal_pop_fitness(new_population)
    #print('fitness', fitness)
    # Selecting the best parents in the population for mating.
    parents = GA.select_mating_pool(new_population, fitness,num_parents_mating)
   # print('parents',parents)
    # Generating next generation using crossover.
    offspring_crossover = GA.crossover(parents,
                                       offspring_size=(pop_size[0]-parents.shape[0], num_weights))
   # print('cross', offspring_crossover)
    # Adding some variations to the offsrping using mutation.
    offspring_mutation = GA.mutation(offspring_crossover)
   # print('mutation', offspring_mutation)
    # Creating the new population based on the parents and offspring.
    new_population[0:parents.shape[0], :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation
    print('new population', new_population)
    # The best result in the current iteration.
    print("Best result : ", numpy.max(fitness))
    fit.append(numpy.max(fitness))
    gen.append(generation)
    best_match_idx = numpy.where(fitness == numpy.max(fitness))
    ang.append(float(new_population[best_match_idx, 0]))
    coesao.append(float(new_population[best_match_idx, 1])) 
# Getting the best solution after iterating finishing all generations.
#At first, the fitness is calculated for each solution in the final generation.
fitness = GA.cal_pop_fitness(new_population)

# Then return the index of that solution corresponding to the best fitness.
best_match_idx = numpy.where(fitness == numpy.max(fitness))
#print("best index",best_match_idx)
print("Best solution : ", new_population[best_match_idx, :])
#print("Best solution fitness : ", fitness[best_match_idx])
savefit(gen,fit)
saveangle(gen,ang)
savecoesao(gen,coesao)