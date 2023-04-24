from .instructions import *
from .nop_instructions import *
import random


def check_nop(avidian):
    register = avidian.register_B
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
