class DebugAvidian:
    # initialize the debugger for the input avidian 
    def __init__(self, avidian):
        self.avidian = avidian


    # use all debugging functions at every time step for this Avidian
    def _print_all(self):
        self._print_genome()
        self._print_inputs()
        self._print_stacks()


    # header for other debugging
    def __print_header__(self, title):
        print("*"*20 + "DEBUG: " + title + "*"*20)


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
