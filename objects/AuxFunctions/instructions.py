import random
from .helpers import *


# nand logical operator, only logical operator as a genome instruction
def nand(avidian):
    # check for nops
    register, _ = check_nop(avidian)
    out = ""
    for i in range(len(avidian.register_A)):
        b = avidian.register_B.val[i]
        c = avidian.register_C.val[i]
        # bitwise nand operation
        if b and c == '1':
            out += '0'
        else:
            out += '1'
    register = out


def if_n_equ(avidian):
    pass


# if b is larger than its complement, skip the next instruction
def if_less(avidian):
    b_complement = ""
    for i in range(avidian.config.register_length):
        b_complement += '0' if avidian.register_B.val[i] == 1 else '1'

    b_complement_int = int(b_complement, 2)
    b = int(avidian.register_B.val, 2)
    if b >= b_complement_int:
        avidian.instruction_pointer += 1


# pop content from active stack to specified register
def pop(avidian):

    # calculate appropiate register
    register, _ = check_nop(avidian)

    if avidian.active_stack == 1:
        try:
            register.val = avidian.stack_1.pop()
        except:
            # stack was empty
            pass
    else:
        try:
            register.val = avidian.stack_2.pop()
        except:
            # stack was empty
            pass


# push contents of BX register into active stack
def push(avidian):
    # calculate appropiate register
    register, _ = check_nop(avidian)

    if avidian.active_stack == 1:
        avidian.stack_1.append(register.val)
    else:
        avidian.stack_2.append(register.val)


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
    for i in range(avidian.config.register_length):
        register.val[i] = '0' if register.val[i] == 1 else '1'


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

    # remove later
    print(len(register.val))


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

    # remove later
    print(len(register.val))


# increments specified register's value by 1
def inc(avidian):
    register, _ = check_nop(avidian)
    # convert to int, add 1, convert back to binary and standardize
    register.val = standarize_register_value_length('{0:b}'.format(int(register.val, 2) + 1), avidian.config.register_length)


# add values of B and C and put sum into specified register
def add(avidian):
    # pick appropriate register
    register, _ = check_nop(avidian)
    # register values as integers
    b, c = int(avidian.register_B.val, 2), int(avidian.register_C.val, 2)
    # add values and update new register's value
    register.val = standarize_register_value_length('{0:b}'.format(b + c), avidian.config.register_length)

# decrements specified register's value by 1
def dec(avidian):
    register, _ = check_nop(avidian)
    # convert to int, subtract 1, convert back to binary and standardize
    register.val = standarize_register_value_length('{0:b}'.format(int(register.val, 2) - 1), avidian.config.register_length)


# subtract register c value from register b value and input into specified register
def sub(avidian):
    # check for output register
    register, _ = check_nop(avidian)
    # subtraction
    b, c = int(avidian.register_B.val, 2), int(avidian.register_C.val, 2)
    # standardize length of this integer output
    out = standarize_register_value_length('{0:b}'.format(b - c), avidian.config.register_length)
    # update register value
    register.val = out


# return BX, generate a new input from environment to go into BX
def IO(avidian):
    # check which register to operate on
    register, _ = check_nop(avidian)
    # set return to correct register contents
    out = register.val
    # register is now replaced with the next environment variable in line
    register.val = avidian.env_input_1
    # The SharedCPU object will check for this output and update new environment variables correspondingly
    return out

def h_alloc(avidian):
    pass

def h_divide(avidian):
    pass

def h_copy(avidian):
    pass

def h_search(avidian):
    pass


# move instruction pointer to where flow head is pointing
def mov_head(avidian):
    avidian.instruction_pointer = avidian.flow_head


# move specified pointer forward to another spot in memory according to contents of CX
def jmp_head(avidian):
    # check for nops, update returned pointer
    _, head = check_nop(avidian)

    # calculate integer value for c
    c = int(avidian.register_C, 2)

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


def get_head(avidian):
    pass


# finished producing off spring?
def if_label(avidian):
    pass


# moves flow head to point at instruction denoted by specified register
def set_flow(avidian):
    # calculate appropriate register
    register, _ = check_nop(avidian)

    # wrap around if longer than current genome
    val = int(register.val, 2) % len(avidian.genome)
    avidian.flow_head = val
