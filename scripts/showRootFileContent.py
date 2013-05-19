import ROOT,sys,getopt
filenames = None
opts, args = getopt.getopt(sys.argv[1:], '',['inputFiles='])
for opt,arg in opts:
 #print opt , " :   " , arg
 if opt in  ("--inputFiles"):
  filenames=arg
if filenames == None:
  sys.exit('provide a file')
filenames = filenames.split(',')
files = [ROOT.TFile(name) for name in filenames ]
if len(files) == 1:
 file.ls()
