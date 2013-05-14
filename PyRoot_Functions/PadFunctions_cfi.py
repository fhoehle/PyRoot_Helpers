import ROOT
def adaptMaxMinOfPad(pad = ROOT.gPad,fac = 0.15):
  objs = pad.GetListOfPrimitives()
  first = None; max = None
  for obj in objs:
    if isinstance(obj,ROOT.TH1F):
      if first == None:
        first = obj
        max = obj.GetMaximum()
        min = obj.GetMinimum()
      max = obj.GetMaximum() if obj.GetMaximum() > max else max
      min = obj.GetMinimum() if obj.GetMinimum() < max else min
  if first != None:
    first.SetMaximum((1+fac)*max)
    first.SetMinimum((1-fac)*min)
  pad.Update()
def getHistsOfPad(pad = ROOT.gPad, type = ROOT.TH1F):
  objs = pad.GetListOfPrimitives()
  hists = []
  for obj in objs:
    if isinstance(obj,type):
      hists.append(obj)
  return hists
import StatBoxFunctions_cfi
def getStatboxsOfPad(pad = ROOT.gPad):
  objs = pad.GetListOfPrimitives()
  first = None; 
  statboxs = []
  for obj in objs:
    if isinstance(obj,ROOT.TH1F):
      statboxs.append(StatBoxFunctions_cfi.GetStatBox(obj))
  return statboxs   
