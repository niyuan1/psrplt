class Data:
    def __init__(self, data, t_all, f_all, pol, clean):
        self.data = data        #npy array containing data
        self.t_all = t_all      #(start time, end time)
        self.f_all = f_all      #(start freq, end freq)
        self.pol = pol          #(xx pol, yy pol)
        self.clean = clean

    def findPulse(interval): #gets time interval around giant pulse
        profile = self.cleanRFI() #clean rfi
        profile = profile[..., pol_select].sum(-1) #sum pols
        profile = profile.sum(1) #sum channels
        giant = profile.argmax() #get maximum (giant pulse) bin
        giant = (t[1] - t[0])*giant/profile.shape[0] + t[0] #convert to time
        t = (giant - interval/2, giant + interval/2) #get time interval
        return self.cropTime(t)

    def cropTime(t_window): #operate on data, crop time axis
        interval = self.t_all[1] - self.t_all[0]
        bstart = int(self.data.shape[0]*(t_window[0] - self.t_all[0])/interval)
        bend = int(self.data.shape[0]*(t_window[1] - self.t_all[0])/interval)
        data = data[bstart:bend, ...]
        return Data(data, t_window, self.f_all, self.pol, self.clean)
    
    def cropFreq(f_window): #operate on data, crop freq axis
        interval = self.f_all[1] - self.f_all[0]
        bstart = int(self.data.shape[1]*(f_window[0] - self.f_all[0])/interval)
        bend = int(self.data.shape[1]*(f_window[1] - self.f_all[0])/interval)
        data = data[:, bstart:bend, ...]
        return Data(data, self.t_all, f_window, self.pol, self.clean)
    
    def cleanRFI(): 
        clean = (min(self.clean[0],self.f_all[0]), 
                 max(self.clean[1],self.f_all[1]))
        return self.cropFreq(clean)
    
    def vlim(): #get vmin,vmax colorbar limits
        vmin = data.mean() - 1*data.std()
        vmax = data.mean() + 1*data.std()
        return vmin, vmax
