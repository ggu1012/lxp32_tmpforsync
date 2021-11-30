import numpy as np
import json

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


# BFS
for idx, cell in enumerate(start):

    stack = np.array([cell], dtype=object)

    level = 0
    visited = np.array([], dtype=object)

    while visited.size != len(connectivity):        

        stack_new = []

        for cell in stack:
            if cell in visited:
                stack = np.delete(stack, np.where(stack == cell))

        visited = np.append(visited, stack)

        for cell in stack:
            memory_level[cell][idx] = level
            neighbor = np.array(connectivity[cell], dtype=object)

            for one in neighbor:
                 if memory_level[one][idx] != -1:
                    neighbor = np.delete(neighbor, np.where(neighbor == one))

            stack_new = np.unique(np.append(stack_new, neighbor))

        level += 1

        stack = stack_new


mem_file.write(json.dumps(memory_level))

con_file.close()
mem_file.close()






        

