from collections import Counter
import itertools
'''
XXXXXXXXXXX
X   X  XX X
X   XX    X
X     X   X
XX     XX X
X         X
XX    X XHX
XXXXX   X X
X X X  X  X
X   H     X
XXXXXXXXXXX
'''

map = [['XXXXXXXXXXX'],['X   X     X'],['X         X'],['X     X   X'],['X X X X X X'],['XXXXX X X X'],['XX X XX XHX'],['XXXXX   X X'],['X X X  X  X'],['X   HX  X X'],['XXXXXXXXXXX']]
map = [list(ele[0]) for ele in map]
'''
[['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], 
['X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', 'X'],
['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
['X', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X'], 
['X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X'],
['X', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X', ' ', 'X'],
['X', 'X', ' ', 'X', ' ', 'X', 'X', ' ', 'X', 'H', 'X'], 
['X', 'X', 'X', 'X', 'X', ' ', ' ', ' ', 'X', ' ', 'X'], 
['X', ' ', 'X', ' ', 'X', ' ', ' ', 'X', ' ', ' ', 'X'],
['X', ' ', ' ', ' ', 'H', 'X', ' ', ' ', 'X', ' ', 'X'], 
['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]
'''
print(map)


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
    #print(score)
    return score

evaluator(map)
