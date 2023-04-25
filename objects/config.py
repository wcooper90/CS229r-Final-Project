class CONFIGURATION:
    # toggle debugging, creates random debugging instances of avidians throughout
    # simulation for a closer look
    debugging = True

    # these 3 parameters are also in main.py
    SIMULATION_LENGTH = 1000
    INITIAL_GENOME_LENGTH = 50
    NUM_ANCESTORS = 100

    # population cap; probability of children in a time step being born is (maximum_population - alive avidians) / maximum_population
    maximum_population = 1000

    # initial SIPs per Avida ancestor
    # currently set to 30 times the genome length of avidians
    # in other words, primative Avidians have an average life span of 30 iterations
    initial_sips = 50 * 30

    # avidians will be initialized with initial_sips +/- initial_sips_variation, for variation in lifespan
    intial_sips_variation = 50 * 4

    # initial computational_merit -- how many instructions Avidian is initially able to process per time step
    initial_computational_merit = 50

    # avidians intialized with initial_computational_merit +/- initial_computational_merit_variation
    initial_computational_merit_variation = 4

    # length of registers, will always be 32 for our simulations
    register_length = 32

    # default setting from the Lenski paper
    # default chance of insertion or deletion of instruction
    # these two parameters create a an expected value of 0.225 mutations per genome of length 50
    mutation_error_rate_per_instruction = 0.0025
    single_instruction_insertion_or_deletion_rate = 0.05

    # threshold of SIPs required to reproduce
    SIP_reproduction_threshold = 200

    # probability of avidian being ready to reproduce given threshold of SIPs is reached
    probability_of_reproduction = 0.5

    # genomes from both parents in sexually reproducing settings will copy half their instructions plus
    # or minus this value to create their portion of their child's genome
    genome_length_variability = 5

    # half a child object can only spend up to this many time steps in the reproduction center
    maximum_time_steps_in_reproduction_center = 5

    # number of time steps required before reproducing again
    reproduction_cooldown = 2

    # probability that mov_head or jmp_head instruction do nothing
    # to prevent asexual avidians in particular from converging to a loop
    head_random_probability = 0.01
