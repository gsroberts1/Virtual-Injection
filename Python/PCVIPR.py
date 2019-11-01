#!/export/home/loecher/linux/bin/python

import numpy as np
import os

## PCVIPR file handling and header parsing
#
# This class does filehandling and header parsing for PC-VIPR datasets,
# ultimately takes just a directory and the class will allow quick calls to
# specific data
#
# Still needs to be able to handle the time averaged data 
class PCVIPR:
    
    ## Initialize with a directory
    def __init__(self,directory, initdebug = 0):
        self.debug = initdebug
        if not (directory[-1] == '/' or  directory[-1] == '\\'):
            directory = directory + '/'
        self.dir = directory
        self.parseHeader()
        self.countNumT()
        if self.debug: print('Folder loaded')
        
    
    ## Parses header and stores relevant values
    #
    # Read and parse header, stored in self.headerDict as all
    # strings, and resolution/timeframes in seperate variables
    def parseHeader(self):
        self.headerDict = {}
        file = open(self.dir + 'pcvipr_header.txt')
        for line in file:
            keyVal = line.split(' ',1)
            self.headerDict[keyVal[0]] = keyVal[1].rstrip()
        self.resX = int(float(self.headerDict['matrixx']))
        self.resY = int(float(self.headerDict['matrixy']))
        self.resZ = int(float(self.headerDict['matrixz']))
        self.fovX = int(float(self.headerDict['fovx']))
        self.numT = int(float(self.headerDict['frames']))
        if self.debug: print((self.headerDict))
    
    ## Returns the numpy array from the given filename
    #
    # Mainly called by getData
    def getArray(self, array):
        fd = open(self.dir + array, 'rb')
        size = self.resX * self.resY * self.resY
        dtype = 'h' #found with numpy.dtype('int16').char
        data = np.fromfile(file=fd, dtype=np.int16).reshape((self.resX, self.resY, self.resY))
        return data
    
    ## Gets the number of timeframes
    #
    # Counts the number of magnitude datasets, this is necessary because the
    # header value is not always correct
    def countNumT(self):
        numT = 0
        for file in os.listdir(self.dir):
            if file[-8:] == '_mag.dat':
                numT = numT + 1
        self.numT = numT
        if self.debug: print(('Time points: ' + str(numT)))
        
    ## Returns the dataset of 'type' at time 't'
    def getData(self, type, t):
        type = type.lower()
        validTypes = ['mag', 'v1', 'v2', 'v3', 'cd']
        if not type in validTypes:
            print(('ERROR: ' + type + 'is not a valid type, try: '  + str(validTypes)))
            return 0
        elif t >= self.numT:
            print(('ERROR: time t is too high, numT = ' + str(self.numT)))
            return 0
        else:
            if type == 'mag':
                filename = "ph_{0:03d}_mag.dat".format(t)
            elif type == 'v1':
                filename = "ph_{0:03d}_vd_1.dat".format(t)
            elif type == 'v2':
                filename = "ph_{0:03d}_vd_2.dat".format(t)
            elif type == 'v3':
                filename = "ph_{0:03d}_vd_3.dat".format(t)
            elif type == 'cd':
                filename = "ph_{0:03d}_cd.dat".format(t)
            return self.getArray(filename)
                

