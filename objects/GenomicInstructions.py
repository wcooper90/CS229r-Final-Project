import random
from .AuxFunctions.instructions import *
from .AuxFunctions.nop_instructions import *


# class to generate initial genomic sequences for Avidians
class GenomicInstructions:

    def __init__(self):
        self.instruction_set = [h_copy, inc, nand, nopA, nopB, nopC, if_n_equ, if_less,
                                pop, push, swap_stk, swap, shift_l, shift_r,
                                sub, dec, add, IO, h_alloc, h_divide,
                                h_search, mov_head, jmp_head, get_head,
                                if_label, set_flow]


    # generate totally random instructions
    def generate_random_initial_instructions(self, genome_length):
        genome_sequence = []
        for i in range(genome_length):
            genome_sequence.append(self.instruction_set[random.randint(0, 25)])
        return genome_sequence


    # generate only instructions of a particular type
    def generate_test_initial_instructions(self, genome_length):
        genome_sequence = []
        for i in range(genome_length):
            genome_sequence.append(self.instruction_set[0])
        return genome_sequence


    # generate instructions selecting based on instruction weights
    def generate_weighted_initial_instructions(self, genome_length, weights):
        assert(len(weights) == 26)
        pass 
