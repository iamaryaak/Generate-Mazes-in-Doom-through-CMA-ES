import numpy as np
from matplotlib import *
import cma
import random
import os

## Functions
def print_map(board):
	# Print the rows
	for r in board:
		#print(r)
		rowprint = ""
		for c in r:
			if c == WALL:
				rowprint = rowprint + "X"
			elif c == EMPTY:
				rowprint = rowprint + " "
			elif c == HP:
                                rowprint = rowprint + "H"
			
		print(rowprint)

print("Implementing CMS-ES to Doom Map Generation")
WALL = 1
EMPTY = 0
HP = 2

## Create a vector of 5 health pack points and 15 wall points
# mapVector = [x_health, y_health, ..., x_wall, y_wall, angled]
mapVector = []

# find random points for 5 health packs
ct = 0
while ct < 5:
    x = random.randint(1, 13)
    y = random.randint(1, 13)
    mapVector.append(x)
    mapVector.append(y)
    ct = ct + 1
# add 15 random wall points and direction
# 0 = up
# 1 = right
# 0.5 = angled up right for 45 degrees
direction = [0, 1, 0.5] 
ct = 0
while ct < 15:
    x = random.randint(1, 13)
    y = random.randint(1, 13)
    angle = random.randint(0, 1)
    mapVector.append(x)
    mapVector.append(y)
    mapVector.append(angle)
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
## Maps are size of 15 by 15 (set size)

doomMap = [[WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
                [WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
                [WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
                [WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
                [WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL]]
mapCt = 0
angled = []
for seq in solutionsList:
    # set health packs first 5 pairs
    for n in range(len(seq)):
        if n < 10:
            x_health = int(seq[n])
            n = n + 1
            y_health = int(seq[n])
            n = n + 1
            #print((x_health), (y_health))
            doomMap[(x_health)][(y_health)] = HP
        if n < 45:
            x_wall = int(seq[n])
            n = n + 1
            y_wall = int(seq[n])
            n = n + 1
            angle = seq[n]
            angled.append(angle)
            n = n + 1
            #print((x_wall), (y_wall))
            doomMap[(x_wall)][(y_wall)] = WALL
    # check if health pack exists, if it doesn't, add it
    if not any(HP in x for x in doomMap):
        x = random.randint(1, 13)
        y = random.randint(1, 13)
        doomMap[x][y] = HP
    print("=====================")
    print_map(doomMap)
    print("=====================")
