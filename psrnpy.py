import sys
import numpy
import psrchive

#run as python psrnpy.py <files>
#get inputs to convert to npy
instruct = sys.argv
#operate on each file
files = [] #get extension, directory, name
for inputFile in instruct[1:]:
    #get file extension
    fileExtension = inputFile.split('.')[-1]
    fileExtension = "."+fileExtension.split(' ')[0]
    #get file directory and name
    filePath = inputFile.split('/')[:-1]
    filePath = "/".join(filePath)
    if filePath != "":
        filePath = filePath + "/"
        fileName = inputFile.split(filePath)[-1]
        fileName = fileName.split(fileExtension)[0]
    else:
        fileName = inputFile.split(fileExtension)[0]
    #check valid file
    if (fileExtension == ".FTp") or (fileExtension == ".ar"):
        print "PSRCHIVE reading " + inputFile
        files.append([filePath, fileName, fileExtension]) #append file info
        arch = psrchive.Archive_load(inputFile) #load archive
        data = arch.get_data() #convert to numpy array
        
        print "Numpy writing " + filePath + fileName + '.npy'
        numpy.save(filePath + fileName, data) #save npy
