from .config import CONFIGURATION
from .Register import Register
from .ReproductionTypeEnum import REPRODUCTION_TYPE
import random


class Avidian:

    def __init__(self, id, genome_instructions, env, reproduction_type, parents=None, time_step=0):
        # configuration
        self.config = CONFIGURATION
        self.id = id
        self.env = env
        self.time_step = time_step

        # avidian attributes
        self.is_alive = True
        self.is_fertile = False
        self.reproduction_type = reproduction_type

        # if simulation type is reproduction separated by sex, assign sex randomly
        self.sex = None
        if reproduction_type == REPRODUCTION_TYPE(3):
            self.sex = 'M' if random.random() > 0.5 else 'F'

        # initialize generated genome
        self.genome = genome_instructions
        # creating variable for copy of instructions to child genome
        self.child_genome = []
        # keep track of who is the parent (tuple of one or two ids)
        self.parents = parents

        # digital organism energy, allow for some variation
        # assigned proportionately to length of genome (with some variation) to maintain average lifespan
        self.SIPS = random.randint(len(self.genome) * self.config.initial_average_life_span - self.config.intial_sips_variation,
                                        len(self.genome) * self.config.initial_average_life_span + self.config.intial_sips_variation)
        # because different Avidians are initialized with different genome lengths, computational merit is
        # assigned proportionately to length of genome (with some variation) to maintain average lifespan
        self.computational_merit = random.randint(len(self.genome) - self.config.initial_computational_merit_variation,
                                                    len(self.genome) + self.config.initial_computational_merit_variation)

        # stacks
        self.stack1 = []
        self.stack2 = []
        self.active_stack = 1

        # initialize registers with random initial inputs
        self.register_A = Register(self.env.generate_environment())
        self.register_B = Register(self.env.generate_environment())
        self.register_C = Register(self.env.generate_environment())

        # organism pointers
        self.instruction_pointer = 0
        self.write_head = 0
        self.read_head = 0
        self.flow_head = 0

        # next environment inputs, assume that these environment variables were immediately loaded to registers B and C
        self.env_input_1, self.env_input_2 = self.register_B.val, self.register_C.val

        # keep track of logical operators this object has already satisfied
        self.operands_achieved = []

        # set to config variable when a child is had
        self.reproduction_cooldown = 0

        # if debugging is on, keep track of the instructions this avidian executed in the last time step
        if self.config.debugging:
            self.instruction_history = []


    # compute the next instruction
    def _step(self, env):
        # if debugging is on, keep track of instructions this avidian executes in this time step
        if self.config.debugging:
            self.instruction_history.append((self.instruction_pointer, self.genome[self.instruction_pointer]))

        step_result = self.genome[self.instruction_pointer](self)
        return step_result
