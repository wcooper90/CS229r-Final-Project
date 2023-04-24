import sys
from pathlib import Path
import os
# set path to parent directory to be able to import instruction functions
sys.path.append(Path().parent)
from objects.AuxFunctions.instructions import *
from objects.AuxFunctions.logic_operators import *




def print_stats(vCPU, avidians):
    print("Total number of Avidians: " + str(len(avidians)))
    alive_avidians = [avidian for avidian in avidians if avidian.is_alive]
    print("Number of alive Avidians: " + str(len(alive_avidians)))
    avidians_with_complex_functions = []
    lengths_of_genomes = []
    healthy_avidians = 0
    complex_operand_avidians = {"not_": 0, "nand_": 0, "and_": 0,
                                    "or_n_":0, "or_": 0, "and_n_":0,
                                    "nor_": 0, "xor_": 0, "equ_": 0}
    for avidian in alive_avidians:
        if avidian.operands_achieved:
            avidians_with_complex_functions.append(str(avidian.id))
            for op in avidian.operands_achieved:
                if op == not_:
                    complex_operand_avidians["not_"] += 1
                elif op == nand_:
                    complex_operand_avidians["nand_"] += 1
                elif op == nor_:
                    complex_operand_avidians["nor_"] += 1
                elif op == xor_:
                    complex_operand_avidians["xor_"] += 1
                elif op == and_n_:
                    complex_operand_avidians["and_n_"] += 1
                elif op == or_:
                    complex_operand_avidians["or_"] += 1
                elif op == or_n_:
                    complex_operand_avidians["or_n_"] += 1
                elif op == equ_:
                    complex_operand_avidians["equ_"] += 1
                elif op == and_:
                    complex_operand_avidians["and_"] += 1


        lengths_of_genomes.append(len(avidian.genome))
        if h_alloc in avidian.genome and h_copy in avidian.genome and h_divide in avidian.genome and avidian.is_alive:
            healthy_avidians += 1
    try:
        print("The average genome length of alive avidians is: " + str(sum(lengths_of_genomes) / len(lengths_of_genomes)))
    except:
        # no avidians are alive to have their genome lengths measured
        pass
    print("Number of alive avidians that have evolved complex functions: " + str(len(avidians_with_complex_functions)))
    print(complex_operand_avidians)
    print("Number of alive avidians that can reproduce is: " + str(healthy_avidians))