import numpy as np


## PCVIPR file handling and header parsing
#
# Filehandling and header parsing for PC-VIPR datasets, takes a
# directory and the class will allow quick calls to specific data
# Still needs to be able to handle the time-averaged data
class PCVIPR:
    ## Initialize with a directory
    def __init__(self, directory, initdebug=0):
        self.headerDict = {}  # for header attribute names and values
        self.debug = initdebug  # set as 0 default, otherwise print info regularly
        if not (directory[-1] == '/' or directory[-1] == '\\'):
            directory = directory + '/'  # add trailing '/' if directory doesn't have it
        self.dir = directory  # pcviprheader.txt parent directory
        self.parseHeader()  # call parseHeader initially
        if self.debug:
            print('Folder loaded')

    ## Parses header and stores relevant values
    #
    # Read and parse header, stored in self.headerDict as all
    # strings, and resolution/timeframes in seperate variables
    def parseHeader(self):
        file = open(self.dir + 'pcvipr_header.txt')  # open file (not binary)
        for line in file:
            keyVal = line.split(' ', 1)  # pull out only one line, split by space
            self.headerDict[keyVal[0]] = keyVal[1].rstrip()  # write out key/value in dict
        self.resX = int(float(self.headerDict['matrixx']))  # pull matrix sizes
        self.resY = int(float(self.headerDict['matrixy']))
        self.resZ = int(float(self.headerDict['matrixz']))
        self.fovX = int(float(self.headerDict['fovx']))  # pull field of view (mm)
        self.numT = int(float(self.headerDict['frames']))  # pull number of cardiac frames
        if self.debug:
            print(self.headerDict)

    ## Returns the numpy array from the given filename
    #
    # Mainly called by getData
    def getArray(self, array):
        fd = open(self.dir + array, 'rb')  # open binary .dat file
        data = np.fromfile(file=fd, dtype=np.int16).reshape((self.resX, self.resY, self.resY))
        return data

    ## Returns the dataset of 'Type' at time 't'
    def getData(self, Type, t):
        Type = Type.lower()  # lowercase all entries to standardize
        validTypes = ['mag', 'v1', 'v2', 'v3', 'cd']  # options for loading
        if Type not in validTypes:
            print(('ERROR: ' + Type + 'is not a valid type, try: ' + str(validTypes)))
            return 0  # if we didn't load a correct data type.
        elif t >= self.numT:
            print(('ERROR: time t is too high, numT = ' + str(self.numT)))
            return 0  # if time frames 't' exceeds actual cardiac frames
        elif t < 1:
            print('ERROR: time t needs to be > 0')
            return 0  # if time frames 't' is not positive
        else:
            if Type == 'mag':  # if magnitude dataset
                filename = "ph_{0:03d}_mag.dat".format(t)
            elif Type == 'v1':  # if velocity (x) dataset
                filename = "ph_{0:03d}_vd_1.dat".format(t)
            elif Type == 'v2':  # if velocity (y) dataset
                filename = "ph_{0:03d}_vd_2.dat".format(t)
            elif Type == 'v3':  # if velocity (z) dataset
                filename = "ph_{0:03d}_vd_3.dat".format(t)
            elif Type == 'cd':  # if comple difference dataset
                filename = "ph_{0:03d}_cd.dat".format(t)
            return self.getArray(filename)
