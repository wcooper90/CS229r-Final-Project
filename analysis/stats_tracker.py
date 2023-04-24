import sys
from pathlib import Path
import os
# set path to parent directory to be able to import instruction functions
sys.path.append(Path().parent)
from objects.AuxFunctions.instructions import *



def print_stats(vCPU, avidians):
    print("Total number of Avidians: " + str(len(avidians)))
    alive_avidians = [avidian for avidian in avidians if avidian.is_alive]
    print("Number of alive Avidians: " + str(len(alive_avidians)))
    avidians_with_complex_functions = []
    lengths_of_genomes = []
    healthy_avidians = 0
    for avidian in alive_avidians:
        if avidian.operands_achieved:
            avidians_with_complex_functions.append(str(avidian.id))
        lengths_of_genomes.append(len(avidian.genome))
        if h_alloc in avidian.genome and h_copy in avidian.genome and h_divide in avidian.genome and avidian.is_alive:
            healthy_avidians += 1
    try:
        print("The average genome length is: " + str(sum(lengths_of_genomes) / len(lengths_of_genomes)))
    except:
        # no avidians are alive to have their genome lengths measured
        pass
    print("Number of alive avidians that have evolved complex functions: " + str(len(avidians_with_complex_functions)))
    print("Number of alive avidians that can reproduce is: " + str(healthy_avidians))
