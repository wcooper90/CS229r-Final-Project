
# bitwise not
# the second argument is a placeholder, not used in this logic operator
def not_(a, b):
    out = ""
    for val in a:
        if val == "1":
            out += "0"
        else:
            out += "1"
    return out


# bitwise nand
def nand_(a, b):
    out = ""
    for i in range(len(a)):
        if a[i] == "1" and b[i] == "1":
            out += "0"
        else:
            out += "1"
    return out


# bitwise and
def and_(a, b):
    out = ""
    for i in range(len(a)):
        if a[i] == "1" and b[i] == "1":
            out += "0"
        elif a[i] == "0" and b[i] == "0":
            out += "0"
        else:
            out += "1"
    return out


# bitwise or_n
def or_n_(a, b):
    out = ""
    for i in range(len(a)):
        if a[i] == "1" and b[i] == "1":
            out += "1"
        elif a[i] == "0" and b[i] == "0":
            out += "1"
        elif a[i] == "1" and b[i] == "0":
            out += "1"
        else:
            out += "0"
    return out


# bitwise  or
def or_(a, b):
    out = ""
    for i in range(len(a)):
        if a[i] == "0" and b[i] == "0":
            out += "0"
        else:
            out += "1"
    return out


# bitwise and_n
def and_n_(a, b):
    out = ""
    for i in range(len(a)):
        if a[i] == "1" and b[i] == "0":
            out += "1"
        else:
            out += "0"
    return out


# bitwise nor
def nor_(a, b):
    out = ""
    for i in range(len(a)):
        if a[i] == "0" and b[i] == "0":
            out += "1"
        else:
            out += "0"
    return out


# bitwise xor
def xor_(a, b):
    out = ""
    for i in range(len(a)):
        if a[i] == "1" and b[i] == "0":
            out += "1"
        elif a[i] == "0" and b[i] == "1":
            out += "1"
        else:
            out += "0"
    return out


# bitwise equals
def equ_(a, b):
    out = ""
    for i in range(len(a)):
        if a[i] == "1" and b[i] == "1":
            out += "1"
        elif a[i] == "0" and b[i] == "0":
            out += "1"
        else:
            out += "0"
    return out
