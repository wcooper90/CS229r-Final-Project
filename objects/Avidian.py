from .config import CONFIGURATION
from .Register import Register


class Avidian:

    def __init__(self, id, genome_instructions, env):
        # configuration
        self.config = CONFIGURATION
        self.is_alive = True
        self.id = id
        self.env = env

        # digital organism energy
        self.SIPS = self.config.initial_sips
        self.computational_merit = self.config.initial_computational_merit

        # stacks
        self.stack1 = []
        self.stack2 = []
        self.active_stack = 1

        # initialize registers with random initial inputs
        self.register_A = Register(self.env.generate_environment())
        self.register_B = Register(self.env.generate_environment())
        self.register_C = Register(self.env.generate_environment())

        # initialize generated genome
        self.genome = genome_instructions

        # organism pointers
        self.instruction_pointer = 0
        self.write_head = 0
        self.read_head = 0
        self.flow_head = 0

        # next environment inputs
        self.env_input_1, self.env_input_2 = self.env.generate_environment(), self.env.generate_environment()


    # compute the next instruction
    def _step(self, env):
        step_result = self.genome[self.instruction_pointer](self)
        return step_result
