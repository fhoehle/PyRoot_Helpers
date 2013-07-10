import ROOT
###########################
class myTDirectory (object):
  def __init__(self,dir):
     self.dir=dir
  def __dir__(self):
     return [key.GetName() for key in self.dir.GetListOfKeys()]
  def __getattr__(self,name):
    if name in [ key.GetName() for key in self.dir.GetListOfKeys()]:
      obj = self.dir.Get(name)
      return myTDirectory(obj) if isinstance(obj,ROOT.TDirectory) else obj
    else:
      return super(object,self).__getattribute__(name)
####################
class myTFile (ROOT.TFile):
  def __insideDir__(self):
    return self.objs
  def __dir__(self):
    return [ key.GetName() for key in super(ROOT.TFile,self).GetListOfKeys()] 
  def __getattr__(self,name):
    if name in [ key.GetName() for key in super(ROOT.TFile,self).GetListOfKeys()]:
      obj = super(ROOT.TFile,self).Get(name)
      return myTDirectory(obj) if isinstance(obj,ROOT.TDirectory) else obj
    else:
      return super(ROOT.TFile,self).__getattribute__(name)
######################

