from numpy import*

class Data:
  def __init__(self, data, telescope):
    self.data = data        #npy array containing data
    self.telescope = telescope
    
  def getTelescope(self):
    return self.telescope
  
  def getData(self):
    return self.data
    
  def findPulse(self): #gets time bin of giant pulse
    if len(self.data.shape) == 4:
      print "Polarized data, assuming " + self.telescope + " polarization"
      if self.telescope == 'jb':
        pols = (0,3)
      elif self.telescope == 'aro':
        pols = (0,3)
      else:
        sys.exit("No polarization information for this telescope")
      Unpol.sumPols(pols)
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
    return Data(data, self.telescope)
    
  def cropFreq(self, f_window): #operate on data, crop freq axis
    data = self.data[:, bstart:bend, ...]
    return Data(data, self.telescope)
    
  def sumPols(self, pols):
    if len(self.data.shape) == 4:
      data = self.data[..., pols].sum(-1)
    else:
      print "No polarizations to sum"
      data = self.data
    return Data(data, self.telescope)
  
  def vlim(self): #get vmin,vmax colorbar limits
    vmin = self.data.mean() - 1*self.data.std()
    vmax = self.data.mean() + 1*self.data.std()
    return vmin, vmax
