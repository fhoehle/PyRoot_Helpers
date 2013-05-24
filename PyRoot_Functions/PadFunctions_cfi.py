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
    first.GetYaxis().SetRangeUser((1-fac)*min,(1+fac)*max)
  pad.Update()
def getHistsOfPad(pad = ROOT.gPad, type = ROOT.TH1F):
  objs = pad.GetListOfPrimitives()
  hists = []
  for obj in objs:
    if isinstance(obj,type):
      hists.append(obj)
  return hists
######################################################
import StatBoxFunctions_cfi
def getStatboxsOfPad(pad = ROOT.gPad):
  objs = pad.GetListOfPrimitives()
  first = None; 
  statboxs = []
  for obj in objs:
    if isinstance(obj,ROOT.TH1):
      statboxs.append(StatBoxFunctions_cfi.GetStatBox(obj))
  return statboxs  
####################
def statboxesRightSide(pad=ROOT.gPad):
   statboxs = getStatboxsOfPad(pad)
   tmpbox = statboxs[0]
   oldPadWidth = pad.GetWw()
   padHeight = pad.GetWh()
   statboxWidth = (tmpbox.GetX2NDC()-tmpbox.GetX1NDC())*oldPadWidth
   statboxHeight = (tmpbox.GetY2NDC()-tmpbox.GetY1NDC())*padHeight
   rightMarginWidth = pad.GetRightMargin()*oldPadWidth
   leftMarginWidth = pad.GetLeftMargin()*oldPadWidth
   histWidth = (1-pad.GetRightMargin()-pad.GetLeftMargin())*oldPadWidth
   noStatboxsPerColumn = int((padHeight*(1-pad.GetTopMargin() - pad.GetBottomMargin()))/statboxHeight)
   columnsStatBoxes = int(len(statboxs)/noStatboxsPerColumn +1)
   pad.SetWindowSize(int(leftMarginWidth+histWidth+statboxWidth*columnsStatBoxes+rightMarginWidth),padHeight)
   newPadWidth = pad.GetWw()
   pad.SetRightMargin((rightMarginWidth+statboxWidth*columnsStatBoxes)/newPadWidth)
   pad.SetLeftMargin(leftMarginWidth/newPadWidth)
   if columnsStatBoxes > 1 :
     print "too many histograms "
   for i,statbox in enumerate(statboxs):
     statbox.SetX1NDC((leftMarginWidth+histWidth+int(i/noStatboxsPerColumn)*statboxWidth)/newPadWidth);statbox.SetX2NDC((leftMarginWidth+histWidth+(int(i/noStatboxsPerColumn)+1)*statboxWidth)/newPadWidth);
     statbox.SetY1NDC((padHeight-pad.GetTopMargin()*padHeight-(i+1-noStatboxsPerColumn*int(i/noStatboxsPerColumn))*statboxHeight)/padHeight);statbox.SetY2NDC((padHeight-pad.GetTopMargin()*padHeight-(i-noStatboxsPerColumn*int(i/noStatboxsPerColumn))*statboxHeight)/padHeight);
   pad.Update()
   pad.Modified()
   pad.Update()
