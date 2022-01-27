import os
import math
from urllib.parse import urlencode

from openeye import oechem as oe

import common

def readhistogram():
    freqs = {}
    total = 0
    for i, line in enumerate(open("histogram.txt")):
        broken = list(map(int, line.rstrip().split()))
        freqs[tuple(broken[:-1])] = broken[-1]
        total += broken[-1]

    probs = {}
    for x, y in freqs.items():
        probs[x] = y / total

    return probs

probability = readhistogram()

def multiple(mlist):
    x = mlist[0]
    for y in mlist[1:]:
        x *= y
    return x

def FindMatches(smarts):
    ss = oe.OESubSearch(smarts)
    if not ss.IsValid():
        return -1
    ss.SetMaxMatches(1)
    fname = "sortedbylength_100K.smi"
    mol = oe.OEGraphMol()
    results = {}
    for line in open(fname):
        if "." in line: continue
        mol.Clear()
        oe.OEParseSmiles(mol, line)
        oe.OESuppressHydrogens(mol)
        if mol.NumAtoms() > 30: continue
        match = list(ss.Match(mol))
        if match:
            types = tuple(common.GetType(atom.target) for atom in match[0].GetAtoms())
            if len(types) > 1:
                if types[-1] < types[0]:
                    # Create a canonical form of types, especially for when
                    # the smarts pattern is symmetrical
                    types = tuple(reversed(types))
            if types not in results:
                for i, atom in enumerate(match[0].GetAtoms()):
                    atom.target.SetMapIdx(1 if i==0 else 2)
                newsmi = oe.OECreateSmiString(mol, oe.OESMILESFlag_AtomStereo | oe.OESMILESFlag_BondStereo | oe.OESMILESFlag_AtomMaps)
                results[types] = "%s %s" % (newsmi, mol.GetTitle())

    if not results:
        return []
    tmp = sorted(results.items(), key=lambda x:multiple([probability[y] for y in x[0]]))
    return [x[1] for x in tmp]

if __name__ == "__main__":
    smarts = "*"
    smiles = FindMatches(smarts)
    width = int(math.sqrt(len(smiles)) + 0.5)
    with open("output.html", "w") as out:
        out.write("<html>\n<head>\n")
        out.write('    <link href="output.css" rel="stylesheet">\n')
        out.write("</head>\n<body>\n")
        props = {"abbr":"off","disp":"bridgehead", "showtitle":"true","annotate":"colmap"}
        for smi in smiles:
            props["smi"] = smi
            # props["sma"] = smarts
            out.write('<img src="https://compchem.soseiheptares.com/depict/bow/png?%s" />\n' % urlencode(props))
        out.write("</body>\n</html>\n")


