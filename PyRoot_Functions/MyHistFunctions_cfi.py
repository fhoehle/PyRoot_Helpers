import FWCore.ParameterSet.Config as cms
import ROOT
def SetErrorsNormHist(h1,integral_option):
 if h1.GetBinError(1) == 0:
   print "no Bin Errors were given, poisson like will be created"
   h1.GetSumw2().Set(0);h1.Sumw2()
 if h1.Integral(integral_option) > 0:
  h1.Scale(1.0/h1.Integral(integral_option))
 else:
  print "hist integral ",h1.Integral(integral_option)
################
class MyHistManager:
  def __init__(self,outputFileName="tmp_output",onlyOnePlotOutputFile=False):
    self.outputFileName=outputFileName
    self.onlyOnePlotOutputFile=onlyOnePlotOutputFile
    self.hists=[]
    self.additionalObjects = []
  def saveHist(self,hist,drawOption=""):
    hist.Sumw2()
    self.hists.append([hist,drawOption])
  def done(self):
    outputFile = ROOT.TFile(self.outputFileName+".root","RECREATE")
    if self.onlyOnePlotOutputFile:
      can_dummy = ROOT.TCanvas("dummy"); can_dummy.SaveAs(self.outputFileName+".ps[")
    for hist,opt in self.hists:
      outputFile.cd(); hist.Write()
      can_tmp = ROOT.TCanvas("can_"+hist.GetName(),hist.GetName(),0,0,700,500)
      can_tmp.cd(); hist.Draw(opt)
#      can_tmp.SaveAs(self.outputFileName+".ps" if self.onlyOnePlotOutputFile else can_tmp.GetName()+".pdf" )
    if self.onlyOnePlotOutputFile:
      can_dummy = ROOT.TCanvas("dummy"); can_dummy.SaveAs(self.outputFileName+".ps]")
    outputFile.cd();
    for addObj in self.additionalObjects:
      addObj.Write()
    outputFile.Write();outputFile.Close()
    import os
    os.system("ps2pdf "+self.outputFileName+".ps "+self.outputFileName+".pdf")
#
class RandomAccordingHist(object):
  def __init__(self,h):
    self._h = h
    self._maxX = h.GetBinCenter(h.GetNbinsX())+h.GetBinWidth(h.GetNbinsX())/2.0
    self._minX = h.GetBinCenter(1)-h.GetBinWidth(1)/2.0
    self._maxY = h.GetMaximum()*1.05
    self._localRand = ROOT.TRandom3()
  def getRandom(self): 
    redo=True
    xRand=0
    while redo:
      x=self._localRand.Rndm(); # output 0..1
      xRand = self._minX + (self._maxX - self._minX)*x # adapting Range
      y= self._localRand.Rndm();
      yRand =  self._maxY * y #adapting Range
      if yRand < self._h.GetBinContent(self._h.FindBin(xRand)):
        redo=False
    return xRand
###
colors=[1,2,3,4,5,6,7,8]
class stackHists():
  def __init__(self,hists):
    self.hists = hists
    self.hists.sort(key=lambda h: -1*h.Integral())
    self.histsStacked = []
  def addToStack(self,hist):
    self.hists.append(hist)
    self.hists.sort(key=lambda h: -1*h.Integral())
  def createStack(self):
    histStacked = self.hists[0].Clone(self.hists[0].GetName()+"_stacking");histStacked.SetFillColor(2)
    self.histsStacked.append(histStacked)
    stackName = histStacked.GetName()
    for i,h in enumerate(self.hists[1:]):
      histStacked = histStacked.Clone(stackName+"_"+str(i))
      histStacked.Add(h)
      histStacked.SetLineColor(h.GetLineColor())
      self.histsStacked.append(histStacked)
  def plotStack(self,nostack=False):
     if nostack:
       self.hists[0].Draw()
       for h in self.hists[1:]:
         h.Draw("same")
     else:
       self.histsStacked[-1].SetFillColor(self.histsStacked[-1].GetLineColor())
       self.histsStacked[-1].Draw()
       for h in reversed(self.histsStacked[:-1]):
         h.SetFillColor(h.GetLineColor())
         h.Draw("same")
     ROOT.gPad.RedrawAxis()
#    
def norm1Hist1D(h,opts=""):
  h.Sumw2();h.Scale(1.0/h.Integral(opts))
def loadSameHistFromFiles(histname, files ):
  hists = []
  for  file in files:
    hist = file.Get(histname);
    setattr(hist,'fromFile',file.GetName())
    hists.append(hist)
  return hists 
def plotHists(hists):
  can = ROOT.TCanvas("can_"+hists[0].GetName(),"",200,10,700,500)
  can.cd()
  for i,h in enumerate(hists):
    norm1Hist1D(h)
    h.SetLineColor(colors[i])
    h.Draw("" if i == 0 else "sames")
  return can
def createRatioPlot(dataH,mcH,pad=ROOT.gPad):
        localPad = pad.Clone()
        localPad.Draw()
	localPad.cd()
        heightRatio = 0.2
        pad1 = ROOT.TPad(pad.GetName()+"_pad1","pad1",0,heightRatio,1,1);
        pad1.SetBottomMargin(0.03);
        pad1.Draw();
        pad1.cd();
        dataH.Draw();
        print "dataH ",dataH.GetEntries()

        mcH.Draw("same");
        localPad.cd()
        pad2 = ROOT.TPad(pad.GetName()+"_pad2","pad2",0,0,1,heightRatio);
        pad2.SetTopMargin(0);
        pad2.Draw();
        pad2.cd();
        ratioHist = dataH.Clone("ratioHist_"+dataH.GetName()+"_"+mcH.GetName())
        ratioHist.Sumw2();ratioHist.Divide(mcH)
        ratioHist.Draw("ep")
        return [localPad,pad1,pad2,ratioHist]

def createRatio(pad,hdata,hmc,dontDraw = False):
        pad.cd()
	hratio = hdata.Clone("ratio_"+hdata.GetName()+"_divide_"+hmc.GetName())
	hratio.Clear()
	hratio.Divide(hdata, hmc, 1., 1., "B")
        if dontDraw:
	   return hratio
	hratio.SetYTitle("data/MC ratio")
	
	hratio.SetMarkerSize(1.2)
	hratio.SetMarkerColor(1)
	hratio.SetLineWidth(1)
	
        ### Draw the plot and the ratio on the same canvas
	pad.Divide(1, 2, 0.01, 0.0)
	
	pad.cd(1)
	ROOT.gPad.SetPad(0.0, 0.25, 1.0, 1.0)
	ROOT.gPad.SetTopMargin(0.1)
	ROOT.gPad.SetLeftMargin(0.16) #0.13
	ROOT.gPad.SetRightMargin(0.04) #0.05
	pad.cd(2)
	ROOT.gPad.SetPad(0.0, 0.0, 1.0, 0.25)
	ROOT.gPad.SetBottomMargin(0.375)
	ROOT.gPad.SetLeftMargin(0.16) #0.13
	ROOT.gPad.SetRightMargin(0.04) #0.05
	
	pad.cd(1)
	hdata.GetYaxis().CenterTitle(1)
	hdata.GetYaxis().SetTitleSize(0.055)
	hdata.GetYaxis().SetTitleOffset(1.3)
	hdata.GetYaxis().SetLabelSize(0.055)
	hdata.GetXaxis().SetNdivisions(505, False)
	ROOT.gPad.RedrawAxis()
	hdata.Draw("E1")
	hmc.Draw("histsame")
	maxH = hdata.GetMaximum() if hdata.GetMaximum() > hmc.GetMaximum() else hmc.GetMaximum()
        hdata.GetYaxis().SetRangeUser(0.0,1.2*maxH)
	pad.RedrawAxis()
	
	pad.cd(2)
	hratio.GetYaxis().CenterTitle(1)
	hratio.GetYaxis().SetTitleSize(0.165) #0.11
	hratio.GetYaxis().SetTitleOffset(0.44) #0.55
	hratio.GetYaxis().SetLabelSize(0.16)
	hratio.GetYaxis().SetNdivisions(205)
	
	hratio.GetXaxis().SetTitleSize(0.16)
	hratio.GetXaxis().SetLabelSize(0.2)
	hratio.GetXaxis().SetTitleOffset(1)
	hratio.GetXaxis().SetLabelOffset(0.006)
	hratio.GetXaxis().SetNdivisions(505, False)
	hratio.GetXaxis().SetTickLength(hratio.GetXaxis().GetTickLength() * 3.0)
	
	hratio.SetYTitle("Data/MC")
	hratio.Draw("E1")
	pad.RedrawAxis()
	#pad.GetFrame().Draw()
        pad.Update()
        return hratio
#### printHist
def printHistContent(hist):
  print "Hist Contents: ",hist.GetName()
  for i in range (hist.GetNbinsX()+2):
    print "    bin ",i," content ",hist.GetBinContent(i)," error ",hist.GetBinError(i)," rel Error ",hist.GetBinError(i)/hist.GetBinContent(i) if hist.GetBinError(i) > 0 and hist.GetBinContent(i) != 0 else -99," binCenter ",hist.GetBinCenter(i)," low x edge ",hist.GetXaxis().GetBinLowEdge(i)," upper Edge ",hist.GetXaxis().GetBinUpEdge(i)
