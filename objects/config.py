class CONFIGURATION:
    # toggle debugging, creates random debugging instances of avidians throughout
    # simulation for a closer look
    debugging = True

    # these 3 parameters are also in main.py
    SIMULATION_LENGTH = 300
    INITIAL_GENOME_LENGTH = 64
    NUM_ANCESTORS = 10


    # initial SIPs per Avida ancestor
    # currently set to 30 times the genome length of avidians
    # in other words, primative Avidians have an average life span of 30 iterations
    initial_sips = 64 * 30

    # avidians will be initialized with initial_sips +/- initial_sips_variation, for variation in lifespan
    intial_sips_variation = 64 * 4

    # initial computational_merit -- how many instructions Avidian is initially able to process per time step
    initial_computational_merit = 64

    # avidians intialized with initial_computational_merit +/- initial_computational_merit_variation
    initial_computational_merit_variation = 4

    # length of registers, will always be 32 for our simulations
    register_length = 32

    # 5 chances with 1% probability to mutate on instruction to another
    instruction_mutation_rate = 0.01
    instruction_mutation_chances = 5

    # 5 chances with 1% probability to delete or add an extra instruction at a random place
    genome_mutation_rate = 0.01
    genome_length_mutation_chances = 5

    # threshold of SIPs required to reproduce
    SIP_reproduction_threshold = 200

    # probability of avidian being ready to reproduce given threshold of SIPs is reached
    probability_of_reproduction = 0.5

    # genomes from both parents in sexually reproducing settings will copy half their instructions plus
    # or minus this value to create their portion of their child's genome
    genome_length_variability = 5

    # population cap; probability of children in a time step being born is (maximum_population - alive avidians) / maximum_population
    maximum_population = 400

    # half a child object can only spend up to this many time steps in the reproduction center
    maximum_time_steps_in_reproduction_center = 5

    # number of time steps required before reproducing again
    reproduction_cooldown = 2
