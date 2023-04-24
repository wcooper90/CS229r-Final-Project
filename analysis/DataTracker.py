import os
import glob
import json
import pandas as pd


class DataTracker:
    def __init__(self):
        pass


    def clear_dir(self):
        files = glob.glob(os.getcwd() + '/analysis/data/*.txt')
        for f in files:
            try:
                os.unlink(f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))


    def write(self, avidian):
        file_path = os.getcwd() + '/analysis/data/' + str(avidian.id) + '.txt'

        # if this is a new avidian, use create new file and use first line for metadata
        if not os.path.isfile(file_path):
            header_details = {}
            header_details['parents'] = avidian.parents
            header_details['sex'] = avidian.sex
            header_details['genomic-sequence'] = [genome.__name__ for genome in avidian.genome]
            header_details['genome-length'] = len(avidian.genome)
            with open(file_path, 'w') as f:
                f.write(json.dumps(header_details) + '\n')
            f.close()


        with open(file_path, 'a') as f:
            details = {}
            details['timestep'] = avidian.time_step
            details['register-A'] = avidian.register_A.val
            details['register-B'] = avidian.register_B.val
            details['register-C'] = avidian.register_C.val
            details['instruction-pointer'] = avidian.instruction_pointer
            details['read-head'] = avidian.read_head
            details['write-head'] = avidian.write_head
            details['flow-head'] = avidian.flow_head
            details['SIPS'] = avidian.SIPS
            details['computational-merit'] = avidian.computational_merit
            details['complex-functions-complete'] = [func.__name__ for func in avidian.operands_achieved]

            # if avidian.instruction_history:
            #     details['instruction-history'] = [(instruction[1].__name__, instruction[0]) for instruction in avidian.instruction_history]

            f.write(json.dumps(details) + '\n')

        f.close()


    # retrieve the data file of specified avidian, return a dictionary
    def read(self, id):
        data = {}
        # this file path appends only '/data/' and not '/analysis/data/' because it assumes you are running
        # analysis scripts from within the analysis directory
        file_path = os.getcwd() + '/data/' + str(id) + '.txt'
        with open(file_path, 'r') as f:
            lines = f.readlines()
            metadata = json.loads(lines[0])
            data = metadata
            data['timesteps'] = []
            for line in lines[1:]:
                data['timesteps'].append(json.loads(line))
        f.close()

        return data
