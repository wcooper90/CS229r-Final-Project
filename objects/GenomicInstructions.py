import random
from .AuxFunctions.instructions import *
from .AuxFunctions.nop_instructions import *

class GenomicInstructions:

    def __init__(self):
        self.instruction_set = [inc, nand, nopA, nopB, nopC, if_n_equ, if_less,
                                pop, push, swap_stk, swap, shift_l, shift_r,
                                sub, dec, add, IO, h_alloc, h_divide,
                                h_copy, h_search, mov_head, jmp_head, get_head,
                                if_label, set_flow]


    def generate_random_initial_instructions(self, genome_length):
        genome_sequence = []
        for i in range(genome_length):
            genome_sequence.append(self.instruction_set[random.randint(0, 25)])
        return genome_sequence


    def generate_test_initial_instructions(self, genome_length):
        genome_sequence = []
        for i in range(genome_length):
            genome_sequence.append(self.instruction_set[0])
        return genome_sequence
