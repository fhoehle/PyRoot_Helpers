import ROOT,math
def GetStatBox(h1,pad = ROOT.gPad):
 #print "version2a"
 pad.Update()
 statbox_tmp = None
 for obj in h1.GetListOfFunctions():
   if isinstance(obj,ROOT.TPaveStats):
     if not statbox_tmp:
       statbox_tmp = obj
     else:
       print "ATTENTION SECOND statbox found"
 if statbox_tmp:
  statbox_tmp.SetName("statbox_"+h1.GetName())
 else:
  print "no statbox found, maybe not created by drawing"
 return statbox_tmp  
def StatBoxSameLineColor(h1,pad = ROOT.gPad ):
  statbox_tmp = GetStatBox(h1,pad)
  color=h1.GetLineColor()
  statbox_tmp.SetTextColor(color)
