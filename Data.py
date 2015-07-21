from numpy import*

class Data:
  def __init__(self, data):
        self.data = data        #npy array containing data
        
  def findPulse(interval): #gets time bin interval around giant pulse
        profile = self.data.sum(1) #sum channels
        giant = profile.argmax() #get maximum (giant pulse) bin
        t = (giant - int(interval/2), giant + (interval/2)) #get time bin interval
        return self.cropTime(t)

    def cropTime(t_window): #operate on data, crop time axis
        data = data[bstart:bend, ...]
        return Data(data)
    
    def cropFreq(f_window): #operate on data, crop freq axis
        data = data[:, bstart:bend, ...]
        return Data(data)
    
    def sumPols(pols):
        data = data.sum(-1)
        return Data(data)
    
    def vlim(): #get vmin,vmax colorbar limits
        vmin = data.mean() - 1*data.std()
        vmax = data.mean() + 1*data.std()
        return vmin, vmax
