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

def Fitness3_Get(synapses):
    weightsFileName = "weights.dat" 
    fitFileName = "fits.dat"
    #Send_First(first)
    Send_Synapse_Weights_ToFile(synapses,weightsFileName)
    os.system('"/Users/kevingottfried/Documents/CS 206/HW/Project_Bullet/bullet3-2.82/Demos/RagdollDemo/AppRagdollDemo"')    
    save_path = path
    completeName = os.path.join(save_path, fitFileName)
    while not os.path.exists(completeName):
        time.sleep(.5);     
    fitness = Fitness_Collect_From_File(fitFileName)
    Delete_File(weightsFileName)

    Delete_File(fitFileName)
    return fitness
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
 
def GetDigit():
    save_path = "/Users/kevingottfried/Documents/CS_228/Final/final/"
    completeName = os.path.join(save_path, "digC.dat")
    print(completeName)
    f = open(completeName, "r")
    digit = f.readline()
    f.close
    return int(digit)
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
        print("%.1f %.1f %.1f %.1f" %(parentFitnessTime, childFitnessTime, parentFitnessNum, childFitnessNum))
        #print("elapsed time of run: %f" %elapsed)
        if (childFitnessTime < parentFitnessTime):
            parent = child 
            parentFitnessTime = childFitnessTime
            parentFitnessNum = childFitnessNum
        elif(parentFitnessNum == 10):
            parent = child 
            parentFitnessTime = childFitnessTime
            parentFitnessNum = childFitnessNum
        parent1Fit[currentGeneration] = parentFitnessNum
        #parent2Fit[currentGeneration] = parentFitnessTime
    
    return parent
    
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
#p = subprocess.Popen(["python","/Users/kevingottfried/Documents/CS_228/Deliverables/Deliverable\ 6/asl.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
#stdin,stderr = p.communicate()
#p.wait()
#print(stdin)
#digitNum = sys.stdin.readline()
#print(digitNum)
digitNum = 10
#
#print("hi")
     
def RunANN():
    digitNum = GetDigit()
    parentString = "best_" + str(digitNum) +".dat"
    parent1 = MatrixCreate(numSensors,numMotors)
    parent1 = BestMatrix(parent1, parentString)
    parent1 = Fitness3_Get(parent1)
#parent1File = os.path.join(path, "parent_1.dat")
#Save_Best(parent1, 1)


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
#plt.plot(parent1Fit)
#plt.show()
#plt.plot(parent2Fit)
#plt.show()
