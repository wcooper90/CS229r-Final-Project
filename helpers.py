from objects.Environment import Environment
from objects.DebugAvidian import DebugAvidian


def run_simulation(avidians, vCPU, tend):

    time = 0
    env = Environment()

    # set up a debugger for the first avidian
    debugger = DebugAvidian(avidians[0])

    while time < tend:
        for avidian in avidians:
            vCPU.compute_time_step(avidian, env)
        time += 1
        print("_"*80)
        print('Finished iteration 1')
        print("_"*80)


        # debugging space
        debugger._print_genome()
