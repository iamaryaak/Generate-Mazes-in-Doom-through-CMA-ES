from operator import itemgetter
import numpy as np
from matplotlib import *
import cma
import random
import os
from collections import Counter
import itertools

WALL = 1
WALL1 = 3
EMPTY = 0
HP = 2
max_num = 9
doomMap = [[WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
                [WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL]]


## Functions
def change_map(board):
	mapdm = []
    # Print the rows
	print(board)
	for r in board:
		tmp = []
		#print(r)
		rowprint = ""
		for c in r:
			if c == WALL:
				rowprint = rowprint + "X"
				tmp.append('X')
			elif c == HP:
				rowprint = rowprint + "H"
				tmp.append('H')
			#elif c == EMPTY:
			else:
				rowprint = rowprint + " "
				tmp.append(' ')

		mapdm.append(tmp)
		print(rowprint)
	return mapdm
        
def vector2map(seq):
    temp = doomMap
    #print(len(seq))
    for n in range(len(seq)):
        if n < 10:
            #print("HEALTH PACK")
            x_health = int(seq[n])
            n = n + 1
            #print(n)
            y_health = int(seq[n])
            n = n + 1
            #print(n)
            # check for out of range
            if temp[(x_health)][(y_health)] != WALL:
                    temp[(x_health)][(y_health)] = HP
        if n < 45 and n > 9:
            #print("WALL")
            x_wall = int(seq[n])
            n = n + 1
            #print(n)
            y_wall = int(seq[n])
            n = n + 1
            #print(n)
            angle = seq[n]
            n = n + 1
            #print(n)
            temp[(x_wall)][(y_wall)] = WALL
    # add wall and angle to txt files so we can use them to create .WAD files
    # wallCt = wallCt + 1
    # fileoutput = "my_maze_inputs/wallList_" + str(wallCt) + ".txt"
    # with open(fileoutput, 'w') as f:
    #     str1 = " ".join(str(e) for e in angled)
    #     f.write(str1)
    #     f.close()
    #     print(fileoutput, " is created!")
    # check if health pack exists, if it doesn't, add it
    if not any(HP in x for x in temp):
        x = random.randint(1, max_num)
        y = random.randint(1, max_num)
        if temp[x][y] != WALL:
                temp[x][y] = HP
        else:
                while temp[x][y] != WALL:
                        x = random.randint(1, max_num)
                        y = random.randint(1, max_num)
                temp[x][y] = HP 
    return temp

def undoNormalize(solutions, maxVectorValue, minVectorValue):
        #print("+++++ UNDO NORM +++++")
        #print("Min and Max\n", minVectorValue, " " ,maxVectorValue)
        # x1 = (zi * (max(x) - min(x))) + min(x)
        solutionsNormal = []
        for seq in solutions:
                print(seq)
                seqNorm = []
                for n in seq:
                        #print(n)
                        res = (n * (maxVectorValue - minVectorValue)) + minVectorValue
                        seqNorm.append(res)
                solutionsNormal.append(seqNorm)
        # check solution to see if it is unnormalized correctly
        #print("Result - undo normalize:") 
        
        return solutionsNormal


def evaluator(map):
    count = Counter(list(itertools.chain.from_iterable(map)))
    print(count)
    two_walls = [0]
    visited = map

    def dfs(x, y):
        if x>= len(map) or x < 0 or y<0 or y>= len(map[0]):
            return ['N']
        if map[x][y] == 'H' or visited[x][y] == ' ':
            visited[x][y] = 'T'
            
            res = dfs(x-1,y-1)+dfs(x-1,y)+dfs(x+1,y)+dfs(x-1,y+1)+ dfs(x,y-1)+ dfs(x+1,y-1)+dfs(x+1,y+1)+dfs(x,y+1)
            counts = Counter(res)
            if counts['X'] >= 4:
                two_walls[0] += 1

        return [map[x][y]]
    x, y = -1, -1
    for ele in range(len(map)):
        for element in range(len(map[ele])):
            if map[ele][element] == ' ':
                print("calling dfs",ele,element)
                x, y = ele, element
                break
        if x>=0:
            break
    dfs(x, y)                 
    visit = Counter(list(itertools.chain.from_iterable(map)))
    #print(two_walls[0])
    score = (visit['T']/(count[' ']+count['H']))*100 + two_walls[0]
    #print(visit['T']/(count[' ']+count['H'])*100)
    #print(visited)
    print("Map Score: ", score)
    return score

def toSolutionNormal(child, minVectorValue, maxVectorValue):
    solutionsNormal = []
    for n in child:
        #res = (n * (maxVectorValue - minVectorValue)) + minVectorValue
        num = n - minVectorValue # (xi - min(x))
        deno = maxVectorValue - minVectorValue # (max(x) - min(x))
        res = num / deno # zi
        solutionsNormal.append(res)
    return solutionsNormal
    
def toSolutionList(solutionsNormal):
    #print(solutionsNormal)
    solutionsList = [] 
    for n in solutionsNormal:
        #print(type(n), n)
                for s in n:
                        num = round(s, 2)
                        solutionsList.append(num)
    return solutionsList

def selection(maps):
    return maps[0:5]

def evolution(mapVector):
    ## Standardize the vector
    # zi = (xi – min(x)) / (max(x) – min(x))
    standardVector = []
    minVectorValue = min(mapVector)
    maxVectorValue = max(mapVector)
    for n in mapVector:
        num = n - minVectorValue # (xi - min(x))
        deno = maxVectorValue - minVectorValue # (max(x) - min(x))
        ans = num / deno # zi
        standardVector.append(ans)

    print("=========================== STANDARDIZED VECTOR ===========================")
    print(standardVector)
    print("Number of points: ", len(standardVector))

    # use CMA-ES
    x0 = standardVector  # initial solution
    sigma0 = 0.01 # std deviation

    # x = best evaluated values
    # es = the cma.CMAEvolutionStrategy class instance used to run the optimization.
    es = cma.CMAEvolutionStrategy(x0, sigma0)
    #print("=========================== MAP VECTOR ===========================")
    solutions = es.ask()
    #print(solutions)

    # xi = (zi * (max(x) - min(x))) + min(x)
    solutionsNormal = []
    for seq in solutions:
        seqNormal = []
        for n in seq:
            # xi = (zi * (max(x) - min(x))) + min(x)
            res = (n * (maxVectorValue - minVectorValue)) + minVectorValue
            seqNormal.append(res)
        solutionsNormal.append(seqNormal)
    

    #print("=========================== SOLUTIONS ===========================")
    #for s in solutionsNormal:
    #    print(s)

    #solutionsList = toSolutionList(solutionsNormal)
    solutionsList = [] 
    for s in solutionsNormal:
        sol = []
        for n in s:
            num = round(n, 2)
            sol.append(num)
        solutionsList.append(sol)

    #print(solutionsList)
    print("Number of Solutions Found: ", len(solutionsList))

    ## Now, convert the vector representation into 2D maps (.txt)
    ## Maps are size of 11 by 11 (set size)
    mapCT = 0
    wallCt = 0
    mapList = []
    maps=[]

    for seq in solutionsList:
        temp_map = doomMap
        print(seq)
        angled = []
        # set health packs first 5 pairs
        temp_map = vector2map(seq)
        mapList += temp_map
        mapV = change_map(temp_map)
        maps.append([seq, evaluator(mapV)])
    maps = sorted(maps, key=itemgetter(1))
    maps.reverse()
    print("=====================") 

    selected_children = selection(maps)

    #print(selected_children)
    #=================================================================================
    # We have done CMA for the first round, and we go loop on the next few generations
    print("start generation")
    generation = 3
    generation_count = 0
    while generation_count < generation:
        solutionsList = []

        for child in selected_children:
            minVec = min(child[0])
            maxVec = max(child[0])
            #print("Min and Max\n", minVec, " " ,maxVec)
            solutionsNormal = toSolutionNormal(child[0], minVec, maxVec)
            es = cma.CMAEvolutionStrategy(solutionsNormal, sigma0)
            solutions = es.ask()
            #print("Solutions generated: ", solutions)
            unNorm = undoNormalize(solutions, maxVec, minVec)
            current_solutions = toSolutionList(unNorm)
            solutionsList.append(current_solutions)
        
        maps=[]
        for child in solutionsList:
            temp_map = doomMap
            print(temp_map)
            angled = []
            #print(child)
            temp_map = vector2map(child)
            mapV = change_map(temp_map)
            maps.append([seq, evaluator(mapV)])
        
        maps = sorted(maps, key=itemgetter(1))
        maps.reverse()
        #do selection
        selected_children = selection(maps) 
        generation_count += 1

    #Final result
    print("=========================== MAP VECTOR ===========================")
    print(selected_children)
    print(len(selected_children))

    solutionsList = []
    for child in selected_children:
        seq = child[0]
        solutionsList.append(seq)
    
    print("=========================== SOLUTIONS ===========================")
    print("Number of Solutions Found: ", len(solutionsList))
    print("Number of Generations: ", generation)
     
    for seq in solutionsList:
        print(seq)
        temp_map = vector2map(seq)
        mapV = change_map(temp_map)
        print(evaluator(mapV))
        print("=====================") 


print("Implementing CMS-ES to Doom Map Generation")
## Create a vector of 5 health pack points and 15 wall points
# mapVector = [x_health, y_health, ..., x_wall, y_wall, angled]
mapVector = []
theMap = np.zeros((10, 10))
# find random points for 5 health packs
ct = 0
while ct < 5:
    x = random.randint(1, max_num)
    y = random.randint(1, max_num)
    mapVector.append(x)
    mapVector.append(y)
    theMap[y][x] = 2
    ct = ct + 1
# add 15 random wall points and direction
# 0 = up
# 1 = right
# 0.5 = angled up right for 45 degrees
direction = [0, 1, 0.5] 
ct = 0
while ct < 15:
    x = random.randint(1, max_num)
    y = random.randint(1, max_num)
    angle = random.randint(0, 1)
    mapVector.append(x)
    mapVector.append(y)
    mapVector.append(angle)
    theMap[y][x] = 1
    ct = ct + 1

evolution(mapVector)
