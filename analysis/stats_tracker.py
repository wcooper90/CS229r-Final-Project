def print_stats(vCPU, avidians):
    print("Total number of Avidians: " + str(len(avidians)))
    print("Number of alive Avidians: " + str(len([avidian for avidian in avidians if avidian.is_alive])))
    avidians_with_complex_functions = []
    lengths_of_genomes = []
    for avidian in avidians:
        if avidian.operands_achieved:
            avidians_with_complex_functions.append(str(avidian.id))
        lengths_of_genomes.append(len(avidian.genome))

    print("The average genome length is: " + str(sum(lengths_of_genomes) / len(lengths_of_genomes)))
    print("The following avidians have evolved complex functions: " + " ".join(avidians_with_complex_functions))
