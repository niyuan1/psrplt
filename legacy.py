import sys
import numpy as np
import matplotlib.pylab as plt

plotType = sys.argv[1]
plotFile = sys.argv[2]

#plot parameters
t_window = (0.815, 0.885)    #time window
f_window = (605., 615.)      #frequency window

#pulse finder parameters
find_Giant_Pulse = True      #do pulseFinder
interval = 0.01              #plot range around giant pulse
f_clean = (607., 613.)       #clean channels

#observation parameters
title = "Giant Pulse at 14:25:05"
t_all = (0.80, 0.90)

#telescope parameters
fileName = plotFile.split('/')[-1]
if (fileName[:2] == 'jb'):
    f_all = (605., 615.)
    title = "JB: " + title
    pol_select = (0, 3)
elif (fileName[:3] == 'aro'):
    f_all = (400., 800.)
    title = "ARO: " + title
    pol_select = (0, 3)
else:
    print "telescope not recognized"

def pulseFinder(data, t, interval): #gets interval around giant pulse
    profile = data[..., pol_select].sum(-1)
    profile = profile.sum(1)
    giant = profile.argmax()
    giant = (t[1] - t[0])*giant/profile.shape[0] + t[0]
    t = (giant - interval/2, giant + interval/2)
    return t #return start, end of time interval

def cropTime(data, t_all, t_window): #operate on data, crop time axis
    interval = t_all[1] - t_all[0]
    bstart = int(data.shape[0]*(t_window[0] - t_all[0])/interval)
    bend = int(data.shape[0]*(t_window[1] - t_all[0])/interval)
    data = data[bstart:bend, ...]
    return data, t_window #return cropped data and time interval

def cropFreq(data, f_all, f_window): #operate on data, crop freq axis
    interval = f_all[1] - f_all[0]
    bstart = int(data.shape[1]*(f_window[0] - f_all[0])/interval)
    bend = int(data.shape[1]*(f_window[1] - f_all[0])/interval)
    data = data[:, bstart:bend, ...]
    return data, f_window #return cropped data and freq interval

def vlim(data): #get vmin,vmax colorbar limits
    vmin = data.mean() - 1*data.std()
    vmax = data.mean() + 1*data.std()
    return vmin, vmax

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s waterfall" % sys.argv[0]
        # Run the code as eg: python waterplot.py waterfall.npy
        sys.exit(1)
    # Waterfall axes: time, frequency, pol=4 (XX, XY, YX, YY).
    w = np.load(plotFile)

    #crop out relevant time window
    w, t_all = cropTime(w, t_all, t_window)
    #crop out relevant frequency window
    w, f_all = cropFreq(w, f_all, f_window)
    #get relevant chunk of waterfall
    if find_Giant_Pulse:
        #clean rfi
        clean = cropFreq(w, f_all, f_clean)[0]
        #find pulse in clean data
        t_window = pulseFinder(clean, t_all, interval)
        #crop out relevant time period
        w, t_all = cropTime(w, t_all, t_window)
    
    #make plots
    plt.figure(1)
    plt.suptitle(title)
    if plotType == 'p': # Make polarization plots
        plt.subplot(221) #plot xx
        vmin, vmax = vlim(w[...,0])
        plt.title('xx')
        plt.imshow(w[...,0].T, aspect='auto', interpolation='nearest', 
                   origin='lower', cmap=plt.get_cmap('Greys'), 
                   extent= t_all + f_all, vmin=vmin, vmax=vmax)
        plt.subplot(222) #plot xy
        vmin, vmax = vlim(w[...,1])
        plt.title('xy')
        plt.imshow(w[...,1].T, aspect='auto', interpolation='nearest', 
                   origin='lower', cmap=plt.get_cmap('Greys'), 
                   extent= t_all + f_all, vmin=vmin, vmax=vmax)
        plt.subplot(223) #plot yx
        vmin, vmax = vlim(w[...,2])
        plt.title('yx')
        plt.imshow(w[...,2].T, aspect='auto', interpolation='nearest', 
                   origin='lower', cmap=plt.get_cmap('Greys'), 
                   vmin=vmin, vmax=vmax)
        plt.subplot(224) #plot yy
        vmin, vmax = vlim(w[...,3])
        plt.title('yy')
        plt.imshow(w[...,3].T, aspect='auto', interpolation='nearest', 
                   origin='lower', cmap=plt.get_cmap('Greys'), 
                   extent= t_all + f_all, vmin=vmin, vmax=vmax)
        plt.show() #show plot

    if plotType == 'i': #make intensity plot
        i = w[...,(pol_select)].sum(-1)
        vmin, vmax = vlim(i)
        plt.imshow(i.T, aspect='auto', interpolation='nearest', 
                   origin='lower', cmap=plt.get_cmap('Greys'), 
                   extent= t_all + f_all, vmin=vmin, vmax=vmax)
        plt.show()

    if plotType == 'D': #make pulse plot
        p = w[...,(pol_select)].sum(-1)
        p = cropFreq(p, f_all, f_clean)[0].sum(1)
        x = np.linspace(t_all[0], t_all[1], len(p))
        plt.plot(x,p)
        plt.xlim(t_all)
        plt.show()

    if plotType == 'c': #make pulse and intensity plot
        plt.subplot(211) #make intensity plot
        i = w[...,(pol_select)].sum(-1)
        vmin, vmax = vlim(i)
        plt.imshow(i.T, aspect='auto', interpolation='nearest', 
                   origin='lower', cmap=plt.get_cmap('Greys'), 
                   extent= t_all + f_all, vmin=vmin, vmax=vmax)
        plt.subplot(212) #make pulse plot
        p = cropFreq(i, f_all, f_clean)[0].sum(1)
        #x = np.linspace(t_all[0], t_all[1], len(p))
        plt.plot(p)
        plt.xlim(0, len(p))
        #plt.xlim(x, t_all)
        plt.show()
