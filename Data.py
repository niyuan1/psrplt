from numpy import*

class Data:
  def __init__(self, data):
    self.data = data        #npy array containing data
  
  def getData(self):
    return self.data
    
  def __str__(self):
    return "Data: undefined time, undefined band"
    
  def findPulse(self): #gets time bin of giant pulse
    Unpol = self.sumPols().getData()
    profile = Unpol.data.sum(1) #sum channels
    return profile.argmax() #get maximum (giant pulse) bin
    
  def getPulseInterval(self, interval): #gets time bin interval around giant pulse
    giant = self.findPulse()
    t = (giant - int(interval/2), giant + (interval/2)) #get time bin interval
    return self.cropTime(t)
    
  def cropTime(self, t_window): #operate on data, crop time axis
    data = self.data[bstart:bend, ...]
    return Data(data)
    
  def cropFreq(self, f_window): #operate on data, crop freq axis
    data = self.data[:, bstart:bend, ...]
    return Data(data)
    
  def sumPols(self, pols=None):
    if pols != None and self.data.shape[-1] == 4:
        data = self.data[..., pols].sum(-1)
    elif self.data.shape[-1] == 4:
        print "Assuming (0,3) (xx,yy) polarization"
        data = self.data[..., (1,3)].sum(-1)
    else: 
        data = self.data
    return Data(data)

  def waterplot(self, plotType):
    if plotType == 'i':
        plotter(self.sumPols(), plotType)
