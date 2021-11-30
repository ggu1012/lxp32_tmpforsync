import os
from pyparsing import *
import json

def remove_cell_port(cell):
    '''
    ex) cpu_inst/U1111/Y ==> cpu_inst/U1111
    '''

    cell = cell.split('/')
    if len(cell) != 1:
        cell = cell[:-1]   

    return '/'.join(cell)


parsed = open(os.getcwd() + "/outputs/syn.sdf", "r")
connectivity = open(os.getcwd() + '/modfiles/connectivity.json', 'w')
tmp = open(os.getcwd() + '/modfiles/connectivity_list.text', 'w')


nodes = dict()
interconnect_section = 0
already_in = 0

inout = [
       	'clk_i',
		'rst_i',
		
		'ibus_cyc_o',
		'ibus_stb_o',
		'ibus_cti_o',
		'ibus_bte_o',
		'ibus_ack_i',
		'ibus_adr_o',
		'ibus_dat_i',
		
		'dbus_cyc_o',
		'dbus_stb_',
		'dbus_we_o',
		'dbus_sel_o',
		'dbus_ack_i',
		'dbus_adr_o',
		'dbus_dat_o',
		'dbus_dat_i',
		
		'irq_i'
]



while True:
    line = parsed.readline().strip(' ').strip('\n')

    if 'INTERCONNECT' in line:
        
        line = line.replace('\\', '')
        # INTERCONNECT, (timing 정보) 버림
        chunk = line.split(' ')[1:-1] 


        first_cell = chunk[0]
        second_cell = chunk[1]

        first_cell = remove_cell_port(first_cell)
        second_cell = remove_cell_port(second_cell)

        avoidflag = 0
        for avoid in inout:
            if avoid in first_cell or avoid in second_cell:
                avoidflag = 1
                continue

        if avoidflag:
            continue

        first_already_in = True if first_cell in nodes else False
        second_already_in = True if second_cell in nodes else False

        
        if first_already_in is True:
            nodes[first_cell].append(second_cell)            
        else:
            nodes[first_cell] = [second_cell]
    
    
        if second_already_in is True:
            nodes[second_cell].append(first_cell)
        else:
            nodes[second_cell] = [first_cell]

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



