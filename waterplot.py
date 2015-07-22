import matplotlib.pylab as plt
import sys
from numpy import*
from SpecData import*

pols = (0,3) #xx,yy polarizations

def plotter(data, plotType):
  if plotType == 'i'
      iPlot(data)
      
def vlim(data): #get vmin,vmax colorbar limits
    vmin = data.mean() - 1*data.std()
    vmax = data.mean() + 1*data.std()
    return vmin, vmax

def iPlot(data): #plots intensity in color map
  plot = data.sumPols().getData()
  if len(plot.shape) != 3: #check if waterfall file is valid
      sys.exit("Waterplot may only plot waterfall files")
  vmin, vmax = vlim(plot) #get color scale
      
  if type(data) is SpecData:
      t_all = data.getTrange()
      f_all = data.getFrange()
      plt.imshow(i.T, aspect='auto', interpolation='nearest', 
             origin='lower', cmap=plt.get_cmap('Greys'), 
             extent= t_all + f_all, vmin=vmin, vmax=vmax)
  elif type(data) is Data:
      plt.imshow(i.T, aspect='auto', interpolation='nearest', 
             origin='lower', cmap=plt.get_cmap('Greys'), 
             vmin=vmin, vmax=vmax)
  plt.show()
