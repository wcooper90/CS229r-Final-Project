class DebugAvidian:
    def __init__(self, avidian):
        self.avidian = avidian

    # for debugging with genome
    def _print_genome(self):
        for func in self.avidian.genome:
            print(func.__name__)
