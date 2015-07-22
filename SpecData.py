from numpy import*
from Data import Data

class SpecData(Data):
  def __init__(self, data, t_all, f_all, clean):
    Data.__init__(self, data)
    self.t_all = t_all
    self.f_all = f_all
    self.clean = clean
  
  def getTrange(self):
    return self.t_all
    
  def getFrange(self):
    return self.f_all
    
  def getClean(self):
    return self.clean
    
  def __str__(self):
    return "Data: time %d to %d, band %d to %d, clean band %d to %d" % (t_all[0],t_all[1],f_all[0],f_all[1],clean[0],clean[1])
  
  def toTime(self, t_bin): #convert a bin to time units
    interval = self.t_all[1] - self.t_all[0]
    return self.t_all[0] + interval*t_bin/self.data.shape[0]
    
  def toTbin(self, time): #convert a time unit to bin
    interval = self.t_all[1] - self.t_all[0]
    return int((time - self.t_all[0])/interval)
    
  def toFreq(self, f_bin): #convert a chan to freq units
    interval = self.f_all[1] - self.f_all[0]
    return self.f_all[0] + interval*f_bin/self.data.shape[0]
    
  def toChan(self, freq): #convert a freq to channel
    interval = self.f_all[1] - self.f_all[0]
    return int((freq - self.f_all[0])/interval)
    
  def getPulseInterval(self, interval): #gets time bin interval around giant pulse
    giant = Data.findPulse(self)
    giant = self.toTbin(self)
    t = (giant - interval/2, giant + interval/2) #get time bin interval
    return self.cropTime(t)

  def cropTime(self, t_window): #operate on data, crop time axis
    interval = self.t_all[1] - self.t_all[0]
    bstart = int(self.data.shape[0]*(t_window[0] - self.t_all[0])/interval)
    bend = int(self.data.shape[0]*(t_window[1] - self.t_all[0])/interval)
    data = self.data[bstart:bend, ...]
    return SpecData(data, t_window, self.f_all, self.clean)
    
  def cropFreq(self, f_window): #operate on data, crop freq axis
    interval = self.f_all[1] - self.f_all[0]
    bstart = int(self.data.shape[1]*(f_window[0] - self.f_all[0])/interval)
    bend = int(self.data.shape[1]*(f_window[1] - self.f_all[0])/interval)
    data = self.data[:, bstart:bend, ...]
    return SpecData(data, self.t_all, f_window, self.clean)
    
  def sumPols(self, pols):
    if len(self.data.shape) == 4:
      data = self.data[..., pols].sum(-1)
    else:
      print "No polarizations to sum"
      data = self.data
    return SpecData(data, self.t_all, self.f_all, self.clean)
  
  def cleanRFI(self):
    return self.cropFreq(self.clean)
    
  def vlim(self): #get vmin,vmax colorbar limits
    vmin = self.data.mean() - 1*self.data.std()
    vmax = self.data.mean() + 1*self.data.std()
    return vmin, vmax
