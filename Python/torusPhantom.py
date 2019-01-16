from pylab import *

def torusPhantom(imsize=128, offset=0.0):
    grid_ref = linspace(-1, 1, imsize)
    Z, Y, X = meshgrid(grid_ref, grid_ref, grid_ref, indexing='ij')
    R = sqrt(X**2 + Y**2)
    outer_radius = 0.6
    Rr = abs(R-outer_radius)
    Rrz = sqrt(Rr**2 + Z**2)
    
    radius = .12
    VES = zeros(Rrz.shape)
    VES[Rrz<radius] = 1
    
    VEL = -Rrz**2 + radius**2
    VEL = VEL*VES
    #VEL = VES
    
    ANG = arctan2(Y,X)
    VX = VEL*-sin(ANG+offset)
    VY = VEL*cos(ANG+offset)
    VZ = zeros(VY.shape)
    
    Ra = sqrt(X**2 + Y**2 + Z**2)
    MAG = zeros(Ra.shape)
    MAG[Ra < .9] = 1
    MAG = MAG+VES
    
    venc = 1.3*VEL.max()
        
    IM0 = zeros((imsize, imsize, imsize, 3),dtype=complex128)
    IM0[:,:,:,0] = MAG*exp(1j*pi*VZ/venc)
    IM0[:,:,:,1] = MAG*exp(1j*pi*VY/venc)
    IM0[:,:,:,2] = MAG*exp(1j*pi*VX/venc)
    
    return (IM0, VX, VY, VZ)