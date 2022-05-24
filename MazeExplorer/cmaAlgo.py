import numpy as np
from matplotlib import *
import cma
import random
import os
from collections import Counter
import itertools
from operator import itemgetter



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
    for ele in range(1, len(map)-1):
        for element in range(1, len(map[ele])-1):
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

print("Implementing CMS-ES to Doom Map Generation")
WALL = 1
WALL1 = 3
EMPTY = 0
HP = 2
max_num = 9
maps = []

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


## Standardize the vector
# zi = (xi – min(x)) / (max(x) – min(x))
standardVector = []
minVectorValue = min(mapVector)
maxVectorValue = max(mapVector)
for n in mapVector:
    num = n - minVectorValue
    deno = maxVectorValue - minVectorValue
    ans = num / deno
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
print("=========================== MAP VECTOR ===========================")
solutions = es.ask()
print(solutions)

# x1 = (zi * (max(x) - min(x))) + min(x)
solutionsNormal = []
for seq in solutions:
    seqNormal = []
    for n in seq:
        res = (n * (maxVectorValue - minVectorValue)) + minVectorValue
        seqNormal.append(res)
    solutionsNormal.append(seqNormal)

print("=========================== SOLUTIONS ===========================")
#for s in solutionsNormal:
    #print(s)

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
mapCT = 0
wallCt = 0
for seq in solutionsList:
    angled = []
    # set health packs first 5 pairs
    for n in range(len(seq)):
        if n < 10:
            x_health = int(seq[n])
            n = n + 1
            y_health = int(seq[n])
            n = n + 1
            #print((x_health), (y_health))
            if doomMap[(x_health)][(y_health)] != WALL:
                    doomMap[(x_health)][(y_health)] = HP
        if n < 45:
            x_wall = int(seq[n])
            n = n + 1
            y_wall = int(seq[n])
            n = n + 1
            angle = seq[n]
            #print(angle)
            angled.append(angle)
            n = n + 1
            #print((x_wall), (y_wall))
            doomMap[(x_wall)][(y_wall)] = WALL
    # add wall and angle to txt files so we can use them to create .WAD files
    wallCt = wallCt + 1
    # fileoutput = "my_maze_inputs/wallList_" + str(wallCt) + ".txt"
    # with open(fileoutput, 'w') as f:
    #     str1 = " ".join(str(e) for e in angled)
    #     f.write(str1)
    #     f.close()
    #     print(fileoutput, " is created!")
    # check if health pack exists, if it doesn't, add it
    if not any(HP in x for x in doomMap):
        x = random.randint(1, max_num)
        y = random.randint(1, max_num)
        if doomMap[x][y] != WALL:
                doomMap[x][y] = HP
        else:
                while doomMap[x][y] != WALL:
                        x = random.randint(1, max_num)
                        y = random.randint(1, max_num)
                doomMap[x][y] = HP
    print("=====================")
    mapV = change_map(doomMap)
    #evaluator(mapV)
    maps.append([seq, evaluator(mapV)])
    #print(maps)
    #print()
    maps = sorted(maps, key=itemgetter(1))
    #print(maps)
    print("=====================")
    
def ES(maps, parents): 
    result = []
    solution = []
    tmp = []
    while len(tmp) < parents: 
        tmp.append(maps.pop())
    print(tmp)
    for m in tmp: 
        es = cma.CMAEvolutionStrategy(x0, sigma0)
        solutions.append(es.ask())
        print("sol: ", solutions)
    solutionsNormal = []
    for solution in solutions: 
        for seq in solution:
            seqNormal = []
            for n in seq:
                res = (n * (maxVectorValue - minVectorValue)) + minVectorValue
                seqNormal.append(res)
            solutionsNormal.append(seqNormal)
    
        solutionsList = []
        for s in solutionsNormal:
            sol = []
            for n in s:
                num = round(n, 2)
                sol.append(num)
            solutionsList.append(sol)
    #print(solutionsList)
    print("Number of Solutions Found: ", len(solutionsList))
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
    mapCT = 0
    wallCt = 0
    for seq in solutionsList:
        angled = []
        # set health packs first 5 pairs
        for n in range(len(seq)):
            if n < 10:
                x_health = int(seq[n])
                n = n + 1
                y_health = int(seq[n])
                n = n + 1
                #print((x_health), (y_health))
                if doomMap[(x_health)][(y_health)] != WALL:
                        doomMap[(x_health)][(y_health)] = HP
            if n < 45:
                x_wall = int(seq[n])
                n = n + 1
                y_wall = int(seq[n])
                n = n + 1
                angle = seq[n]
                #print(angle)
                angled.append(angle)
                n = n + 1
                #print((x_wall), (y_wall))
                doomMap[(x_wall)][(y_wall)] = WALL
        wallCt = wallCt + 1
        if not any(HP in x for x in doomMap):
            x = random.randint(1, max_num)
            y = random.randint(1, max_num)
            if doomMap[x][y] != WALL:
                    doomMap[x][y] = HP
            else:
                    while doomMap[x][y] != WALL:
                            x = random.randint(1, max_num)
                            y = random.randint(1, max_num)
                    doomMap[x][y] = HP
                    
        mapV = change_map(doomMap)
        
        result.append([seq, evaluator(mapV)])
        #print(maps)
        #print()
        result = sorted(maps, key=itemgetter(1))
    return result

count = 10
n = 0
while n < count:    
    maps = ES(maps, 2)

    
#     fileoutput = "my_maze_inputs/doomMap_" + str(mapCT) + ".txt"
#     # ignore healthpacks for now...
#     with open(fileoutput, 'w') as f:
#         for row in doomMap:
#             rowprint = ""
#             for c in row:
#                 if c == WALL:
#                     rowprint = rowprint + "X"
#                 #elif c == HP:
#                     #rowprint = rowprint + " "
#                 else:
#                     rowprint = rowprint + " "
#             f.write(rowprint)
#             f.write("\n")
#         f.close()
#         print(fileoutput, " is created!")
#     mapCT = mapCT + 1
    # print("=====================")
    # print_map(doomMap)
    # print(evaluator(doomMap))
    # print("=====================")

# print("All .txt files have been created")


