import random
from .AuxFunctions.instructions import *
from .AuxFunctions.nop_instructions import *


# class to generate initial genomic sequences for Avidians
class GenomicInstructions:

    def __init__(self):
        self.instruction_set = [h_alloc, h_copy, h_divide, nopC, nopA, nopB, if_n_equ, if_less,
                                pop, push, swap_stk, swap, shift_l, shift_r,
                                sub, dec, add, IO,  inc, nand,
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
        for i in range(genome_length // 2):
            genome_sequence.append(nand)
            genome_sequence.append(IO)
        return genome_sequence


    # generate instructions selecting based on instruction weights
    def generate_weighted_initial_instructions(self, genome_length, weights):
        assert(len(weights) == 26)
        pass


    # return hand-crafted ancestral genome, consisting only of replication and nop operations
    def generate_ancestral_instructions(self, genome_length):
        genome_sequence = []

        # only iterate for genome_length - 3 because we append the 3 replication instructions at the end
        for i in range(genome_length - 6):
            # index 3 is the nopC command, as specified by the Lenski paper
            genome_sequence.append(nopC)

        genome_sequence = [h_alloc, h_copy, h_divide] + genome_sequence + [h_alloc, h_copy, h_divide]
        return genome_sequence
