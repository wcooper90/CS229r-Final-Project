import sys
from pathlib import Path
import os
# set path to parent directory to be able to import instruction functions
sys.path.append(Path().parent)
from objects.AuxFunctions.instructions import *
from objects.AuxFunctions.logic_operators import *
from objects.config import CONFIGURATION
import matplotlib.pyplot as plt
import numpy as np


def track_stats(vCPU, avidians, data):
    generations = []
    genome_length = []
    complex_organisms = []
    computational_merit = []
    alive_avidians = 0
    for avidian in avidians:
        if avidian.is_alive:
            alive_avidians += 1
            generations.append(avidian.generation)
            genome_length.append(len(avidian.genome))
            complex_organisms.append(len(avidian.operands_achieved))
            computational_merit.append(avidian.computational_merit)

    if alive_avidians == 0:
        for key in data.keys():
            data[key].append(0)

    else:
        data['avg_genome_length'].append(sum(genome_length) / alive_avidians)
        data['max_genome_length'].append(max(genome_length))
        data['min_genome_length'].append(min(genome_length))
        data['avg_generation'].append(sum(generations) / alive_avidians)
        data['max_generation'].append(max(generations))
        data['min_generation'].append(min(generations))
        data['percent_complex_features'].append(len([x for x in complex_organisms if x > 0]) / alive_avidians)
        data['avg_computational_merit'].append(sum(computational_merit) / alive_avidians)
        data['min_computational_merit'].append(min(computational_merit))
        data['max_computational_merit'].append(max(computational_merit))


def snapshot_plot(vCPU, avidians, time):
    print("Total number of alive Avidians: " + str(len(avidians)))
    alive_avidians = [avidian for avidian in avidians if avidian.is_alive]
    print("Number of alive Avidians: " + str(len(alive_avidians)))
    avidians_with_complex_functions = []
    lengths_of_genomes = []
    healthy_avidians = 0
    complex_operand_avidians = {"not_": 0, "nand_": 0, "and_": 0,
                                    "or_n_":0, "or_": 0, "and_n_":0,
                                    "nor_": 0, "xor_": 0, "equ_": 0}

    num_complex_operands = {1: 0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}

    for avidian in alive_avidians:
        if avidian.operands_achieved:
            avidians_with_complex_functions.append(str(avidian.id))
            num_complex_functions = 0
            for op in avidian.operands_achieved:
                if op == not_:
                    complex_operand_avidians["not_"] += 1
                    num_complex_functions += 1
                elif op == nand_:
                    complex_operand_avidians["nand_"] += 1
                    num_complex_functions += 1
                elif op == nor_:
                    complex_operand_avidians["nor_"] += 1
                    num_complex_functions += 1
                elif op == xor_:
                    complex_operand_avidians["xor_"] += 1
                    num_complex_functions += 1
                elif op == and_n_:
                    complex_operand_avidians["and_n_"] += 1
                    num_complex_functions += 1
                elif op == or_:
                    complex_operand_avidians["or_"] += 1
                    num_complex_functions += 1
                elif op == or_n_:
                    complex_operand_avidians["or_n_"] += 1
                    num_complex_functions += 1
                elif op == equ_:
                    complex_operand_avidians["equ_"] += 1
                    num_complex_functions += 1
                elif op == and_:
                    complex_operand_avidians["and_"] += 1
                    num_complex_functions += 1

            if num_complex_functions > 0:
                num_complex_operands[num_complex_functions] += 1

        lengths_of_genomes.append(len(avidian.genome))
        # ins_hist = [b[1] for b in avidian.instruction_history]
        # if h_alloc in ins_hist and h_copy in ins_hist and h_divide in ins_hist and avidian.is_alive:
        #     healthy_avidians += 1
    try:
        print("The average genome length of alive avidians is: " + str(sum(lengths_of_genomes) / len(lengths_of_genomes)))
    except:
        # no avidians are alive to have their genome lengths measured
        pass
    print("Number of alive avidians that have evolved complex functions: " + str(len(avidians_with_complex_functions)))
    print(complex_operand_avidians)
    # print("Number of alive avidians that can reproduce is: " + str(healthy_avidians))

    # only create the snapshot plots if there are avidians with complex features
    if not all(value == 0 for value in complex_operand_avidians.values()):
        plt.bar(range(len(complex_operand_avidians)), list(complex_operand_avidians.values()), align='center')
        plt.xticks(range(len(complex_operand_avidians)), list(complex_operand_avidians.keys()))
        plt.savefig("analysis/plots/snapshots/snapshot_funcs" + str(time) + ".png")
        plt.clf()

    if not all(value == 0 for value in num_complex_operands.values()):
        plt.bar(range(len(num_complex_operands)), list(num_complex_operands.values()), align='center')
        plt.xticks(range(len(num_complex_operands)), list(num_complex_operands.keys()))
        plt.savefig("analysis/plots/snapshots/snapshot_num_funcs" + str(time) + ".png")
        plt.clf()


def plot(data):
    config = CONFIGURATION()
    xpoints = [int(i) for i in np.arange(0, config.SIMULATION_LENGTH, config.interval)]

    plt.plot(xpoints, data['avg_generation'])
    plt.plot(xpoints, data['min_generation'])
    plt.plot(xpoints, data['max_generation'])
    plt.xlabel('Time Step', fontsize=12)
    plt.ylabel('Generation', fontsize=12)
    plt.legend(['average generation', 'min generation', 'max generation'])
    plt.savefig("analysis/plots/generations.png")
    plt.clf()

    plt.plot(xpoints, data['percent_complex_features'])
    plt.xlabel('Time Step', fontsize=12)
    plt.ylabel('Percentage of Alive Population with Complex Features', fontsize=12)
    plt.savefig("analysis/plots/complex_features.png")
    plt.clf()

    plt.plot(xpoints, data['avg_genome_length'])
    plt.plot(xpoints, data['min_genome_length'])
    plt.plot(xpoints, data['max_genome_length'])
    plt.legend(['average length', 'min length', 'max length'])
    plt.xlabel('Time Step', fontsize=12)
    plt.ylabel('Genome Length', fontsize=12)
    plt.savefig("analysis/plots/genome_length.png")
    plt.clf()

    plt.plot(xpoints, data['avg_computational_merit'])
    plt.plot(xpoints, data['min_computational_merit'])
    plt.plot(xpoints, data['max_computational_merit'])
    plt.legend(['average merit', 'min merit', 'max merit'])
    plt.xlabel('Time Step', fontsize=12)
    plt.ylabel('Computational Merit', fontsize=12)
    plt.savefig("analysis/plots/computational_merit.png")
    plt.clf()
