import ROOT 
def NormalStyle():
  ROOT.gROOT.SetStyle('Plain')
  #ROOT.gStyle.SetFillColor(0);  #white fill color # otherwise all hists are filled with white
  ROOT.gStyle.SetFrameBorderMode(0);  #no frame border
  ROOT.gStyle.SetCanvasBorderMode(0);  #no canvas border
  ROOT.gStyle.SetOptTitle(0);  #no title
