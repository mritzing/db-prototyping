def parsefile(filename):
    with open(filename, 'r') as pdbFile:
        for line in pdbFile.readlines():
            if "atm" or "atom" in line.split()[0]:
                parseline(line.strip())

# Ex lines:
# HETATM    3  NAQ DRG     1      18.720   7.260   1.360  1.00 20.00           N
# HETATM    4  OAT DRG     1      20.090   7.560   1.340  1.00 20.00           O


def parseline(line):
    lineArr = line.split()
