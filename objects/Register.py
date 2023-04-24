"""
Register Object, each Avida object has 3 of them. This class exists so we can reference and pass
values in registers of Avida objects without actually changing register values
"""
class Register:

    # initialize with just the register's value
    def __init__(self, val):
        self.val = val

    # for ease of access printing register's value
    def __repr__(self):
        return self.val

    # for ease of access printing register's value
    def __str__(self):
        return self.val
