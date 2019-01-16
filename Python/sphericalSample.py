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

def sampleInPlane(CD, VZ, thresh, zs, width=1):
    plane = sum(CD[zs-width:zs+width,:,:],axis=0)
    dplane = sign(sum(VZ[zs-width:zs+width,:,:],axis=0))
    
    plane[plane<=thresh] = 0
    plane[plane>thresh] = 1
    
    plane[dplane<0] = 0
    
    X,Y = nonzero(plane)
    
    x = X[i] + rand()
    y = Y[i] + rand()
    z = zs
    
    i = randint(0, len(X))
    
    out = array([x,y,z])
    
    return out