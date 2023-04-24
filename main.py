from objects.Avidian import Avidian
from objects.SharedCPU import SharedCPU
from objects.GenomicInstructions import GenomicInstructions
from objects.Environment import Environment
from objects.ReproductionTypeEnum import REPRODUCTION_TYPE
from objects.ReproductionCenter import ReproductionCenter
from objects.config import CONFIGURATION
from analysis.DataTracker import DataTracker
from run_simulation import run_simulation


# connect to configuration file
config = CONFIGURATION()

# these are here for easy access, more parameters can be found in >objects>config.py
SIMULATION_LENGTH = config.SIMULATION_LENGTH
INITIAL_GENOME_LENGTH = config.INITIAL_GENOME_LENGTH
NUM_ANCESTORS = config.NUM_ANCESTORS

# reproduction type can be ASEX (asexual), SEX_NO_SEXES (sexual but does not distinguish between male and female),
# and SEX_WITH_SEXES (sexual, where only males and females are copatible)
reproduction_type = REPRODUCTION_TYPE.SEX_NO_SEXES

# environment generates random binary strings as inputs for Avidians
env = Environment()

# generates initiate genomic instructions for Avidian objects
genomic_instructions = GenomicInstructions()

# handles instructions for mutating and combining genomes, and spawning new Avidian objects
reproduction_center = ReproductionCenter(reproduction_type)

# for analysis and plotting
data_tracker = DataTracker()
#
# # wipe all current files
# data_tracker.clear_dir()

# intialize ancestors
avidians = []
for i in range(NUM_ANCESTORS):
    new_genome = genomic_instructions.generate_random_initial_instructions(INITIAL_GENOME_LENGTH)
    avidians.append(Avidian(i, new_genome, env, reproduction_type, time_step=0))

# initialize vCPU
vCPU = SharedCPU(NUM_ANCESTORS, reproduction_type)
# run simulation with data tracker
# run_simulation(avidians, vCPU, SIMULATION_LENGTH, reproduction_center, data_tracker)
# run simulation without data tracker
run_simulation(avidians, vCPU, SIMULATION_LENGTH, reproduction_center)
