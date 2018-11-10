# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 21:40:56 2018

@author: Cliente
TESTE FITNESS SLOPE COMPLETE
"""


import numpy
from math import cos,sin,pi,tan,sqrt,acos

def cal_pop_fitness(pop):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function caulcuates the sum of products between each input and its corresponding weight.
    fitness = []
    for n in range(len(pop)):
        
        h = [] # average slice hight
        p=[] # peso da fatia
        lb = [] #largura da base
        dx = [] # largura da faixa
        gama = []
        u = [] #poropressao
        theta= []
        xm = [] # ponto medio da lamela
        xfat = []
        yfat = []
        coesao = 198 #INPUT
        phi = 44.48 #INPUT
        phig = (phi*pi)/180
        x0 = 3 # INPUT
        x1 = 6.3 # INPUT
        y0 = 5.0 # INPUT
        y1 = 1.67 # INPUT
        ampr = float(pop[n,0]) # gene amplificador do raio 0.5<ampr<2.0
        r = ampr*sqrt(abs(x1-x0)**2+abs(y1-y0)**2)  #DEFAULT
        a = x1 # coordenada horizontal do centro do raio de corte #DEFAULT (GENERALIZAR)
        b = y1+r  # coordenada vertical do centro do raio de corte # GENE INDIRETO
        fx1 = a-sqrt(r**2-(y0-b)**2)
        n_slc = int(pop[n,1]) # total de fatias # GENE   2<n_slc<30
        dx0 = abs(x1-fx1)/n_slc #largura da fatia
        gama0 = 21 # (kN/m3) peso especifico do solo # INPUT
        u0 = 0 # INPUT (VARY)
        cangular = (y1-y0)/(x1-x0)
        clinear = y0-x0*cangular
        # (x-a)**2 + (y-b)**2 = r**2
        
        xmedio = 0
        xmedio = fx1+dx0/2
        for i in range(n_slc):
            dx.append(dx0)
            gama.append(gama0)
            u.append(u0)
            h.append(0)
            lb.append(0)
            p.append(0)
            theta.append(0)
            xm.append(xmedio+i*dx0) # teste xm[7]+dx0/2 = x1
        for i in range(n_slc+1):    
            xfat.append(fx1+i*dx0) #teste xfat[7]+dx0 = x1
            yfat.append(b-sqrt(r**2-(xfat[i]-a)**2))
        #print(xm)    
        for i in range(n_slc):
            if xm[i] <= x0: hsolo = y0 # superior parte plana
            else: hsolo = cangular*xm[i]+clinear # talude
            h[i] = hsolo-(b-sqrt(r**2-(xm[i]-a)**2)) # h - coordenada em y do ponto medio da na circunferencia
            dxfat = xfat[i+1]-xfat[i]
            dyfat = yfat[i+1]-yfat[i]
            lb[i] = sqrt(dxfat**2 + dyfat**2 )
            p[i] = h[i]*dx0*gama0 
            theta[i] = pi/2-(acos(abs(x1-xm[i])/r))    #rad
        '''
        print('theta',theta)    
        print('h',h)
        print('lb',lb)    
        print('p',p)
        
        p[0] = 3.577875
        p[1] = 3.70125 #erro aqui no tcc
        p[2] = 15.2985
        p[3] = 19.61663
        p[4] = 22.94775
        p[5] = 24.79838
        p[6] = 18.50625
        p[7] = 7.772625
       '''
              
        sum1 = 0
        sum2 = 0
            
        for i in range(n_slc):
            sum1 = sum1 + coesao*lb[i]+(p[i]*cos(theta[i])-u[i]*dx[i]*cos(theta[i]))*tan(phig)
            sum2 = sum2 + p[i]*sin(theta[i])
        fitness.append(sum1/sum2)
    return fitness

num_weights = 2
sol_per_pop = 100
num_parents_mating = 4

# Defining the population size.
#sol_per_po = total de individuos por populacao
# num_weights = genes por individuo
pop_size = (sol_per_pop,num_weights) # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
new_population = []
for i in range(sol_per_pop):
    lista = []
    ampr = numpy.random.uniform(0.7,2.0)
    n_slc = int(numpy.random.uniform(2,30))
    lista.append(ampr)
    lista.append(n_slc)
    new_population.append(lista)
    
new_population = numpy.asarray(new_population)

#Creating the initial population.

#print('random pop',new_population)

fitness = cal_pop_fitness(new_population)
#print('fitness', fitness)
best_match_idx = numpy.where(fitness == numpy.max(fitness))
print("best index",best_match_idx)
print("Best solution : ", new_population[best_match_idx, :])

fitness = numpy.asarray(fitness)
print("Best result : ", fitness[best_match_idx])