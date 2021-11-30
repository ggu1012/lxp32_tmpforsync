import numpy as np
import json
from random import shuffle

con_file = open('modfiles/connectivity.json', 'r')
mem_file = open('modfiles/memory_level.json', 'w')

connectivity = json.load(con_file)

cells = list(connectivity.keys())

# Find starting points - memory macros
start = []
for cell in cells:
    if 'sram' in cell:
        start.append(cell)

memory_level = dict()


for cell in cells:
    memory_level[cell] = [-1 for n in range(len(start))]

for idx, cell in enumerate(start):

    stack = np.array([cell])

    level = 0
    while stack.size != len(connectivity):
        
        if stack.size >= len(connectivity):
            print(stack.size)
                
        stack_new = []
        for cell in stack:
            memory_level[cell][idx] = level
            neighbor = np.array(connectivity[cell])

            for one in neighbor:
                if memory_level[one][idx] != -1:
                    neighbor = np.delete(neighbor, np.where(neighbor == one))

            neighbor = np.unique(neighbor)
            stack_new = np.append(stack_new, neighbor)

        level += 1

        stack = stack_new


    # stack = np.append([], connectivity[cell])
    # memory_level[cell] = [0 for n in range(len(start))] 

    # # DFS
    # while len(stack) != 0:
    #     tail, stack = stack[-1], stack[:-1]

    #     # Skip the node that already been visited
    #     if memory_level[tail][idx] != -1:
    #         continue
                
    #     lowest = 1000000 # arbitrary large num
    #     for neighbor in connectivity[tail]:
    #         if memory_level[neighbor][idx] == -1:
    #             continue
    #         lowest = memory_level[neighbor][idx] if memory_level[neighbor][idx] <= lowest \
    #             else lowest

    #     memory_level[tail][idx] = lowest + 1

    #     shuffle(connectivity[tail])
    #     stack = np.append(stack, connectivity[tail])

mem_file.write(json.dumps(memory_level))

con_file.close()
mem_file.close()






        

