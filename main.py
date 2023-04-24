from objects.Avidian import Avidian
from objects.SharedCPU import SharedCPU
from objects.GenomicInstructions import GenomicInstructions
from objects.Environment import Environment
from objects.ReproductionTypeEnum import REPRODUCTION_TYPE
from objects.ReproductionCenter import ReproductionCenter
from run_simulation import run_simulation


# these are here for easy access, more parameters can be found in >objects>config.py
SIMULATION_LENGTH = 1000
INITIAL_GENOME_LENGTH = 64
NUM_ANCESTORS = 10

# reproduction type can be ASEX (asexual), SEX_NO_SEXES (sexual but does not distinguish between male and female),
# and SEX_WITH_SEXES (sexual, where only males and females are copatible)
reproduction_type = REPRODUCTION_TYPE.SEX_WITH_SEXES


# environment generates random binary strings as inputs for Avidians
env = Environment()

# generates initiate genomic instructions for Avidian objects
genomic_instructions = GenomicInstructions()

# handles instructions for mutating and combining genomes, and spawning new Avidian objects
reproduction_center = ReproductionCenter(reproduction_type)

# intialize ancestors
avidians = []
for i in range(NUM_ANCESTORS):
    new_genome = genomic_instructions.generate_random_initial_instructions(INITIAL_GENOME_LENGTH)
    avidians.append(Avidian(i, new_genome, env, reproduction_type))

# initialize vCPU
vCPU = SharedCPU(NUM_ANCESTORS, reproduction_type)
# run simulation
run_simulation(avidians, vCPU, SIMULATION_LENGTH, reproduction_center)
