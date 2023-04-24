from objects.Environment import Environment
from objects.DebugAvidian import DebugAvidian
from objects.config import CONFIGURATION
from analysis.stats_printer import print_stats
import numpy as np
import random


def run_simulation(avidians, vCPU, t_end, reproduction_center, data_tracker=None):

    config = CONFIGURATION()
    time = 0
    env = Environment()
    num_debuggers = None
    debuggers = []
    debugger_spawn_timing = []

    # use DebugAvidian object to track random instances of avidians
    if config.debugging:
        num_debuggers = 40
        debugger_spawn_timing = list(np.arange(0, t_end, t_end // num_debuggers))[1:]
        # set up a debugger for the first avidian
        debuggers.append(DebugAvidian(avidians[-1]))

    # array for info for new offspring to be stored
    new_avidians_info = []

    # main loop
    while time < t_end:
        # if debugger is set up, spawn a debugging avidian every now and then
        if time in debugger_spawn_timing:
            # use most recent avidian as debugger
            debuggers.append(DebugAvidian(avidians[-1]))

        # compute step for each avidian
        for avidian in avidians:
            # compute a time step
            for offspring_info in vCPU.compute_time_step(avidian, env, data_tracker):
                new_avidians_info.append(offspring_info)
            avidian.time_step += 1

        # alive avidians
        num_alive_avidians = len([1 for avidian in avidians if avidian.is_alive])

        # probability of successful set of child objects created
        prob_child_success = max((config.maximum_population - num_alive_avidians) / config.maximum_population, 0)

        # if the maximum population has not been reached, continue making children objects
        if random.random() < prob_child_success:
            # use helper functions to create new avidian objects depending on reproduction type
            # returns new avidian objects as well as updating the new_avidians_info list
            new_avidian_objects, new_avidians_info = reproduction_center.process(new_avidians_info, vCPU, time)
            # append any new avidians to population
            avidians = avidians + new_avidian_objects

        # if the maximum population has been reached, delete some fraction of instances in new_avidians_info each time step
        else:
            new_avidians_info = new_avidians_info[:len(new_avidians_info) // 2]

        # increment time
        time += 1

        # debugging space
        print("_"*80)
        print('Finished iteration ' + str(time))

        if time % 10 == 0:
            print_stats(vCPU, avidians)
            # for debugger in debuggers:
            #     if debugger.avidian.is_alive:
            #         debugger._print_instruction_history()
            #         debugger._print_reproductive_capacity()
