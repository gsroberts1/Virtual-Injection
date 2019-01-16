from pylab import *

def sampleInSphere(rad,r0):
    u = rand()
    v = rand()
    w = rand()
    
    theta = 2*pi*u
    phi = arccos(2*v-1)
    r = w**(1/3)*rad
    
    x = r*cos(theta)*sin(phi)
    y = r*sin(theta)*sin(phi)
    z = r*cos(phi)
    
    out = array([x,y,z]) + r0
    
    return out

def sampleInPlane(X,Y,zs):
    
    i = randint(0, len(X))
    
    x = X[i] + rand()
    y = Y[i] + rand()
    z = zs
    
    out = array([z,x,y])
    
    return out