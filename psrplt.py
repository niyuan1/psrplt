import sys
import numpy as np
import argparse
from psrdata import*

#parser arguments
parser = argparse.ArgumentParser(prog='psrplt', description="Plots npy in recognized pulsar format")
parser.add_argument('files', metavar='files', type=str, nargs='*',
                    help="files to be plotted")
parser.add_argument('-p', '--plot', type=str, default='c',
                    help="[P] for plot options")
parser.add_argument('-t', '--time', type=str, default=None,
                    help="give total time limits of all data in seconds as t1:t2")
parser.add_argument('-f', '--freq', type=str, default=None,
                    help="set total freq limits of all data in MHz as -f f1:f2")
parser.add_argument('--telescope', type=str, default=None,
                    help="[T] for list of recognized telescopes. This sets freq band accordingly.")
parser.add_argument('-tw', '--timeWindow', type=str, default=None,
                    help="sub-segment of total time to plot in seconds, give as t1:t2")
parser.add_argument('-fw', '--freqWindow', type=str, default=None,
                    help="sub-band of total telescope band to plot in MHz, give as f1:f2")
parser.add_argument('--pulseFinder', type=float, default=None,
                    help="set to find window of <s> seconds around giant pulse and set as time window to plot")
parser.add_argument('--startTime', type=str, default=None,
                    help="set start time in ...Hour:Minute:Second")
args = parser.parse_args()

if args.plot == 'P':
    print "[D] plot intensity profile"
    print "[i] plot intensity spectrum profile"
    print "[c] compare intensity profile with intensity spectrum profile"
    print "[p] compare 4 polarization intensity spectrum profile"
else:
    #make a title
    if args.startTime != None:
        title = args.startTime #give title to plots as startTime
    else:
        title = ""
    if args.pulseFinder != None:
        title = "Giant Pulse " + title
    else:
        title = "Plot " + title
        
    data = [] # make list of data objects
    for plotFile in args.files: #understand files, make data objects
        if args.telescope == None: #attempt to find telescope name from file
            fileName = plotFile.split('/')[-1]
            if (fileName[:2] == 'jb'):
                print "assuming " + plotFile + "is from JB"
                telescope = "JB"
            elif (fileName[:3] == 'aro'):
                print "assuming " + plotFile + "is from ARO"
                telescope = "ARO"
            else: 
                sys.exit("unable to identify telescope for " + plotFile + ", give telescope as argument --telescope")
        elif args.telescpe == ('jb' or 'aro'):
            telescope = "JB"
        elif args.telescpe == 'aro':
            telescope = "ARO"
        else:
            sys.exit("telescope not recognized")
        
        #load numpy file containing data
        plotNpy = np.load(plotFile)

        #get information by telescope
        if telescope == "JB":
            pol_select = (0,3)   #get xx, yy pols
            f_all = (305., 315.) #get freq band
            clean = (307., 313.) #get clean channels
        elif telescope == "ARO":
            pol_select = (0,3)   #get xx, yy pols
            f_all = (400., 800.) #get freq band
            clean = (400., 800.) #get clean channels

        #get total time range
        if args.time != None and len(args.time.split(':')) == 2:
            t_all = (args.time.split(':')[0], args.time.split(':')[1])
        elif args.time != None: #nonsensical time given
            sys.exit("give total time limits of all data in seconds as t1:t2")
        else: #have bins as time unit
            t_all = (0,plotNpy.shape[0])
        
        #get total frequency range
        if args.freq != None and len(args.freq.split(':')) == 2:
            f_all = (args.freq.split(':')[0], args.freq.split(':')[1])
        elif args.freq != None: #nonsensical freq given
            sys.exit("give total freq limits of all data in MHz as f1:f2")
        
        plotNpy = np.load(plotFile)
        data.append(Data(plotNpy, t_all, f_all, pol_select, clean))
