from .instructions import *
from .nop_instructions import *
import random

nops = [nopA, nopB, nopC]
complements = {nopA: nopB, nopB: nopC, nopC: nopA}

# look ahead in the instruction set of the given Avidian to see if there's a nop that effects the current instruction 
def check_nop(avidian, instruction):
    # set_flow has a different default register than the others
    register = avidian.register_B
    if instruction == 'set_flow':
        register = avidian.register_C

    # default head is instruction pointer
    head = 'IP'

    pointer = avidian.instruction_pointer
    pointer += 1
    # wrap around if necessary
    if pointer == len(avidian.genome):
        pointer = 0

    if avidian.genome[pointer] == nopA:
        register = avidian.register_A
        head = 'IP'
    elif avidian.genome[pointer] == nopB:
        register = avidian.register_B
        head = 'RH'
    elif avidian.genome[pointer] == nopC:
        register = avidian.register_C
        head = 'WH'
        
    return register, head

def check_template(avidian):
    pointer = avidian.instruction_pointer
    pointer += 1
    if pointer == len(avidian.genome):
        pointer = 0
    complement = []
    if avidian.genome[pointer] not in nops:
        return []
    while avidian.genome[pointer] in nops:
        complement.append(complements[avidian.genome[pointer]])
        pointer += 1
        if pointer == len(avidian.genome):
            pointer = 0
    return complement

def find_complement(avidian, complement):
    stop = avidian.instruction_pointer
    pointer = stop + 1
    if pointer == len(avidian.genome):
        pointer = 0
    tmp = []
    distance = 1
    while pointer != stop:
        if avidian.genome[pointer] in nops:
            beginning = pointer
            tmp.append(complements[avidian.genome[pointer]])
            if tmp == complement:
                avidian.flow_head = beginning
                avidian.register_B.val = format(distance, 'b').zfill(32)
                avidian.register_C.val = format(len(complement), 'b').zfill(32)
                return
        else:
            tmp = []
        pointer += 1
        distance += 1
        if pointer == len(avidian.genome):
            pointer = 0
    avidian.register_B.val = '0' * 32
    avidian.register_C.val = '0' * 32
    avidian.flow_head = stop + 1
    return


# input of binary string, standardizes it to the correct length
def standardize_register_value_length(val, register_length):

    # temporary fix, because sometimes the incoming value will be a negative binary number
    if val[0] == "-":
        val = val[1:]

    # if binary string is too larger for the register, truncate the right side
    # TODO; figure out a better mechanism for this?
    if len(val) > register_length:
        return val[:register_length]

    # otherwise, pad the left size with zeros
    else:
        zeros = register_length - len(val)
        appended = ""
        for z in range(zeros):
            appended += "0"
        return appended + val