import matplotlib.pylab as plt
import sys
from numpy import*

pols = (0,3) #xx,yy polarizations

def plotter(data, plotType):
  if plotType == 'i'
      iPlot(data)
      
def vlim(data): #get vmin,vmax colorbar limits
    vmin = data.mean() - 1*data.std()
    vmax = data.mean() + 1*data.std()
    return vmin, vmax

def iPlot(data):
  plot = data.getData()
  if plot.shape[-1] == 4:
      print "Polarized data, assuming (0,3) (xx,yy) polarization"
      plot = data.sumPols((0,3)).getData()
  if len(plot.shape) != 3:
      print "Waterplot may only plot waterfall files"
  
  vmin, vmax = vlim(plot)
  plt.imshow(i.T, aspect='auto', interpolation='nearest', 
             origin='lower', cmap=plt.get_cmap('Greys'), 
             extent= t_all + f_all, vmin=vmin, vmax=vmax)
  plt.show()
