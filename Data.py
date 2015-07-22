from numpy import*
from waterplot import*

################################
# Data Class
################################

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
    bstart, bend = int(t_window[0]), int(t_window[1])
    data = self.data[bstart:bend, ...]
    return Data(data)
    
  def cropFreq(self, f_window): #operate on data, crop freq axis
    bstart, bend = int(f_window[0]), int(f_window[1])
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

################################
# Special Data Class extends Data Class
# Operates with physical units
################################

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
    tstart, tend = self.t_all[0], self.t_all[1]
    fstart, fend = self.f_all[0], self.f_all[1]
    cstart, cend = self.clean[0], self.clean[1]
    return "Data: time %g:%g, band %g:%g, clean %g:%g" % (tstart, tend, fstart, fend, cstart, cend)
  
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
    
  def sumPols(self, pols=None): #sum polarizations
    if pols != None and self.data.shape[-1] == 4:
        data = self.data[..., pols].sum(-1)
    elif self.data.shape[-1] == 4:
        print "Assuming (0,3) (xx,yy) polarization"
        data = self.data[..., (1,3)].sum(-1)
    else: 
        data = self.data
    return SpecData(data, self.t_all, self.f_all, self.clean)
  
  def cleanRFI(self): #clean known RFI
    return self.cropFreq(self.clean)
