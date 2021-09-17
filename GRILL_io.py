
import os
from collections import namedtuple
def read_spectrum(f):
    file_path = os.path.abspath(f)
    file = open(file_path)

    header = file.readline().split()
    print(header)

    spectrum = { h: [] for h in header }

    print(spectrum)

    lines = file.readlines()
    table = []
    for line in lines:
        #print(line)
        table.append(line.split())

    print(len(table))
  

    for row in table:
        for index, (p, item) in enumerate(spectrum.items()):
            #print(p, item, index)
            item.append(float(row[index]))

    return spectrum  