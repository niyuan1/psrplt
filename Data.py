from numpy import*

class Data:
  def __init__(self, data):
    self.data = data        #npy array containing data
  
  def getData(self):
    return self.data
    
  def __str__(self):
    return "Data: undefined time, undefined band"
    
  def findPulse(self): #gets time bin of giant pulse
    if self.data.shape[-1] == 4:
      print "Polarized data, assuming (0,3) (xx,yy) polarization"
      Unpol = self.sumPols((0,3))
    else:
      Unpol = self
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
    
  def sumPols(self, pols):
    if self.data.shape[-1] == 4:
      data = self.data[..., pols].sum(-1)
    else:
      print "No polarizations to sum"
      data = self.data
    return Data(data)
