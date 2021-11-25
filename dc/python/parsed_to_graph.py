import os
from pyparsing import *
import json


parsed = open(os.getcwd() + "/outputs/syn.sdf", "r")
connectivity = open(os.getcwd() + '/modfiles/connectivity.json', 'w')
tmp = open(os.getcwd() + '/modfiles/connectivity_list.text', 'w')


nodes = dict()
interconnect_section = 0
already_in = 0

while True:
    line = parsed.readline().strip(' ').strip('\n')

    if line =='':
        print('x')

    if 'INTERCONNECT' in line:
        
        line = line.replace('\\', '')
        # INTERCONNECT, (timing 정보) 버림
        chunk = line.split(' ')[1:-1] 

        first = chunk[0].split('/')
        if len(first) != 1:
            first = first[:-1]
        first_united = '/'.join(first)

        already_in = 1 if first_united in nodes else 0

        for elem in chunk[1:]:
            elem_split_by_slash = elem.split('/')
            if len(elem_split_by_slash) != 1:
                elem_split_by_slash = elem_split_by_slash[:-1]
                elem_united = '/'.join(elem_split_by_slash)

            if already_in:               
                nodes[first_united].append(elem_united)
            else:
                nodes[first_united] = [elem_united]

        interconnect_section = 1

    if interconnect_section and (line == ')'):

        
        ## debug
        for node in nodes:
            tmp.write(node + '     ')
            
            for elem in nodes[node]:
                tmp.write(elem + ' ')

            tmp.write('\n')
        ##



        connectivity.write(json.dumps(nodes))
        break

parsed.close()
tmp.close()
connectivity.close()
