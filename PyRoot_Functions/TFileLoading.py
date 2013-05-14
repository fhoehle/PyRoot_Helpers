import ROOT
def loadFiles(name=None):
  if name==None:
    print "no name given"
    return None
  filenames = name.split(',')
  return [ROOT.TFile(filename) for filename in filenames]
