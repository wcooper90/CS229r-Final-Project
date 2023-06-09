from objects.Environment import Environment
from objects.DebugAvidian import DebugAvidian
from objects.config import CONFIGURATION
from analysis.stats_printer import snapshot_plot, track_stats, plot
import numpy as np
import random
import threading


def run_thread(vCPU, avidians, env, new_avidians_info, data_tracker=None):
    for avidian in avidians:
        # compute a time step
        for offspring_info in vCPU.compute_time_step(avidian, env, data_tracker):
            new_avidians_info.append(offspring_info)
        avidian.time_step += 1


def run_simulation(avidians, vCPU, t_end, reproduction_center, threads=2, data_tracker=None):

    # data to plot
    data = {"avg_genome_length":[], "avg_generation":[], "percent_complex_features":[],
            'max_genome_length': [], 'min_genome_length': [],
            "max_generation": [], "min_generation": [], 'avg_computational_merit': [],
            'min_computational_merit': [], 'max_computational_merit': []}


    config = CONFIGURATION()
    time = 0
    env = Environment()
    num_debuggers = None
    # debuggers = []
    # debugger_spawn_timing = []
    num_alive_avidians = config.NUM_ANCESTORS

    # use DebugAvidian object to track random instances of avidians
    # if config.debugging:
    #     num_debuggers = 40
    #     debugger_spawn_timing = list(np.arange(0, t_end, t_end // num_debuggers))[1:]
    #     # set up a debugger for the first avidian
    #     debuggers.append(DebugAvidian(avidians[-1]))

    # array for info for new offspring to be stored
    new_avidians_info = []

    # no longer need to keep track of dead avidians
    alive_avidians = []

    # main loop
    while time < t_end:
        # if debugger is set up, spawn a debugging avidian every now and then
        # if time in debugger_spawn_timing:
        #     # use most recent avidian as debugger
        #     debuggers.append(DebugAvidian(avidians[-1]))

        # # compute step for each avidian
        # for avidian in avidians:
        #     # compute a time step
        #     for offspring_info in vCPU.compute_time_step(avidian, env, data_tracker):
        #         new_avidians_info.append(offspring_info)
        #     avidian.time_step += 1

        # compute step for each avidian across multiple threads
        split_work = np.array_split(avidians, threads)
        thds = []
        for i in range(threads):
            thd = threading.Thread(target=run_thread, args=(vCPU, split_work[i], env, new_avidians_info, ))
            thd.start()
            thds.append(thd)

        # wait for all threads to finish
        for thd in thds:
            thd.join()


        # alive avidians
        # num_alive_avidians = len([1 for avidian in avidians if avidian.is_alive])

        # probability of successful set of child objects created
        prob_child_success = max((config.maximum_population - num_alive_avidians) / config.maximum_population, 0)
        # print(prob_child_success)
        # print("num_alive: " + str(num_alive_avidians))

        # if the maximum population has not been reached, continue making children objects
        if random.random() < prob_child_success:
            # use helper functions to create new avidian objects depending on reproduction type
            # returns new avidian objects as well as updating the new_avidians_info list
            new_avidian_objects, new_avidians_info = reproduction_center.process(new_avidians_info, vCPU, time)
            # append any new avidians to population
            avidians = avidians + new_avidian_objects

        # if the maximum population has been reached, delete some fraction of instances in new_avidians_info each time step
        else:
            # new_avidians_info = [new_avidians_info[:len(new_avidians_info) // 2]]
            new_avidians_info = []



        # debugging space
        if time % config.interval == 0:
            print("_"*80)
            print('Finished iteration ' + str(time))
            snapshot_plot(vCPU, avidians, time)
            track_stats(vCPU, avidians, data)
            # for debugger in debuggers:
            #     if debugger.avidian.is_alive:
            #         print(debugger.avidian.generation)
                    # debugger._print_instruction_history()
                    # debugger._print_reproductive_capacity()

        # increment time
        time += 1


        """
        ONLY KEEPING ALIVE AVIDIANS
        """
        avidians = [avidian for avidian in avidians if avidian.is_alive]
        # alive avidians
        num_alive_avidians = len(avidians)

    plot(data)

    # for key in data.keys():
    #     print(data[key])
