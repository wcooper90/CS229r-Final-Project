from .AuxFunctions.instructions import *


class DebugAvidian:
    # initialize the debugger for the input avidian
    def __init__(self, avidian):
        self.avidian = avidian


    # use all debugging functions at every time step for this Avidian
    def _print_all(self):
        self._print_genome()
        self._print_inputs()
        self._print_stacks()
        self._print_reproductive_capacity()


    # header for other debugging
    def __print_header__(self, title):
        print("*"*20 + "DEBUG " + str(self.avidian.id) + ": " + title + "*"*20)


    # print number of reproductive instructions in genome
    def _print_reproductive_capacity(self):
        self.__print_header__("REPRODUCTIVE CAPACITY")
        allocs, copies, divides = 0, 0, 0
        for instruction in self.avidian.genome:
            if instruction == h_alloc:
                allocs += 1
            elif instruction == h_copy:
                copies += 1
            elif instruction == h_divide:
                divides += 1
        print("allocs, copies, divides: " + str(allocs) + ', ' + str(copies) + ', ' + str(divides))


    # CAN ONLY BE USED WHEN DEBUGGING IS ON
    # prints the most recent instruction history for this debugger
    def _print_instruction_history(self):
        self.__print_header__("INSTRUCTION HISTORY")
        for tup in self.avidian.instruction_history:
            print(tup[1].__name__, tup[0])


    # for debugging with genome
    def _print_genome(self):
        self.__print_header__("GENOME INSTRUCTIONS")
        for func in self.avidian.genome:
            print(func.__name__)

    # for debugging with inputs
    def _print_inputs(self):
        self.__print_header__("ENVIRONMENT INPUTS")
        print(self.avidian.env_input_1)
        print(self.avidian.env_input_2)


    # for debugging with stacks
    def _print_stacks(self):
        self.__print_header__("STACK STATES")
        print("stack 1:", self.avidian.stack_1)
        print("stack 2:", self.avidian.stack_2)
