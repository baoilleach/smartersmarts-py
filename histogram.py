import time
from collections import defaultdict
from openeye import oechem as oe
from common import GetType

atomtypes = defaultdict(int)

def CountAtomTypes(mol):
    for atom in mol.GetAtoms():
        vector = GetType(atom)
        atomtypes[vector] += 1

if __name__ == "__main__":
    fname = r"D:\LargeData\ChEMBL\chembl24_1\chembl_24_1.ism"

    with open(fname, "r") as inp:
        mol = oe.OEGraphMol()
        t = time.time()
        for i, line in enumerate(inp):
            if i and i % 10000 == 0:
                if i % 100000 == 0: break
                sofar = time.time() - t
                totallength = sofar*1820035 / i
                print(i, "%f" % (totallength - sofar,))
            oe.OEParseSmiles(mol, line)
            oe.OESuppressHydrogens(mol)
            CountAtomTypes(mol)
            mol.Clear()

    tmp = sorted(atomtypes.items(), key=lambda x:x[1], reverse=True)
    with open(r"nbu\histogram_new.txt", "w") as f:
        for x, freq in tmp:
            f.write(" ".join(str(y) for y in x) + " %d\n" % freq)
