# -*- coding: utf-8 -*-
import numpy as np 
import random
import copy
from matplotlib import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time; 
import sys
import os;
import os.path
path = '/Users/kevingottfried/Documents/CS 206/HW/Project_Bullet/bullet3-2.82/Demos/RagdollDemo/'
first = None
def MatrixCreate(rows, columns):
    a = np.zeros((rows,columns))
    return a

def VectorCreate(width):
    i = width
    v = np.zeros((i), dtype='f')
    return v
    
def MatrixRandomize(v):
    for x in range(len(v)):
        for y in range(len(v[0])):
            v[x,y] = (random.random() * 2) - 1
    return v   
def MatrixPerturb(p, prob):
    c = copy.deepcopy(p)
    for x in range(len(p)):
        for y in range(len(p[0])):
            if prob > random.random():
                c[x,y] = (2 * random.random()) - 1
    return c

#def Fitness3_Get(synapses):
#    weightsFileName = "weights.dat" 
#    fitFileName = "fits.dat"
#    #Send_First(first)
#    Send_Synapse_Weights_ToFile(synapses,weightsFileName)
#    os.system('"/Users/kevingottfried/Documents/CS 206/HW/Project_Bullet/bullet3-2.82/Demos/RagdollDemo/AppRagdollDemo"')
#    
#    save_path = path
#    completeName = os.path.join(save_path, fitFileName)
#    while not os.path.exists(completeName):
#        time.sleep(.5);     
#    fitness = Fitness_Collect_From_File(fitFileName)
#    Delete_File(weightsFileName)
#
#    Delete_File(fitFileName)
#    return fitness 
def Weights_Collect_From_File(filename):
    open_path = path
    completeName = os.path.join(open_path, filename)
    #f = open(completeName, 'r')
    with open(completeName) as f:
            synapses = map(float, f)
    i = 0
    for row in range(0,4):
        for weight in range(0,8):
            
            temp[row, weight] = synapses[i]
            i+= 1
            
    f.close()
    return temp
        
def Send_Synapse_Weights_ToFile(synapses, filename):
    save_path = path
    completeName = os.path.join(save_path, filename)
    f = open(completeName, 'w')
    for rows in synapses:
        for synapse in rows:
            f.write("%s\n" % synapse)
            #print(synapse)
    f.close()
    
def Fitness_Collect_From_File(filename):
    open_path = path
    fits = []
    completeName = os.path.join(open_path, filename)
    myfile = open(completeName, "r")
    for f in myfile:
        fits.append(float(f))
    return fits
    
def Delete_File(filename):
    delete_path = path
    completeName = os.path.join(delete_path, filename)
    os.remove(completeName)
    
def Save_Best(synapses, num):
    save_path = path
    bestWFN = "parent_{}.dat".format(num)
    completeName = os.path.join(save_path, bestWFN)
    f = open(completeName, 'w')
    for rows in synapses:
        for synapse in rows:
            f.write("%s\n" % synapse)
            #print(synapse)
    f.close()
def Evolve(parent):
    parentFitness = Fitness3_Get(parent)
    parentFitnessNum = parentFitness[0]
    print(parentFitnessNum)
    parentFitnessTime = parentFitness[1]
    print(parentFitnessTime)
    for currentGeneration in range(0,numGenerations):
        child = MatrixPerturb(parent, .15)
        time_start = time.time()
        childFitness = Fitness3_Get(child) 
        childFitnessNum = float(childFitness[0])
        childFitnessTime = float(childFitness[1])
        
        time_end   = time.time()
        elapsed    = time_end - time_start 
        if( elapsed > 0.01 ) :
            ratepermin = 60.0 / elapsed
        else :
            ratepermin = 5455.0
        #allrates.append(ratepermin)
        print("%d %.1f %.1f" %(currentGeneration, parentFitnessNum, childFitnessNum))
        print("elapsed time of run: %f" %elapsed)
        if (childFitnessNum > parentFitnessNum):
            parent = child 
            parentFitnessTime = childFitnessTime
            parentFitnessNum = childFitnessNum
        parent1Fit[currentGeneration] = parentFitnessNum
        #parent2Fit[currentGeneration] = parentFitnessTime
    
    return parent
def Genetic_Recombination(parent1, parent2):
    temp = copy.deepcopy(parent1) 
    prob = 0.5
    for x in range(len(parent1)):
        for y in range(len(parent1[0])):
            if  prob > random.random():
                temp[x,y] = parent2[x,y]
    return temp
    
def BestMatrix(v, fileName):
    open_path = path
    completeName = os.path.join(open_path, fileName)
    file = open(completeName, "r")
    with open(completeName) as f:
        synapses = map(float, f) #turns the file into an array of floats
    i = 0
    for row in range(0,4):
        for weight in range(0,8):
            
            v[row, weight] = synapses[i]
            i+= 1
    file.close()
    return v   
allrates = []
numSensors = 4; 
numMotors = 8; 
numGenerations = 1000;
parent1Fit = VectorCreate(numGenerations)
parent2Fit = VectorCreate(numGenerations)
parent1 = MatrixCreate(numSensors,numMotors)
parent2 = MatrixCreate(numSensors, numMotors)
parent1 = BestMatrix(parent1, "parent_2.dat")
#parent2 = BestMatrix(parent2, "parent_3.dat")
worse = MatrixCreate(numSensors,numMotors)
#parent1 = MatrixRandomize(parent1)
worse = MatrixRandomize(worse)
Save_Best(worse,4)
#parent2 = MatrixRandomize(parent2)
#parent1 = MatrixPerturb(parent1,2)
#parent2 = MatrixPerturb(parent2,2)
parent1File = os.path.join(path, "parent_1.dat")
#parent2File = os.path.join(path, "parent_2.dat") 
#for currentPar in range(0,1):
parent1 = Evolve(parent1)
Save_Best(parent1, 1)
#parent2 = Evolve(parent2)
#Save_Best(parent2, 2)
#child = Genetic_Recombination(parent1, parent2)
#child = Evolve(child)
#Save_Best(child, 3)


#tcol = 'g'
#ls = '-'
#linestyles = ['-', '--', ':','--',':']
#styles = [r'$\lambda$',r'$\bowtie$',r'$\circlearrowleft$',r'$\clubsuit$',
#r'$\checkmark$']
#colors = ('b','g','r','c','m','y','k')
#t = np.arange(0,  numGenerations,  1 )
#
#plt.figure(figsize=(8,8))
#ax = plt.subplot(1,1, 1)
#plt.xlabel("Generation")
#plt.ylabel("fitness")
#plt.plot(t,parent1Fit, ls, color=tcol, markersize=5)
# 
##ax.set_yticklabels([])
##ax.set_xticklabels([])
# 
#plt.show()      
plt.plot(parent1Fit)
plt.show()
plt.plot(parent2Fit)
plt.show()
