class CONFIGURATION:
    # initial SIPs per Avida ancestor
    # currently set to 30 times the genome length of avidians
    # in other words, primative Avidians have an average life span of 30 iterations 
    initial_sips = 1920

    # initial computational_merit -- how many instructions Avidian is initially able to process per time step
    initial_computational_merit = 64

    # length of registers, will always be 32 for our simulations
    register_length = 32

    # each mutation has a 1% chance of mutating
    instruction_mutation_rate = 0.01

    # the whole genome has a 1% chance of adding a new random instruction or deleting an instruction
    genome_mutation_rate = 0.01

    # threshold of SIPs required to reproduce
    SIP_reproduction_threshold = 50

    # probability of avidian being ready to reproduce given threshold of SIPs is reached
    probability_of_reproduction = 0.5

    # genomes from both parents in sexually reproducing settings will copy half their instructions plus
    # or minus this value to create their portion of their child's genome
    genome_length_variability = 5
