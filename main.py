from objects.Avidian import Avidian
from objects.SharedCPU import SharedCPU
from objects.GenomicInstructions import GenomicInstructions
from objects.Environment import Environment
from helpers import run_simulation



SIMULATION_LENGTH = 1
INITIAL_GENOME_LENGTH = 1
NUM_ANCESTORS = 1


env = Environment()
vCPU = SharedCPU()
genomic_instructions = GenomicInstructions()


avidians = []
for i in range(NUM_ANCESTORS):
    avidians.append(Avidian(i, genomic_instructions.generate_test_initial_instructions(INITIAL_GENOME_LENGTH), env))

run_simulation(avidians, vCPU, SIMULATION_LENGTH)
