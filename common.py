from openeye import oechem as oe

def NewGetType(atom):
    mtype = 0
    for bond in atom.GetBonds():
        bo = bond.GetOrder()
        mtype += bo * 16
    return (atom.GetAtomicNum(), atom.GetValence(), atom.GetImplicitHCount(), mtype, 1 if atom.IsInRing() else 0, atom.GetFormalCharge())

def GetType(atom):
    return (atom.GetAtomicNum(), atom.GetValence(), atom.GetImplicitHCount(), atom.GetExplicitDegree(), 1 if atom.IsInRing() else 0, atom.GetFormalCharge())
