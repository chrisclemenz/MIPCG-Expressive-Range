# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 20:25:07 2023

@author: Christian
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
np.set_printoptions(linewidth=100)
path = 'Levels'

leniencies = []
openness = []

for level in os.listdir(path):
    print(level)
    
    #read in level data
    f = open(path + '/' + level, "r")
    dim = f.readline().split()
    width = int(dim[0])
    height = int(dim[1])
    f.readline()
    #data = [[-1] * width]*height
    data = []
    
    #human objects
    for y in range(height):
        line = f.readline()
        data.append(list(map(int,line.split())))
        #print(line)
    
    test = f.readline()
    
    #AI objects
    for y in range(height):
        line = f.readline().split()
        for x in range(width):
            if int(line[x])>-1 : data[y][x] = int(line[x])
        
    data = np.array(data)    
    #print(data)
    
    
    chestID = 0
    monsterID = 6
    trapID = 12
    
    #leniency
    chests = 0
    monsters = 0
    traps = 0
    
    for row in data:
        for cell in row:
            if cell == chestID: chests+=1
            if cell == monsterID: monsters+=1
            if cell == trapID: traps+=1

    #print("chests: " + str(chests))
    #print("monsters: " + str(monsters))
    #print("traps:" + str(traps))
    
    leniency = chests - monsters - traps
    #print("leniency" + str(leniency))
    leniencies.append(leniency)
    
    #openness
    wallID = 16
    floorID = 4
    walls = np.count_nonzero(data == 16)
    floors = np.count_nonzero(data == 4)
    openness.append(floors/walls)
    #connectedness
    
    
leniencies = np.array(leniencies)
print(leniencies)
ratio = 2/(np.max(leniencies)-np.min(leniencies)) 
shift = (np.max(leniencies)+np.min(leniencies))/2 
print(np.max(leniencies))
print(np.min(leniencies))
print(ratio)
print(shift)
leniencies = (leniencies - shift)*ratio
print(leniencies)

shift = np.max(openness) - np.min(openness)
openness = (openness - np.min(openness))/shift
#print( (openness - np.min(openness))/shift)
plt.hist(leniencies)
plt.show()
plt.hist(openness)
plt.show

plt.hist2d(leniencies, openness, bins=(20, 20))
plt.colorbar()
plt.show()