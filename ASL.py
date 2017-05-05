# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import sys
import os
import subprocess
sys.path.insert(0, "/Users/kevingottfried/Documents/CS_228/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib")
import Leap
import pickle
import numpy as np
import time
import random
from random import randint
from Tkinter import *
import threading
import asl_ANN

path = '/Users/kevingottfried/Documents/CS_228/Deliverables/Deliverable_7/userData/'
completeName = os.path.join(path, 'classifier.p')
f = open(completeName,'rb')
digitCorrect = 10
clf = pickle.load(f)
testData = np.zeros((1,30),dtype='f')
#testData[:] = None
#print(testData)
matplotlib.interactive(True)
fig = plt.figure( figsize = (8,6))
ax = fig.add_subplot(111, projection='3d')
success = False
xPt = 0
yPt = 0
xMin = 1000.0
xMax = -1000.0
yMin = 1000.0
yMax = -1000.0
zMin = 0
zMax = 1000

controller = Leap.Controller() 
lines = [] 

def CenterData(testData):
    allXCoordinates = testData[0,::3]
    meanValue = allXCoordinates.mean()
    testData[0,::3] = allXCoordinates - meanValue
    allYCoordinates = testData[0,1::3]
    meanValue = allYCoordinates.mean()
    testData[0,1::3] = allYCoordinates - meanValue
    allZCoordinates = testData[0,2::3]
    meanValue = allZCoordinates.mean()
    testData[0,2::3] = allZCoordinates - meanValue
    return testData
    
def Success():
    global testData, predictedClass, digitCorrect
    success = False
    #thisData = testData
    #if(testData.isnan(float)):
    #    return
    thisData = CenterData(testData)
    predictedClass = clf.predict(thisData)
    numList = [0,1,2,3,4,5,6,7,8,9]
    if(not HandOverDevice):
        return
    if (predictedClass in numList):
        success = True
        numList.remove(predictedClass)
        digitCorrect = predictedClass[0]
        print(predictedClass[0])
    return success
        
def HandleHand():
    global testData
    frame = controller.frame()
    if(len(frame.hands) > 0):
        k = 0
        hand = frame.hands[0]
        for i in range(0,5):
            fingers = hand.fingers
            finger_type = fingers.finger_type(i)
            finger = finger_type[0]
            for j in range(0,4):
                bone = finger.bone(j)
                base = bone.prev_joint
                tip = bone.next_joint 
                xTip = tip[0]
                yTip = tip[1]
                zTip = tip[2]
                xBase = base[0]
                yBase = base[1]
                zBase = base[2]
                if ( (j==0) | (j==3) ):
                    testData[0,k] = xTip
                    testData[0,k+1] = yTip
                    testData[0,k+2] = zTip
                    k = k + 3
                lines.append(ax.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip],'r'))

        #testData = CenterData(testData)
        #predictedClass = clf.predict(testData)
        #print predictedClass
    plt.pause(0.001)
    plt.draw()
    while(len(lines) > 0):
        ln = lines.pop(0)
        ln.pop(0).remove()
        ax.set_xlim(-400,400)
        ax.set_ylim(-700,700)
        ax.set_zlim(-700,700)
        ax.view_init(azim=90)
        del ln
        ln = []
def State0():
    global programState, firstAttempt
    if(HandOverDevice()):
        time.sleep(1)
def Run():
    count = 0
    HandleHand()
    while(not HandOverDevice()):
        HandleHand()
    HandleHand()
    while(count != 30):
        HandleHand()
        count +=1
    while(not Success()):
        HandleHand()
        #if(Success()):
        #    return

def Pipe():
    global digitCorrect
    SendDigit(digitCorrect)
    print("saved")
    #os.system('"/Users/kevingottfried/Documents/CS_228/Deliverables/Deliverable\ 6/asl_ANN.py"')
    #p = subprocess.Popen(["python ","/Users/kevingottfried/Documents/CS_228/Deliverables/Deliverable\ 6/asl_ANN.py"], stdout=subprocess.PIPE,shell=True)
    #stdout,stderr = p.communicate(str(digitCorrect))
    #p.wait()
    #print(stdout)
    
def SendDigit(digitCorrect):
    save_path = "/Users/kevingottfried/Documents/CS_228/Final/final/"
    completeName = os.path.join(save_path, "digC.dat")
    print(digitCorrect)
    f = open(completeName, 'w')
    f.write("%i" % digitCorrect)
    f.close()

def Robot(digitCorrect):
    #import asl_ANN 
    print("waited")
    #p1 = p.RunANN(digitCorrect)
    asl_ANN.RunANN()
    #p1.parentString = "best_" + str(digitCorrect) +".dat"
    #p1.parent1 = p1.MatrixCreate(p1.numSensors,p1.numMotors)
    #p1.parent1 = p1.BestMatrix(p1.parent1, p1.parentString)
    #p1.parent1 = p1.Fitness3_Get(p1.parent1)

def HandOverDevice():
    hand = False
    frame = controller.frame()
    if(len(frame.hands) > 0):
        hand = True
    return hand

while True:
    
    #Run()
    #os.system('"/Users/kevingottfried/Documents/CS_228/Deliverables/Deliverable 6/asl_ANN.py"')
    
    a = threading.Thread(target = Run()).start()
    p = threading.Thread(target = Pipe()).start()
    q = threading.Thread(target = Robot(digitCorrect)).start()
    #print(stdout + "here")




    