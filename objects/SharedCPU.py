from .AuxFunctions.logic_operators import *
from .Avidian import Avidian


# vCPU to simulate population of avidians
class SharedCPU:

    def __init__(self, num_avidians, reproduction_type):
        # tuples of (logic operator, corresponding computational merit multiplier reward)
        self.logic_operators = [(not_, 2), (nand_, 2), (and_, 4), (or_n_, 4), (or_, 8),
                                    (and_n_, 8), (nor_, 16), (xor_, 16), (equ_, 32)]

        # number of ancestor avidians
        self.num_avidians = num_avidians
        self.reproduction_type = reproduction_type


    # iterate through one time step for all avidians
    def compute_time_step(self, avidian, env):

        # if debugging is on, reset instruction history at every step
        if avidian.config.debugging:
            avidian.instruction_history = []

        # new_offspring to be returned to main script, if applicable
        new_offspring_info = []

        # if dead, to not do anything
        if not avidian.is_alive:
            return []

        # if there is a reproduction cooldown, lower it
        if avidian.reproduction_cooldown > 0:
            avidian.reproduction_cooldown -= 1

        # execute as many sequential instructions as computational merit allows
        for i in range(avidian.computational_merit):

            # wrap around instruction set
            if avidian.instruction_pointer >= len(avidian.genome):
                avidian.instruction_pointer = 0

            # checks if IO instruction was written, or if new offspring occurred
            step_result = avidian._step(env)
            if step_result:
                new_avidian_genome = self._avidian_time_step_result_handler(avidian, step_result)
                if new_avidian_genome:
                    child_avidian_info = [new_avidian_genome, env, avidian.sex]
                    new_offspring_info.append(child_avidian_info)

            # update instruction pointer (wrap around if necessary), update SIPs
            avidian.instruction_pointer += 1
            avidian.SIPS -= 1
            if avidian.SIPS <= 0:
                avidian.is_alive = False
                # print('Avidian ' + str(avidian.id) + ' ran out of sips! he thirsty! ')
                return []

        # return a list of new offspring to main script, if applicable
        return new_offspring_info


    # check to update computational merit of avidian, also return any new offspring objects
    def _avidian_time_step_result_handler(self, avidian, step_result):
        # check if there's a result from IO output
        if step_result[0]:
            self._check_logical_operand_match(avidian, step_result[0])

        return step_result[1]


    def _check_logical_operand_match(self, avidian, step_result):
        # keep track of necessary variables locally, update environmental inputs of avidian for following steps
        env_input_1, env_input_2 = avidian.env_input_1, avidian.env_input_2
        avidian.env_input_1 = avidian.env_input_2
        avidian.env_input_2 = avidian.env.generate_environment()

        # iterate through logic operators to check for matches
        for tup in self.logic_operators:
            func, reward = tup[0], tup[1]
            # only compute if this object has not yet achieved the new logical operator capability
            if func not in avidian.operands_achieved:
                if step_result == func(env_input_1, env_input_2):
                    print("Avidian " + str(avidian.id) + " achieved " + str(func) + "!")
                    avidian.computational_merit *= reward
                    avidian.operands_achieved.append(func)
                    # give this avidian some extra sips, proprotional to reward
                    avidian.SIPS += avidian.SIPS * reward / 16
