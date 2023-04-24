from objects.Environment import Environment
from objects.DebugAvidian import DebugAvidian
from analysis.stats_tracker import print_stats


def run_simulation(avidians, vCPU, tend, reproduction_center):

    time = 0
    env = Environment()

    # set up a debugger for the first avidian
    debugger = DebugAvidian(avidians[0])

    # array for info for new offspring to be stored
    new_avidians_info = []

    # main loop
    while time < tend:
        # compute step for each avidian
        for avidian in avidians:
            # compute a time step
            for offspring_info in vCPU.compute_time_step(avidian, env):
                new_avidians_info.append(offspring_info)

        # use helper functions to create new avidian objects depending on reproduction type
        # returns new avidian objects as well as updating the new_avidians_info list
        new_avidian_objects, new_avidians_info = reproduction_center.process(new_avidians_info, vCPU)

        # append any new avidians to population
        avidians = avidians + new_avidian_objects
        # increment time
        time += 1

        # debugging space
        print("_"*80)
        print('Finished iteration ' + str(time))
        print_stats(vCPU, avidians)
        # debugger._print_genome()
