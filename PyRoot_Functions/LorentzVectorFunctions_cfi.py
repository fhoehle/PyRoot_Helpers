import ROOT
def convertToTLorentz(p):
  return ROOT.TLorentzVector(p.px(),p.py(),p.pz(),p.energy())
def boostToCM(p,pCM):
  import copy
  p_boosted = copy.deepcopy(p)
  p_boosted.Boost(ROOT.TVector3(-1.0*pCM.BoostVector().Px(),-1.0*pCM.BoostVector().Py(),-1.0*pCM.BoostVector().Pz()))
  return p_boosted
