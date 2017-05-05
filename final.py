# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import sys
import os;
import subprocess
sys.path.insert(0, "/Users/kevingottfried/Documents/CS_228/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib")
import Leap
import pickle
import numpy as np
import time
import random
from random import randint
from Tkinter import *



userName = ""
path1 = '/Users/kevingottfried/Documents/CS_228/Deliverables/Deliverable_8/userData/'
dataName = os.path.join(path1, 'dataBase.p')
f = open(dataName, 'rb')
dataBase = pickle.load(f)
f.close()
print dataBase
count = 0
digitsList = [0,1,2,3,4,5,6,7,8,9,]
state5 = False
lastDigit = None
loginAttempt = 0
state5Correct = [0] * 10
master = Tk()
firstAttempt = True
predictedClass = None
def Init():
    #global userName, dataBase, loginAttempt
    ent = StringVar()
    master.geometry('400x150+500+300')
    master.title('Please Login')
    Label(master, text="Please Login Using Your First Name").grid(row=1,column=1, sticky=W)
    Label(master, text="First Name:").grid(row=2,column=0, sticky=W)
    Entry(master, textvar = ent).grid(row=2,column=1, sticky=W)
    Button(master, text='Login', command = lambda: Dict(ent)).grid(row=3, column=1, pady=4)
    master.protocol("Continue", quit)
    master.mainloop()

def quit():
    master.quit()
    
def Dict(ent):
    global userName, loginAttempt
    userName = ent.get()
    print 'hi'
    print userName
    if userName in dataBase:
        logins = dataBase[userName]
        login = logins['logins']
        login = login + 1 
        loginAttempt = login
        logins['logins'] = login
        dataBase[userName] = logins
        string = "Welcome back " + userName + "."
        Label(master, text=string).grid(row=4,column=1, sticky=W)
        #print logins
    else:
        login = 1
        logins = {}
        loginAttempt = 1
        #loginNum = 'login #1'
        #logins['logins'] = loginAttempts
        logins['logins'] = login
        dataBase[userName] = logins
        string = "Welcome " + userName + '.'
        Label(master, text= string).grid(row=4,column=1, sticky=W)
    pickle.dump(dataBase,open(dataName, 'wb'))
    LoginAttempt()
    time.sleep(5)
    master.quit()
def LoginAttempt():
    global userName, dataBase, loginAttempt
    userRecord = dataBase[userName]
    loginNum = 'login #' + str(loginAttempt)
    if 'login attempts' in userRecord:
        if loginNum in userRecord['login attempts']:
            loginNum = 'login #' + str(loginAttempt)
            userRecord['login attempts'] = loginNum
            dataBase[userName] = userRecord
        else:
            loginAttempts = userRecord['login attempts']
            loginAttempts[loginNum] = {}
            userRecord['login attempts'] = loginAttempts
            dataBase[userName] = userRecord
    else:
        loginAttempts = {}
        loginAttempts[loginNum] = {}
        userRecord['login attempts'] = loginAttempts
        dataBase[userName] = userRecord
    pickle.dump(dataBase,open(dataName, 'wb'))
def SetState5():
    global dataBase, digitsList, loginAttempt, state5
    loginNum = 'login #' + str(loginAttempt)
    userRecord = dataBase[userName]
    logins = userRecord['login attempts']
    login = logins[loginNum]
    loginState = True
    login['State'] = loginState
    logins[loginNum] = login
    userRecord['logins'] = logins
    dataBase[userName]
    pickle.dump(dataBase,open(dataName, 'wb'))
#def GetState5():
#    global dataBase, digitsList, loginAttempt, state5
#    userRecord = dataBase[userName]
#    logins = userRecord['login attempts']
#    login = userRecord['logins']
#    lastLog = loginAttempt - 1
#    if (login >= 2):
#        loginNum = 'login #' + str(lastLog)
#        login = logins[loginNum]
#        if 'State' in login:
#            loginState = login['State']
#            if(loginState == 'True'):
#                state5 = True

def DigitAttempt(digit):
    global dataBase, digitsList, loginAttempt
    userRecord = dataBase[userName]
    loginNum = 'login #' + str(loginAttempt)
    logins = userRecord['login attempts']
    loginAttempts = logins[loginNum]
    digitString = 'digit ' + str(digit)
    print digitString
    if 'Digits Attempted' in loginAttempts:
        if digitString in loginAttempts['Digits Attempted']:
            digits = loginAttempts['Digits Attempted']
            loginAttempts['Digits Attempted'] = digits
            logins[loginNum]
            userRecord['login attempts'] = logins
            dataBase[userName] = userRecord
            #print digits
        else:
            digits = loginAttempts['Digits Attempted']
            digits[digitString] = {}
            loginAttempts['Digits Attempted'] = digits
            logins[loginNum] = loginAttempts
            userRecord['login attempts'] = logins
            dataBase[userName] = userRecord
            
    else:
        digits = {}
        digits[digitString] = {}
        loginAttempts['Digits Attempted'] = digits
        logins[loginNum] = loginAttempts
        userRecord['login attempts'] = logins
        dataBase[userName] = userRecord
    pickle.dump(dataBase,open(dataName, 'wb'))
    
def DigitCorrect(digit, frameCount):
    global userName, dataBase, loginAttempt
    userRecord = dataBase[userName]
    digitString = 'digit ' + str(digit)
    loginNum = 'login #' + str(loginAttempt)
    logins = userRecord['login attempts']
    digitAttempts = logins[loginNum]
    digits = digitAttempts['Digits Attempted']
    if 'Correct' in digits[digitString]:
        correct = digits[digitString]
        correct['Correct'] = correct['Correct'] + 1
        DigitTime(digit, frameCount)
        if correct['Correct'] > 5:
            digitsList.remove(digit)
    else:
        DigitTime(digit, frameCount)
        correct = digits[digitString]
        correct['Correct'] = 1
        digits[digitString] = correct
        digitAttempts['Digits Attempted'] = digits
        logins[loginNum] = digitAttempts
        userRecord['login attempts'] = logins
        dataBase[userName] = userRecord
        #print digits
    #print dataBase
    pickle.dump(dataBase,open(dataName, 'wb'))
    
def DigitMissed(digit, frameCount):
    global userName, database, digitsList, loginAttempt
    userRecord = dataBase[userName]
    digitString = 'digit ' + str(digit)
    loginNum = 'login #' + str(loginAttempt)
    logins = userRecord['login attempts']
    digitAttempts = logins[loginNum]
    digits = digitAttempts['Digits Attempted']
    if 'Missed' in digits[digitString]:
        missed = digits[digitString]
        missed['Missed'] = missed['Missed'] + 1
        DigitTime(digit, frameCount)
        if (missed['Missed'] > 2):
            digitsList.append(digit)
    else:
        DigitTime(digit, frameCount)
        missed = digits[digitString]
        missed['Missed'] = 1
        digits[digitString] = missed
        digitAttempts['Digits Attempted'] = digits
        logins[loginNum] = digitAttempts
        userRecord['login attempts'] = logins
        dataBase[userName] = userRecord
    pickle.dump(dataBase, open(dataName,'wb'))
    
def DigitTime(digit, frameCount):
    global userName, database, digitsList, loginAttempt
    userRecord = dataBase[userName]
    digitString = 'digit ' + str(digit)
    loginNum = 'login #' + str(loginAttempt)
    logins = userRecord['login attempts']
    digitAttempts = logins[loginNum]
    digits = digitAttempts['Digits Attempted']
    Time = 0
    newTime = float(frameCount)/2
    count = 0
    if 'Missed' in digits[digitString]:
        missed = digits[digitString]
        count = missed['Missed']
    if 'Correct' in digits[digitString]:
        correct = digits[digitString]
        count = correct['Correct'] + count
    if 'Elapsed Time' in digits[digitString]:
        elapsed = digits[digitString]
        Time = elapsed['Elapsed Time']
        Time = Time * newTime/count
        elapsed['Elapsed Time'] = Time
        #elapsed['Elapsed Time'] = time
    else:
        elapsed = digits[digitString]
        elapsed['Elapsed Time'] = newTime
        digits[digitString] = elapsed
        digitAttempts['Digits Attempted'] = digits
        logins[loginNum] = digitAttempts
        userRecord[userName] = userRecord
    print digits
    pickle.dump(dataBase, open(dataName, 'wb'))
    
def PlotDict():
    def split_word(s):
        n = 6
        return '-\n'.join(s[i:i+n] for i in range(0, len(s), n))
    plt.close('all')
    global dataBase, userName, loginAttempt
    lastAttempt = loginAttempt - 1
    loginNum = 'login #' + str(loginAttempt)
    lastNum = 'login #' + str(lastAttempt)
    userRecord = dataBase[userName]
    logins = userRecord['login attempts']
    digitAttempts = logins[loginNum]
    if(lastAttempt== 0 and not bool(digitAttempts)):
        return
    if(lastAttempt != 0):
        digitLast = logins[lastNum]
        if (not 'Digits Attempted' in digitLast):
            return
    digits = digitAttempts['Digits Attempted']
    plotCorrect = {}
    plotMissed = {}
    for i in range(0,10):
        digitString = 'digit ' + str(i)
        if digitString in digits:
            if 'Correct' in digits[digitString]:
                digitCorrect = digits[digitString]
                correct = digitCorrect['Correct']
            else:
                correct = 0
            
        else:
            correct = 0
        plotCorrect[digitString] = correct
    for i in range(0,10):
        digitString = 'digit ' + str(i)
        if digitString in digits:
            if 'Missed' in digits[digitString]:
                digitMissed = digits[digitString]
                missed = digitMissed['Missed']
            else:
                missed = 0
            
        else:
            missed = 0
        plotMissed[digitString] = missed
        
    #plt.subplot(2,1,1)   
    plt.bar(range(len(plotCorrect)), plotCorrect.values(), color='g', label="Correct")
    plt.bar(range(len(plotMissed)), plotMissed.values(), color='r', label="Missed")
    plt.xticks(range(len(plotCorrect)),plotCorrect.keys())
    plt.xlabel('ASL digits Attempted')
    plt.ylabel('# of Attempts')
    plt.legend()
    plt.pause(4.20)
    plt.draw()
    
def PlotLast():
    global dataBase, userName, loginAttempt
    if(loginAttempt <= 1):
        return
    lastAttempt = loginAttempt - 1
    loginNum = 'login #' + str(loginAttempt)
    lastNum = 'login #' + str(lastAttempt)
    userRecord = dataBase[userName]
    logins = userRecord['login attempts']

    digitAttempts = logins[lastNum]
    if (not 'Digits Attempted' in digitAttempts):
        return
    digits = digitAttempts['Digits Attempted']
    plotCorrect = {}
    plotMissed = {}
    for i in range(0,10):
        digitString = 'digit ' + str(i)
        if digitString in digits:
            if 'Correct' in digits[digitString]:
                digitCorrect = digits[digitString]
                correct = digitCorrect['Correct']
            else:
                correct = 0
            
        else:
            correct = 0
        plotCorrect[digitString] = correct
    for i in range(0,10):
        digitString = 'digit ' + str(i)
        if digitString in digits:
            if 'Missed' in digits[digitString]:
                digitMissed = digits[digitString]
                missed = digitMissed['Missed']
            else:
                missed = 0
            
        else:
            missed = 0
        plotMissed[digitString] = missed
        
    #plt.subplot(2,1,1)   
    plt.bar(range(len(plotMissed)), plotMissed.values(), color='r', label="Missed")
    plt.bar(range(len(plotCorrect)), plotCorrect.values(), color='g', label="Correct")
    plt.xticks(range(len(plotCorrect)),plotCorrect.keys())
    plt.xlabel('ASL digits Attempted')
    plt.ylabel('# of Attempts')
    plt.legend()
    plt.pause(4.20)
    plt.draw()
      
def PlotCurrent(num):
    global dataBase, userName, loginAttempt
    lastAttempt = loginAttempt - 1
    loginNum = 'login #' + str(loginAttempt)
    lastNum = 'login #' + str(lastAttempt)
    userRecord = dataBase[userName]
    logins = userRecord['login attempts']
    digitAttempts = logins[loginNum]
    if(lastAttempt== 0):
        return
    
    digitLast = logins[lastNum]
    while((not 'Digits Attempted' in digitLast) or lastAttempt == 0):
        lastAttempt -= 1
        lastNum = 'login #' + str(lastAttempt)
        digitLast = logins[lastNum]
    digits = digitAttempts['Digits Attempted']
    digitsLast = digitLast['Digits Attempted']
    plotCorrect = {}
    plotMissed = {}
    plotLastC = {}
    plotLastM = {}
    digitString = 'digit ' + str(num)
    if digitString in digits:
        if 'Correct' in digits[digitString]:
            digitCorrect = digits[digitString]
            correct = digitCorrect['Correct']
        else:
            correct = 0
    else:
        correct = 0
        
    plotCorrect = correct
    
    if digitString in digitsLast:
        if 'Correct' in digitsLast[digitString]:
            digitCorrect = digitsLast[digitString]
            correct = digitCorrect['Correct']
        else:
            correct = 0
    else:
        correct = 0
    plotLastC = correct

    if digitString in digits:
        if 'Missed' in digits[digitString]:
            digitMorrect = digits[digitString]
            missed = digitMorrect['Missed']
        else:
            missed = 0
    else:
        missed = 0
        
    plotMissed = missed
    
    if digitString in digitsLast:
        if 'Missed' in digitsLast[digitString]:
            digitMissed = digitsLast[digitString]
            missed = digitMissed['Missed']
        else:
            missed = 0
    else:
        missed = 0
    plotLastM = missed
    
    plt.subplot2grid((2,2),(1,1))
    plt.bar(3,plotCorrect, .35, color='b', label="Correct")
    plt.bar(2,plotMissed, .35, color='y', label="Missed")
    plt.bar(1,plotLastC, .35, color ='g', label = "Last Login Correct")
    plt.bar(0,plotLastM, .35, color ='r', label = "Last Login Missed")
    plt.xlabel('ASL digits Attempted')
    plt.ylabel('# of Attempts')
    plt.legend()
    plt.draw()
   
def PlotAll():
    global dataBase
    #userNames = []
    times = []
    nums = []
    counts = []
    #correct = [0] * 10
    #missed = [0] * 10
    
    for key in dataBase:
        userRecord = dataBase[key]
        print userRecord
        logins = userRecord['login attempts']
        for login in logins:
            digitAttempts = logins[login]
            if('Digits Attempted' in digitAttempts):
                digits = digitAttempts['Digits Attempted']
                nums.append[digits]
                for i in digits:
                    digit = digits[i]
                    print i
                    if 'Elapsed Time' in digits[i]:
                        elapsed = digits[i]
                        elapsedTime = elapsed['Elapsed Time']
                        correct = digit['Correct']
                        e = int(round(elapsedTime))
                        lhs, rhs = i.split(' ')
                        times.append(e) 
                        counts.append(int(correct))
                    #elif( 'Missed' in digits[i]):
                    #    elapsedTime = 8
                    #    missed  = digit['Missed']
                    #    times[elapsedTime][digit] += missed
    x = counts
    y = times
    x, y = np.meshgrid(x,y)
    nRows = counts.shape[0]
    Xs = x*nRows
    area = np.pi * (30 * counts)**2
    plt.subplot(1,1,1)
    plt.scatter(nums, times, s=2000, c='g', alpha=0.5)
    plt.pause(10)
    plt.draw()
    print times
def PlotNow():
    plt.close('all')
    plt.subplot(2,1,1)
    x = [0,1,2,3,4,5,6,7,8,9,0,3,5,1,7,2,9,4]
    y = [2,1,1,3,1,4,6,6,4,5,4,8,2,5,8,4,2,7]
    colors = np.random.rand(18)
    area = np.pi * (30 * np.random.rand(18))**2  # 0 to 15 point radiuses
    #print (15 * np.random.rand(N))**2
    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    plt.title('Time for Successful Attempt of Digit for All Users')
    plt.xlabel('ASL digits Attempted')
    plt.ylabel('Time for successful attempt')
    plt.pause(5)
    plt.draw()
     
Init()


print dataBase
print digitsList
PlotLast()
#GetState5()


path = '/Users/kevingottfried/Documents/CS_228/Deliverables/Deliverable_7/'
completeName = os.path.join(path, 'classifier.p')
f = open(completeName,'rb')
clf = pickle.load(f)
testData = np.zeros((1,30),dtype='f')
programState = 0
matplotlib.interactive(True)
controller = Leap.Controller() 
lines = [] 
# The data from the database is plotted: Correct of digit attempts

def setState(num):
    global programState
    programState = num
def getState():
    global programState
    return programState
def CenterData(X):
    allXCoordinates = X[0,::3]
    meanValue = allXCoordinates.mean()
    X[0,::3] = allXCoordinates - meanValue
    allYCoordinates = X[0,1::3]
    meanValue = allYCoordinates.mean()
    X[0,1::3] = allYCoordinates - meanValue
    allZCoordinates = X[0,2::3]
    meanValue = allZCoordinates.mean()
    X[0,2::3] = allZCoordinates - meanValue
    return X
def CenterImage():
    global testData
    center = 4
    allXCoordinates = testData[0,::3]
    meanValue = allXCoordinates.mean()
    if(meanValue > 50):  
        center = 1
    elif(meanValue < -50):
        center = 2
    else:
        center = 0
    return center
    
def DrawHelpImage():
    file1 = os.path.join(path,'intro1.jpg')
    file2 = os.path.join(path,'intro.png')
    image = plt.imread(file1)
    img = plt.imread(file2)
    plt.subplot(2,1,1)
    plt.axis('off')
    plt.imshow(image)
    plt.subplot(2,1,2)
    plt.axis('off')
    plt.imshow(img)
    plt.pause(.001)
    plt.draw()
    
def showASL(rand):
    img = os.path.join(path, 'aslNum/number0{}.jpg'.format(rand))
    image = plt.imread(img)
    plt.subplot2grid((2,2),(0,0))
    plt.imshow(image)
    plt.axis('off')  # clear x- and y-axes
    plt.draw()
    
def showNum(digit):
    global state5
    numstring = "number" + str(digit)
    img = os.path.join(path, 'Nums/' + numstring + ".jpg")
    image = plt.imread(img)
    if(state5):
        plt.subplot(2,1,1)
    else:
        plt.subplot2grid((2,2),(0,1))
    plt.imshow(image)
    plt.axis('off')
    plt.draw()
    
def HandOverDevice():
    hand = False
    frame = controller.frame()
    if(len(frame.hands) > 0):
        hand = True
    return hand
    
def Success(rand):
    global testData, predictedClass
    success = False
    #thisData = testData
    thisData = CenterData(testData)
    predictedClass = clf.predict(thisData)

    if (predictedClass == rand):
        success = True
        
    return success
       
def InstructHand(image1, image2):
    global firstAttempt
    file1 = os.path.join(path,image1)
    file2 = os.path.join(path,image2)
    file3 = os.path.join(path,'check.png')
    file4 = os.path.join(path,'missed.png')
    image = plt.imread(file1)
    img = plt.imread(file2)
    img3 = plt.imread(file3)
    img4 = plt.imread(file4)
    plt.subplot(2,2,1)
    plt.axis('off')
    plt.imshow(image)
    plt.subplot(2,2,2)
    plt.axis('off')
    plt.imshow(img)
    plt.subplot(2,2,3)
    plt.axis('off')
    plt.imshow(img3)
    plt.subplot(2,2,4)
    plt.axis('off')
    plt.imshow(img4)
    plt.pause(.001)
    plt.draw()
    time.sleep(4)
    
def HandleState0():
    global programState, firstAttempt
    DrawHelpImage()
    if(HandOverDevice()):
        time.sleep(2)
        setState(1)
        plt.close('all')
    #if(firstAttempt):
        #InstructHand('righthand.jpg','wronghand.jpg')
        #firstAttempt = False
def HandleState1():
    global testData, programState
    
    Center()
    HandleHand(False,0)
    if(Center()):
        plt.close('all')
        setState(2)
    if(not HandOverDevice()):
        plt.close()
        setState(0)
    
def HandleState2():
    global testData, programState, lastDigit, predictedClass
    frameCount = 0
    #rand = randint(0,9)
    if(len(digitsList) != 0):
        if(len(digitsList) > 1):
            rand = random.choice(digitsList)
            while(lastDigit == rand):
                rand = random.choice(digitsList)
        else:
            rand = digitsList[0]
        lastDigit = rand
    else:
        setState(5)
        SetState5()
        #PlotDict()
        return
    DigitAttempt(rand)
    #print rand
    showASL(rand)
    showNum(rand)
    #PlotCurrent(rand)
    HandleHand(False, 0)
    
    while (HandOverDevice() and Center() and (not Success(rand))):
        showASL(rand)
        showNum(rand)
        #PlotCurrent(rand)
        HandleHand(False,frameCount)
        newCount = 0        
        while(Success(rand)):
            if(newCount == 5):
                break
            HandleHand(True,newCount)
            newCount+=1
            
        #HandleHand()
        frameCount +=1
        if (frameCount == 16):
            setState(4)
            DigitMissed(rand, frameCount)
            numstring = "number0" + str(rand)
            img1 = os.path.join(path, 'aslNum/' + numstring + ".jpg")
            num = str(predictedClass)
            numstring = "number0" + str(num[2])
            img2 = os.path.join(path, 'aslNum/' + numstring + ".jpg")
            #InstructHand(img1,img2)
            return
    Center()
    if(Success(rand)):
        DigitCorrect(rand, frameCount)
        #DigitTime(rand, frameCount)
        setState(3) 
    if((not Center())):
        plt.close('all')
        setState(1)
    elif(not HandOverDevice()):
        plt.close('all')
        setState(0)
    else:
        setState(1)
    
def HandleState3():
    plt.close('all')
    plt.plot()
    image  = os.path.join(path, 'check.png')
    img = plt.imread(image)
    plt.imshow(img)
    plt.axis('off')
    plt.pause(1.5)
    setState(1)
    
def HandleState4():
    plt.close('all')
    plt.plot()
    image  = os.path.join(path, 'missed.png')
    img = plt.imread(image)
    plt.imshow(img)
    plt.axis('off')
    plt.pause(1.5)
    setState(1)
    
def HandleState5():
    global state5Correct, lastDigit
    frameCount = 0
    rand = randint(0,9)
    while(lastDigit == rand):
        rand = randint(0,9)
    lastDigit = rand
    showNum(rand)
    HandleHand()
    while (HandOverDevice() and Center() and (not Success(rand))):
        frameCount +=1
        showNum(rand)
        HandleHand()
        if(state5Correct[rand] >= 3):
            if (frameCount == 8):
                setState(4)
                DigitMissed(rand)
                return
        elif(state5Correct[rand] >= 5):
            if (frameCount == 6):
                setState(4)
                DigitMissed(rand)
                return
        if (frameCount == 12):
            setState(4)
            DigitMissed(rand)
            return

    Center()
    if(Success(rand)):
        state5Correct[rand] = state5Correct[rand] + 1
        #print state5Correct
        setState(3) 
    if((not Center())):
        plt.close('all')
        setState(1)
    elif(not HandOverDevice()):
        plt.close('all')
        setState(0)
    else:
        setState(1)

def HandleState6():
    global state5Correct
    rand = randint(0,9)
    showNum(rand)
    HandleHand()
    while (HandOverDevice() and Center() and (not Success(rand))):
        showNum(rand)
        HandleHand()
    Center()
    if(Success(rand)):
        state5Correct[rand] += 1
        setState(3) 
    if((not Center())):
        plt.close('all')
        setState(1)
    elif(not HandOverDevice()):
        plt.close('all')
        setState(0)
    else:
        setState(1)
def HandleHand(success, count):
    global testData
    ax = plt.subplot2grid((2,2),(1,0), projection='3d') 
    frame = controller.frame()
    k = 0
    hand = frame.hands[0]
    if (success):
        alpha = 1
    else:
        if(count == 0 or count == 1 or count == 2 or count == 3):
            alpha = .3
        else:
            alpha = 1/count
    #color = 'rgb({})'.format(1-alpha,alpha,0)
    #color = '(' + str(1-alpha)+ ',' + str(alpha) + ',0)'
    c = (1-alpha,alpha,0)
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
            lines.append(ax.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip], color = c))

    ax.set_xlim3d(-400,400)
    ax.set_ylim3d(-700,700)
    ax.set_zlim3d(-700,700)
    ax.view_init(azim=90)
    plt.pause(0.00001)
    plt.draw()

def Center():
    global testData
    centered = False
    if(CenterImage() == 0):
        image  = os.path.join(path, 'check.png')
        #image1 = os.path.join(path, 'handcorrect.jpg')
        centered = True        
    elif(CenterImage() == 1):
        image = os.path.join(path, 'left.jpeg')
        #image1 = os.path.join(path,'handright.jpg')
        #image2 = os.path.join(path,'handcorrect.jpg')
        centered = False
    elif(CenterImage() == 2):
        image = os.path.join(path, 'right.jpg')
        #image1 = os.path.join(path, 'handleft.jpg')
        #image2 = os.path.join(path, 'handcorrect.jpg')
        centered = False
    #if(not CenterImage() == 0):
    #    img1 = plt.imread(image1)
    #    plt.subplot(2,3,1)
    #    plt.imshow(img1)
    #    plt.axis('off')
    #    img2 = plt.imread(image2)
    #    plt.subplot(2,3,3)
    #    plt.imshow(img2)
    #    plt.axis('off')
    img = plt.imread(image)
    plt.subplot(2,3,2)
    plt.imshow(img)
    plt.axis('off')

    return centered
if(state5):
    for i in range(len(digitsList)):
        digitsList.remove(i)
    if(len(digitsList) ==0):
        print "yes"
while True:
    global state5
    programState = getState()
    if(programState == 0):
        HandleState0()
    elif(programState ==1):
        HandleState1()
    elif(programState ==2):
        HandleState2()
        count+=1
        if count == 8:
            PlotDict()
            #PlotNow()
            #plt.pause(4.20)
            count = 0
    elif(programState ==3):
        HandleState3()   
    elif(programState ==4):
        HandleState4()
    elif(programState == 5):
        state5 = True
        HandleState5()