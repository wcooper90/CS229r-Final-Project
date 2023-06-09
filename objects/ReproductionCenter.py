from .Avidian import Avidian
from .ReproductionTypeEnum import REPRODUCTION_TYPE
from .config import CONFIGURATION
from .AuxFunctions.instructions import *
from .AuxFunctions.nop_instructions import *
import random


"""
Object to synthesize reproduction data from avidiands --
Creates new avidian objects
"""
class ReproductionCenter():
    # initialize with reproduction type
    def __init__(self, reproduction_type):
        self.reproduction_type = reproduction_type
        self.config = CONFIGURATION()
        self.instruction_set = [h_copy, inc, nand, nopA, nopB, nopC, if_n_equ, if_less,
                                pop, push, swap_stk, swap, shift_l, shift_r,
                                sub, dec, add, IO, h_alloc, h_divide,
                                h_search, mov_head, jmp_head, get_head,
                                if_label, set_flow]

    # main handler
    def process(self, new_avidians_info, vCPU, time):
        if self.reproduction_type == REPRODUCTION_TYPE(1):
            return self._process_asexual(new_avidians_info, vCPU, time)
        elif self.reproduction_type == REPRODUCTION_TYPE(2):
            return self._process_sexual_no_sexes(new_avidians_info, vCPU, time)
        else:
            return self._process_sexual_with_sexes(new_avidians_info, vCPU, time)


    # create new avidians asexually
    def _process_asexual(self, new_avidians_info, vCPU, time):
        new_avidians = []
        for values in new_avidians_info:
            # mutate genome
            mutated_genome = self._mutate_genome(values[0])
            # create new object
            new_avidian_object = Avidian(vCPU.num_avidians, mutated_genome, values[1], self.reproduction_type, (values[3]), time, values[4])
            new_avidians.append(new_avidian_object)
            vCPU.num_avidians += 1
        # return the list of new avidian objects and an empty list, because in asexual reproduction
        # we immediately process all children
        return new_avidians, []


    # create new avidians sexually, sexes of the parents do not matter
    def _process_sexual_no_sexes(self, new_avidians_info, vCPU, time):
        new_avidians = []
        compatible = []
        counter = 0
        while counter < len(new_avidians_info):
            if len(compatible) == 1:
                # if there is a compatible partner, combine genomes, mutate, and create child obejct
                new_genome = self._combine_genomes(new_avidians_info[counter][0], compatible[0][0])
                generation = min(new_avidians_info[counter][4], compatible[0][4])
                mutated_genome = self._mutate_genome(new_genome)
                new_avidian_object = Avidian(vCPU.num_avidians, mutated_genome, new_avidians_info[counter][1],
                                                self.reproduction_type, (new_avidians_info[counter][3], compatible[0][3]), time, generation)
                new_avidians.append(new_avidian_object)
                vCPU.num_avidians += 1
                compatible = []
            else:
                compatible.append(new_avidians_info[counter])

            counter += 1

        # return the list of new avidian objects and the leftover genomes, to be used in next iteration
        return new_avidians, compatible


    # create new avidians sexually, sexes of the parents do now must be compatible
    def _process_sexual_with_sexes(self, new_avidians_info, vCPU, time):
        new_avidians = []
        compatible = []
        counter = 0
        while counter < len(new_avidians_info):
            new_genome = None
            generation = None
            if len(compatible) > 0:
                # if we find a match, delete compatible flag will be set to True and corresponding object will be removed from compatible list
                delete_compatible_object_flag = False
                delete_object_idx = None
                for i, values in enumerate(compatible):
                    if new_avidians_info[counter][2] == 'M' and values[2] == 'F':
                        new_genome = self._combine_genomes(new_avidians_info[counter][0], compatible[0][0])
                        generation = min(new_avidians_info[counter][4], compatible[0][4])
                        delete_compatible_object_flag = True
                        delete_object_idx = i
                        break
                    elif new_avidians_info[counter][2] == 'F' and values[2] == 'M':
                        new_genome = self._combine_genomes(new_avidians_info[counter][0], compatible[0][0])
                        generation = min(new_avidians_info[counter][4], compatible[0][4])
                        delete_compatible_object_flag = True
                        delete_object_idx = i
                        break

                # delete object if it's been matched, mutate genome, create new opject, and udpate avidian counter
                if delete_compatible_object_flag:
                    mutated_genome = self._mutate_genome(new_genome)
                    new_avidian_object = Avidian(vCPU.num_avidians, mutated_genome, values[1],
                                                    self.reproduction_type, (new_avidians_info[counter][3], compatible[i][3]), time, generation)
                    new_avidians.append(new_avidian_object)
                    del compatible[delete_object_idx]
                    vCPU.num_avidians += 1

                # if there's no match, put this specimen back into compatible list
                else:
                    compatible.append(new_avidians_info[counter])

            # if there's no one in the compatible list yet, put this specimen into compatible list
            else:
                compatible.append(new_avidians_info[counter])

            # udpate counter
            counter += 1

        # return the list of new avidian objects and the leftover genomes, to be used in next iteration
        return new_avidians, compatible


    # mutate genome according to config variables
    def _mutate_genome(self, genome):

        # for each instruction, small probability of error in copy
        for i in range(len(genome)):
            rand = random.random()
            if rand < self.config.mutation_error_rate_per_instruction:
                genome[i] = self.instruction_set[random.randint(0, 25)]

        # for each genome, small probability of a deletion or insertion
        if random.random() < self.config.single_instruction_insertion_or_deletion_rate:
            # 50% chance of deleting a random instruction
            if random.random() <= 0.5:
                del genome[random.randint(0, len(genome) - 1)]
            # 50% chance of inserting a new random instruction at a random point
            else:
                genome.insert(random.randint(0, len(genome)), self.instruction_set[random.randint(0, 25)])

        return genome


    # combine genomes of two sexually reproducing avidians randomly
    # one-point crossover
    def _combine_genomes(self, genome1, genome2):
        combined_genome = None
        genome1_length, genome2_length = len(genome1), len(genome2)

        # randomly rotate both genomes
        pivot1 = random.randint(0, genome1_length)
        pivot2 = random.randint(0, genome2_length)
        genome1 = genome1[pivot1:] + genome1[:pivot1]
        genome2 = genome2[pivot2:] + genome2[:pivot2]


        # if genome lengths are uneven, change them to the nearest even number with equal probability 
        if genome1_length % 2 == 1:
            if random.random() < 0.5:
                genome1_length += 1
            else:
                genome1_length -= 1
        if genome2_length % 2 == 1:
            if random.random() < 0.5:
                genome2_length += 1
            else:
                genome2_length -= 1

        # cut each parent genome to maintain about half of its instructions
        # this integer division may be causing a decrease in average genome length
        genome1_new_length = random.randint(genome1_length // 2 - self.config.genome_length_variability + 1, genome1_length // 2 + self.config.genome_length_variability)
        genome1 = genome1[:genome1_new_length]
        genome2_new_length = random.randint(genome2_length // 2 - self.config.genome_length_variability + 1, genome2_length // 2 + self.config.genome_length_variability)
        genome2 = genome2[:genome2_new_length]

        # randomly select order in which genomes are combined
        if random.random() < 0.5:
            combined_genome = genome1 + genome2
        else:
            combined_genome = genome2 + genome1

        # return out
        return combined_genome
