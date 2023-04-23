from .instructions import *
from .nop_instructions import *


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
def standarize_register_value_length(val, register_length):
    # val should not be longer than the register length already
    assert(len(val) <= register_length)
    zeros = register_length - len(val)
    appended = ""
    for z in range(zeros):
        appended += "0"
    return appended + val
