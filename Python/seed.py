from pylab import *


## Seed random points within a sphere
def sampleInSphere(rad, r0):
    u = rand()  # random float between 0 and 1
    v = rand()
    w = rand()
    
    theta = 2*pi*u  # convert to random angle between 0 and 2pi
    phi = arccos(2*v-1)  # random azimuthal angle between 0 and pi
    r = w**(1/3)*rad  # random radius between 0 and 'rad'
    
    x = r*cos(theta)*sin(phi)  # convert to x,y,z coordinates
    y = r*sin(theta)*sin(phi)
    z = r*cos(phi)
    
    out = array([x, y, z]) + r0  # shift to r0 location
    
    return out


## Seed random points within a plane
def sampleInPlane(X, Y, zs):
    i = randint(0, len(X))  # get random integer
    j = randint(0, len(Y))

    x = X[i]  # place seed in random X,Y location
    y = Y[j]

    out = array([x, y, zs])

    return out
