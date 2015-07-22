# Psrplt
A Python based Psrplot like device that operates on and plots 
Scintellometry npy files in recognized pulsar formats.

Scintellometry source: https://github.com/mhvk/scintellometry.git

The file psrplt is the interface program that takes command line arguments for Psrplt.

It incorporates the user friendly features of Argparse to receive and interpret arguments.

As of today, Psrplt is capably of plotting:

-Waterfall


# Data 
is the unit object on which psrplt operates and carries only 
information from the numpy array.

It contains many methods to manipulate and plot Data.


#SpecData 
inherits from Data and in addition carries information about physical units 
which propagate to its methods which also account for units.


#psrnpy 
is a program that allows psrplt compatibility with Psrchive.

It invokes the Swig based Psrchive python wrapper.

As of today, it converts: 

- Psrchive .FTp and .ar -> .npy


#waterplot 
is the plotting program for waterfall data.

As of today, waterplot is capable of plotting:

- Intensity map


#legacy 
is a basic waterplotting software from which the idea of psrplt originated.
