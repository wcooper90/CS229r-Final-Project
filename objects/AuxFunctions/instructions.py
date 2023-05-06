import random
from .helpers import *
import sys
from pathlib import Path
import copy
import os
# set path to parent directory to be able to import configuration values
sys.path.append(Path().parent.parent)
from objects.config import CONFIGURATION
from objects.Avidian import Avidian


# nand logical operator, only logical operator as a genome instruction
def nand(avidian):
    # check for nops
    register, _ = check_nop(avidian)
    out = ""
    for i in range(len(avidian.register_A.val)):
        b = avidian.register_B.val[i]
        c = avidian.register_C.val[i]
        # bitwise nand operation
        if b == '1' and c == '1':
            out += '0'
        else:
            out += '1'
    register.val = out


# if specified register's value not equal to its complement, skip the next instruction
def if_n_equ(avidian):
    # find appropriate register
    register, _ = check_nop(avidian)

    # find binary complement
    complement = ""
    for i in range(avidian.config.register_length):
        complement += '0' if register.val[i] == 1 else '1'

    # check for equality
    complement = int(complement, 2)
    val = int(register.val, 2)
    if val != complement:
        avidian.instruction_pointer += 1
        # wrap around genome if necessary
        if avidian.instruction_pointer == len(avidian.genome):
            avidian.instruction_pointer = 0



# if specified register value is larger than its complement, skip the next instruction
def if_less(avidian):
    # find appropriate register
    register, _ = check_nop(avidian)

    # find binary complement
    complement = ""
    for i in range(avidian.config.register_length):
        complement += '0' if register.val[i] == 1 else '1'

    # check for inequality
    complement = int(complement, 2)
    val = int(register.val, 2)
    if val >= complement:
        avidian.instruction_pointer += 1
        # wrap around genome if necessary
        if avidian.instruction_pointer == len(avidian.genome):
            avidian.instruction_pointer = 0


# pop content from active stack to specified register
def pop(avidian):

    # calculate appropiate register
    register, _ = check_nop(avidian)

    if avidian.active_stack == 1:
        try:
            register.val = avidian.stack1.pop()
        except:
            # stack was empty
            pass
    else:
        try:
            register.val = avidian.stack2.pop()
        except:
            # stack was empty
            pass


# push contents of BX register into active stack
def push(avidian):
    # calculate appropiate register
    register, _ = check_nop(avidian)

    if avidian.active_stack == 1:
        avidian.stack1.append(register.val)
    else:
        avidian.stack2.append(register.val)


# switch the active stack
def swap_stk(avidian):
    if avidian.active_stack == 1:
        avidian.active_stack = 2
    else:
        avidian.active_stack = 1


# replace value in specified register with its complement
def swap(avidian):
    # check for corret register
    register, _ = check_nop(avidian)
    complement = ""
    # calculate complement
    for i in range(avidian.config.register_length):
        if register.val[i] == '1':
            complement += '0'
        else:
            complement += '1'
    register.val = complement


# shift bits 1 to the right in specified register
def shift_r(avidian):
    # check for appropriate register
    register, _ = check_nop(avidian)

    # start with 0 as output
    out = "0"
    # copy [:-1] register contents to the rest of new register string
    for i in range(0, avidian.config.register_length - 1):
        out += register.val[i]
    # set val
    register.val = out


# shift bits 1 to the left in specified register
def shift_l(avidian):
    # check for appropriate register
    register, _ = check_nop(avidian)

    # copy [1:] values to new string
    out = ""
    for i in range(1, avidian.config.register_length):
        out += register.val[i]
    # append 0 on the very end
    out += "0"
    register.val = out


# increments specified register's value by 1
def inc(avidian):
    register, _ = check_nop(avidian)
    # convert to int, add 1, convert back to binary and standardize
    register.val = standardize_register_value_length('{0:b}'.format(int(register.val, 2) + 1), avidian.config.register_length)


# add values of B and C and put sum into specified register
def add(avidian):
    # pick appropriate register
    register, _ = check_nop(avidian)
    # register values as integers
    b, c = int(avidian.register_B.val, 2), int(avidian.register_C.val, 2)
    # add values and update new register's value
    register.val = standardize_register_value_length('{0:b}'.format(b + c), avidian.config.register_length)

# decrements specified register's value by 1
def dec(avidian):
    register, _ = check_nop(avidian)
    # convert to int, subtract 1, convert back to binary and standardize
    register.val = standardize_register_value_length('{0:b}'.format(int(register.val, 2) - 1), avidian.config.register_length)


# subtract register c value from register b value and input into specified register
def sub(avidian):
    # check for output register
    register, _ = check_nop(avidian)
    # subtraction
    b, c = int(avidian.register_B.val, 2), int(avidian.register_C.val, 2)
    # standardize length of this integer output
    out = standardize_register_value_length('{0:b}'.format(b - c), avidian.config.register_length)
    # update register value
    register.val = out


# output value from a register, generate a new input from environment to go into the register
def IO(avidian):
    # check which register to operate on
    register, _ = check_nop(avidian)
    # set return to correct register contents
    out = register.val
    # register is now replaced with the next environment variable in line
    register.val = avidian.env_input_1
    # The SharedCPU object will check for this output and update new environment variables correspondingly
    return [out, []]


"""
The following functions use nop templates: h-search, if-label
The following functions are used for repreduction purposes: h-alloc, h-divide, h-copy, h-search

Not totally sure what templates or complement templates are supposed to represent.
Instead of using them, we create a new reproduction mechanism, specific to Python Avidians


- if h_alloc instruction is executed:
    - check to see that Avidian's remaining SIPs are above the threshold for creating offspring
        - set reproduction tag to yes with probability specified in configuration file if so

- if h_divide instruction is executed:
    - check to see if Avidian's child is ready (all genomic instructions copied)
        - if ready, return genomic instructions for new Avidian object

- if h_copy instruction is executed:
    - if reproduction tag is set to true from h_alloc:
        - copy a random chunk approximately half the length of the current genome into genome for child
        - set genomic copy tag to true

if h_search instruction is executed:
    - find the nearest next nop instruction, put distance to this instruction into B register
    - C register will be set to size of continuous sequence of nop instructions
    - flow_head is placed at the beginning of the complement of the nop sequence, if it exists
    - if no template (no nop operations):
        - B and C registers set to 0
        - flow_head placed to current instruction pointer position


if if_label instruction is executed:
    - given that this instruction is usually used to determine if an organism has finished completing offspring,
        we will just have it do nothing for now.

"""


# does nothing for now, usually supposed to do with nop complements
def if_label(avidian):
    pass


# will be implemented with the above description soon, but don't see a real need for it now...
def h_search(avidian):
    pass


# allocates additional memory for organism up to maximum use for its offspring
def h_alloc(avidian):
    # access to config values
    config = CONFIGURATION()

    # if above energy (SIPS) threshold, and passes probability of reproduction threshold, set is_fertile to True
    if avidian.SIPS > config.SIP_reproduction_threshold:
        # if the avidian did not recently have a child
        if avidian.reproduction_cooldown == 0:
            if random.random() > config.probability_of_reproduction:
                avidian.is_fertile = True


# splits off new offspring if child_genome exists, sets parent back to default settings
def h_divide(avidian):
    # if a genome exists for the child, it's ready
    if avidian.child_genome:
        # no register output, but return list of genomic instructions
        child = [[], avidian.child_genome]
        # reset parent attributes
        avidian.child_genome = []
        avidian.is_fertile = False

        # set cooldown
        avidian.reproduction_cooldown = avidian.config.reproduction_cooldown
        return child


# copy genome to child genome
def h_copy(avidian):
    # copy over the genome directly if Avidian is is_fertile
    # Mutations will be handled by the ReproductionCenter object once this copied genome is registered by h_divide
    if avidian.is_fertile:
        avidian.child_genome = copy.copy(avidian.genome)


# move instruction pointer to where flow head is pointing
def mov_head(avidian):
    avidian.instruction_pointer = avidian.flow_head



# move specified pointer forward to another spot in memory according to contents of CX
def jmp_head(avidian):
    # check for nops, update returned pointer
    _, head = check_nop(avidian)

    # calculate integer value for c
    c = int(avidian.register_C.val, 2)

    # depending on if there is a nop operation, change the corresponding head by c
    # the mod function is to wrap the pointer around if the value is too big
    if head == "IP":
        avidian.instruction_pointer += c
        avidian.instruction_pointer %= len(avidian.genome)
    elif head == "RH":
        avidian.read_head += c
        avidian.read_head %= len(avidian.genome)
    else:
        avidian.write_head += c
        avidian.write_head %= len(avidian.genome)


# instruction set was not super clear about this.
# write the position of a specified head into a specified register
def get_head(avidian):
    # find appropriate register
    register, head = check_nop(avidian)

    # find the specified head's value
    head_value = None
    if head == "IP":
        head_value = avidian.instruction_pointer
    elif head == "RH":
        head_value = avidian.read_head
    else:
        head_value = avidian.write_head

    # format and udpate register value
    register.val = standardize_register_value_length('{0:b}'.format(head_value), avidian.config.register_length)


# moves flow head to point at instruction denoted by specified register
def set_flow(avidian):
    # calculate appropriate register
    register, _ = check_nop(avidian)

    # wrap around if longer than current genome
    val = int(register.val, 2) % len(avidian.genome)
    avidian.flow_head = val
