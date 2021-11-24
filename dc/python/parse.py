import os
from pyparsing import *

netlist = open(os.getcwd() + "/outputs/flat_syn.v", "r")
connectivity = open(os.getcwd() + "/outputs/netlist_parsed.txt", "w")

line = netlist.readline()

chunk = []
WIREFLAG = False

parentheses = Word('(' + ')')
wire = Word('\\' + alphanums + '/' + '_')
parsing = parentheses + wire('wire') + parentheses





# 앞에 쓸데 없는 line 제거, module 부터 읽도록
for n in range(6):
    line = netlist.readline()


while True:
    line = netlist.readline().lstrip(" ")

    if not line:
        break

    if "wire" in line:
        WIREFLAG = True

    if WIREFLAG == True and ";" in line:
        WIREFLAG = False
        continue

    if not WIREFLAG:
        chunk += line.rstrip("\n")

        if ";" in line:
            chunk = "".join(chunk)

            if (
                "module" not in chunk
                and "input" not in chunk
                and "output" not in chunk
                and "assign" not in chunk
            ):

                subchunk = chunk.split(' ')

                

                cellType = subchunk[0]
                instance = subchunk[1]

                connectivity.write(cellType + ' ' + instance + ' ')

                subchunk = chunk.split('.')

                for fn,s,e in parsing.scanString(chunk):
                    connectivity.write(fn.wire + ' ')

                connectivity.write('\n')





            chunk = []

netlist.close()
connectivity.close()
