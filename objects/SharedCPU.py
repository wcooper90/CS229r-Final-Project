from .AuxFunctions.logic_operators import *



class SharedCPU:

    def __init__(self):
        # tuples of (logic operator, corresponding computational merit multiplier reward)
        self.logic_operators = [(not_, 2), (nand_, 2), (and_, 4), (or_n_, 4), (or_, 8),
                                    (and_n_, 8), (nor_, 16), (xor_, 16), (equ_, 32)]


    # iterate through one time step for all avidians
    def compute_time_step(self, avidian, env):
        # if dead, to not do anything
        if not avidian.is_alive:
            return 

        for i in range(avidian.computational_merit):
            # wrap around instruction set
            if avidian.instruction_pointer == len(avidian.genome):
                avidian.instruction_pointer = 0

            # if an IO instruction was read, check for logical operand matches
            step_result = avidian._step(env)
            if step_result:
                self._check_logical_operand_match(avidian, step_result)

            avidian.instruction_pointer += 1
            avidian.SIPS -= 1
            if avidian.SIPS <= 0:
                avidian.is_alive = False
                print('Avidian ' + str(avidian.id) + ' is dead. ')
                return


    def _check_logical_operand_match(self, avidian, step_result):
        # keep track of necessary variables locally, update environmental inputs of avidian for following steps
        env_input_1, env_input_2 = avidian.env_input_1, avidian.env_input_2
        avidian.env_input_1 = avidian.env_input_2
        avidian.env_input_1 = avidian.env.generate_environment()

        # iterate through logic operators to check for matches
        for tup in self.logic_operators:
            func, reward = tup[0], tup[1]
            if step_result == func(env_input_1, env_input_2):
                avidian.computational_merit *= reward
