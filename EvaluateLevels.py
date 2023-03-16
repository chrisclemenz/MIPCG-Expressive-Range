# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 20:25:07 2023

@author: Christian
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

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
    islands = []
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
        islands.append(island)

    return islands



def calc_expressive_range(path):
    leniencies = []
    openness = []
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
        
        total = chests + monsters + traps
        leniency = chests - monsters - traps
        #print("leniency" + str(leniency))
        leniencies.append(leniency/total)
        
        #openness
        wallID = 16
        floorID = 4
        door1ID = 2
        door2ID = 3
        walls = np.count_nonzero(data == 16)
        floors = np.count_nonzero(data == 4)
        openness.append(floors/(walls+floors))
        #connectedness
        rooms = findIslands(data, {floorID})
        connected_rooms = findIslands(data, {floorID,door1ID,door2ID})
        connectedness.append(len(connected_rooms)/len(rooms))
        #print(len(connected_rooms)/len(rooms))
        
    leniencies = np.array(leniencies)
    #print(leniencies)
    ratio = 2/(np.max(leniencies)-np.min(leniencies)) 
    shift = (np.max(leniencies)+np.min(leniencies))/2 
    #print(np.max(leniencies))
    #print(np.min(leniencies))
    #print(ratio)
    #print(shift)
    #leniencies = (leniencies - shift)*ratio
    #print(leniencies)
    
    #shift = np.max(openness) - np.min(openness)
    #print( (openness - np.min(openness))/shift)
    plt.hist(leniencies,range=[-1,1], bins= 50)
    plt.xlabel('leniency', fontsize=20)
    plt.title("")
    plt.show()
    
    plt.hist(openness,range = [0,1],bins= 200)
    plt.xlabel('openness', fontsize=20)
    plt.title("")
    plt.show()
    
    plt.hist(connectedness, range = [0,1],bins= 50)
    plt.xlabel('connectedness', fontsize=20)
    plt.title("")
    plt.show()
    
    plt.hist2d(openness, connectedness, bins=(100, 100),range=[[0, 1], [0, 1]])
    plt.colorbar()
    plt.xlabel('openness', fontsize=20)
    plt.ylabel('connectedness', fontsize=20)
    plt.title("expressive range")
    plt.show()
    
    plt.hist2d(openness, leniencies, bins=(100, 100),range=[[0, 1], [-1, 1]])
    plt.colorbar()
    plt.xlabel('openness', fontsize=20)
    plt.ylabel('leniency', fontsize=20)
    plt.title("expressive range")
    plt.show()
    
    
    
path = 'Levels'
path_smoothed = 'Levels_smoothing'
calc_expressive_range(path)
calc_expressive_range(path_smoothed)
