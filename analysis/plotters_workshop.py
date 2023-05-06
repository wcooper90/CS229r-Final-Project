from DataTracker import DataTracker
import os
import glob
import json


data_tracker = DataTracker()

files = glob.glob(os.getcwd() + '/data/*.txt')
num_avidians = len(files)

data = {}

for i in range(num_avidians):
    data[i] = data_tracker.read(i)

"""
TODO: find out which complex functions are being achieved (if it actually proportionally matches computational merit rewards)
TODO: find out if organisms which can complete complex functions are more likely to have a parent who can do the same
"""

capable = {}
for i in range(num_avidians):
    for dic in data[i]['timesteps']:
        if len(dic['complex-functions-complete']) > 0:
            print(str(i), data[i]['parents'], dic['complex-functions-complete'])
            capable[i] = 0
            if data[i]['parents'][0] in capable:
                capable[data[i]['parents'][0]] += 1
            if data[i]['parents'][1] in capable:
                capable[data[i]['parents'][1]] += 1
            break

print(capable)
