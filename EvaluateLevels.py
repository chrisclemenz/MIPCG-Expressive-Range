# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 20:25:07 2023

@author: Christian
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import copy

def swap_cols(arr, frm, to):
    arr[:,[frm, to]] = arr[:,[to, frm]]


def findIslands(board,indices):
    visited = set()
    queue = deque()
    notVisited = set()
    for index in indices:
        floors = np.argwhere(board == index)
        swap_cols(floors, 0, 1)
        notVisited.update(map(tuple, floors))
    rooms = []
    while len(notVisited)>0:
        start = list(notVisited)[0]
        queue.append(start)
        visited.add(start)
        notVisited.remove(start)
        island = [start]
        while queue:
            element = queue.popleft()
            y = element[1]
            x = element[0]
            
            up = (x,y-1)
            down = (x,y+1)
            left = (x-1,y)
            right = (x+1,y)
                    
            if up not in visited and all(ele >= 0 for ele in up) and all(ele < len(board) for ele in up) and board[up[1]][up[0]] in indices:
                visited.add(up)
                notVisited.discard(up)
                queue.append(up)
                island.append(up)
            if down not in visited and all(ele >= 0 for ele in down) and all(ele < len(board) for ele in down) and board[down[1]][down[0]] in indices:
                visited.add(down)
                notVisited.discard(down)
                queue.append(down)
                island.append(down)
            if left not in visited and all(ele >= 0 for ele in left) and all(ele < len(board) for ele in left) and board[left[1]][left[0]] in indices:
                visited.add(left)
                notVisited.discard(left)
                queue.append(left)
                island.append(left)
            if right not in visited and all(ele >= 0 for ele in right) and all(ele < len(board) for ele in right) and board[right[1]][right[0]] in indices:
                visited.add(right)
                notVisited.discard(right)
                queue.append(right)
                island.append(right)
        rooms.append(island)

    return rooms

chestID = 0
monsterID = 6
trapID = 12
wallID = 16
floorID = 4
door1ID = 2
door2ID = 3

def calc_expressive_range(path, smoothed):
    leniencies = []
    emptiness = []
    connectedness = []
    
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
        
        
        #### evaluate training data
        training_data = copy.deepcopy(data)
        training_data = np.array(training_data)
        
        chests = 0
        monsters = 0
        traps = 0
        
        for row in training_data:
            for cell in row:
                if cell == chestID: chests+=1
                if cell == monsterID: monsters+=1
                if cell == trapID: traps+=1
        
        total = chests + monsters + traps
        training_leniency = (chests - monsters - traps)/total
        
        walls = np.count_nonzero(np.logical_and(training_data !=4, training_data!=-1))
        floors = np.count_nonzero(training_data == 4)
        training_emptiness = floors/(walls+floors)
        

        rooms = findIslands(training_data, {floorID})
        connected_rooms = findIslands(training_data, {floorID,door1ID,door2ID})
        training_connectedness = len(connected_rooms)/len(rooms)
        
        #####
        f.readline()
        
        
        #AI objects
        for y in range(height):
            line = f.readline().split()
            for x in range(width):
                if int(line[x])>-1 : data[y][x] = int(line[x])
            
        data = np.array(data)    
        
        
        #leniency
        chests = 0
        monsters = 0
        traps = 0
        
        for row in data:
            for cell in row:
                if cell == chestID: chests+=1
                if cell == monsterID: monsters+=1
                if cell == trapID: traps+=1
    
       
        
        total = chests + monsters + traps
        leniency = chests - monsters - traps
        leniencies.append(leniency/total)
        
        #emptiness
        
        walls = np.count_nonzero(np.logical_and(data !=4, data!=-1))
        floors = np.count_nonzero(data == 4)
        emptiness.append(floors/(walls+floors))
        #connectedness
        rooms = findIslands(data, {floorID})
        connected_rooms = findIslands(data, {floorID,door1ID,door2ID})
        connectedness.append(len(connected_rooms)/len(rooms))
        #print(len(connected_rooms)/len(rooms))
        
    leniencies = np.array(leniencies)
    
    postfix = " with Smoothing" if smoothed else " without Smoothing"
    
    plt.hist(leniencies,range=[-1,1], bins= 50)
    plt.xlabel('leniency', fontsize=20)
    plt.title("")
    plt.axvline(training_leniency, color='red', linestyle='dashed', linewidth=1)
    plt.show()
    
    plt.hist(emptiness,range = [0,1],bins= 200)
    plt.xlabel('emptiness', fontsize=20)
    plt.title("")
    plt.axvline(training_emptiness, color='red', linestyle='dashed', linewidth=1)
    plt.show()
    
    plt.hist(connectedness, range = [0,1],bins= 50)
    plt.xlabel('connectedness', fontsize=20)
    plt.axvline(training_connectedness, color='red', linestyle='dashed', linewidth=1)
    plt.title("")
    plt.show()
    
    plt.hist2d(emptiness, connectedness, bins=(100, 100),range=[[0, 1], [0, 1]],vmin=0,vmax=10)
    plt.colorbar()
    plt.xlabel('Emptiness', fontsize=20)
    plt.ylabel('Connectedness', fontsize=20)
    plt.title("Expressive Range" + postfix)
    plt.plot(training_emptiness,training_connectedness,marker='o',color='red')
    plt.show()
    
    plt.hist2d(emptiness, leniencies, bins=(100, 100),range=[[0, 1], [-1, 1]],vmin=0,vmax=10)
    plt.colorbar()
    plt.xlabel('Emptiness', fontsize=20)
    plt.ylabel('Leniency', fontsize=20)
    plt.title("Expressive Range" + postfix)
    plt.plot(training_emptiness,training_leniency,marker='o',color='red')

    plt.show()
    
    plt.hist2d(connectedness, leniencies, bins=(100, 100),range=[[0, 1], [-1, 1]],vmin=0,vmax=10)
    plt.colorbar()
    plt.xlabel('Connectedness', fontsize=20)
    plt.ylabel('Leniency', fontsize=20)
    plt.title("Expressive Range" + postfix)
    plt.plot(training_connectedness,training_leniency,marker='o',color='red')
    plt.show()
    
path = 'Levels'
path_smoothed = 'Levels_smoothing'
calc_expressive_range(path, False)
calc_expressive_range(path_smoothed,True)
