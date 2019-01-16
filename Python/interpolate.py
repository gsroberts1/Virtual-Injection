from pylab import *

def interpolate3Dpoint(A,r):
    x0 = floor(r[0])
    y0 = floor(r[1])
    z0 = floor(r[2])
    x1 = ceil(r[0])
    y1 = ceil(r[1])
    z1 = ceil(r[2])
    
    dx = r[0]-x0
    dy = r[1]-y0
    dz = r[2]-z0
    
    out = (1-dx)*(1-dy)*(1-dz)*A[x0,y0,z0] + \
          dx*(1-dy)*(1-dz)*A[x1,y0,z0] + \
          (1-dx)*dy*(1-dz)*A[x0,y1,z0] + \
          (1-dx)*(1-dy)*dz*A[x0,y0,z1] + \
          (1-dx)*dy*dz*A[x0,y1,z1] + \
          dx*(1-dy)*dz*A[x1,y0,z1] + \
          dx*dy*(1-dz)*A[x1,y1,z0] + \
          dx*dy*dz*A[x1,y1,z1]
    
    return out

def grid3Dpoint(A,r,val):
    x0 = floor(r[0])
    y0 = floor(r[1])
    z0 = floor(r[2])
    x1 = ceil(r[0])
    y1 = ceil(r[1])
    z1 = ceil(r[2])
    
    dx = r[0]-x0
    dy = r[1]-y0
    dz = r[2]-z0
    
    A[x0,y0,z0] = A[x0,y0,z0] + val*(1-dx)*(1-dy)*(1-dz)
    A[x1,y0,z0] = A[x1,y0,z0] + val*dx*(1-dy)*(1-dz)
    A[x0,y1,z0] = A[x0,y1,z0] + val*(1-dx)*dy*(1-dz)
    A[x0,y0,z1] = A[x0,y0,z1] + val*(1-dx)*(1-dy)*dz
    A[x0,y1,z1] = A[x0,y1,z1] + val*(1-dx)*dy*dz
    A[x1,y0,z1] = A[x1,y0,z1] + val*dx*(1-dy)*dz
    A[x1,y1,z0] = A[x1,y1,z0] + val*dx*dy*(1-dz)
    A[x1,y1,z1] = A[x1,y1,z1] + val*dx*dy*dz

def interpolate3D3Dpoint(A,r):
    x0 = floor(r[0])
    y0 = floor(r[1])
    z0 = floor(r[2])
    x1 = ceil(r[0])
    y1 = ceil(r[1])
    z1 = ceil(r[2])
    
    dx = r[0]-x0
    dy = r[1]-y0
    dz = r[2]-z0
    
    out = zeros(3)
    
    out[0] = (1-dx)*(1-dy)*(1-dz)*A[x0,y0,z0,0] + \
          dx*(1-dy)*(1-dz)*A[x1,y0,z0,0] + \
          (1-dx)*dy*(1-dz)*A[x0,y1,z0,0] + \
          (1-dx)*(1-dy)*dz*A[x0,y0,z1,0] + \
          (1-dx)*dy*dz*A[x0,y1,z1,0] + \
          dx*(1-dy)*dz*A[x1,y0,z1,0] + \
          dx*dy*(1-dz)*A[x1,y1,z0,0] + \
          dx*dy*dz*A[x1,y1,z1,0]
    
    out[1] = (1-dx)*(1-dy)*(1-dz)*A[x0,y0,z0,1] + \
          dx*(1-dy)*(1-dz)*A[x1,y0,z0,1] + \
          (1-dx)*dy*(1-dz)*A[x0,y1,z0,1] + \
          (1-dx)*(1-dy)*dz*A[x0,y0,z1,1] + \
          (1-dx)*dy*dz*A[x0,y1,z1,1] + \
          dx*(1-dy)*dz*A[x1,y0,z1,1] + \
          dx*dy*(1-dz)*A[x1,y1,z0,1] + \
          dx*dy*dz*A[x1,y1,z1,1]
    
    out[2] = (1-dx)*(1-dy)*(1-dz)*A[x0,y0,z0,2] + \
          dx*(1-dy)*(1-dz)*A[x1,y0,z0,2] + \
          (1-dx)*dy*(1-dz)*A[x0,y1,z0,2] + \
          (1-dx)*(1-dy)*dz*A[x0,y0,z1,2] + \
          (1-dx)*dy*dz*A[x0,y1,z1,2] + \
          dx*(1-dy)*dz*A[x1,y0,z1,2] + \
          dx*dy*(1-dz)*A[x1,y1,z0,2] + \
          dx*dy*dz*A[x1,y1,z1,2]
    
    return out

def interpolate3D3Dpointarray(A,r0, r1, dr, ddr):    
    
    out = zeros(r0.shape)
    
    for i in range(r0.shape[0]):
    
        out[i,0] = ddr[i,0]*ddr[i,1]*ddr[i,2]*A[r0[i,0],r0[i,1],r0[i,2],0] + \
              dr[i,0]*ddr[i,1]*ddr[i,2]*A[r1[i,0],r0[i,1],r0[i,2],0] + \
              ddr[i,0]*dr[i,1]*ddr[i,2]*A[r0[i,0],r1[i,1],r0[i,2],0] + \
              ddr[i,0]*ddr[i,1]*dr[i,2]*A[r0[i,0],r0[i,1],r1[i,2],0] + \
              ddr[i,0]*dr[i,1]*dr[i,2]*A[r0[i,0],r1[i,1],r1[i,2],0] + \
              dr[i,0]*ddr[i,1]*dr[i,2]*A[r1[i,0],r0[i,1],r1[i,2],0] + \
              dr[i,0]*dr[i,1]*ddr[i,2]*A[r1[i,0],r1[i,1],r0[i,2],0] + \
              dr[i,0]*dr[i,1]*dr[i,2]*A[r1[i,0],r1[i,1],r1[i,2],0]
        
        out[i,1] = ddr[i,0]*ddr[i,1]*ddr[i,2]*A[r0[i,0],r0[i,1],r0[i,2],1] + \
              dr[i,0]*ddr[i,1]*ddr[i,2]*A[r1[i,0],r0[i,1],r0[i,2],1] + \
              ddr[i,0]*dr[i,1]*ddr[i,2]*A[r0[i,0],r1[i,1],r0[i,2],1] + \
              ddr[i,0]*ddr[i,1]*dr[i,2]*A[r0[i,0],r0[i,1],r1[i,2],1] + \
              ddr[i,0]*dr[i,1]*dr[i,2]*A[r0[i,0],r1[i,1],r1[i,2],1] + \
              dr[i,0]*ddr[i,1]*dr[i,2]*A[r1[i,0],r0[i,1],r1[i,2],1] + \
              dr[i,0]*dr[i,1]*ddr[i,2]*A[r1[i,0],r1[i,1],r0[i,2],1] + \
              dr[i,0]*dr[i,1]*dr[i,2]*A[r1[i,0],r1[i,1],r1[i,2],1]
        
        out[i,2] = ddr[i,0]*ddr[i,1]*ddr[i,2]*A[r0[i,0],r0[i,1],r0[i,2],2] + \
              dr[i,0]*ddr[i,1]*ddr[i,2]*A[r1[i,0],r0[i,1],r0[i,2],2] + \
              ddr[i,0]*dr[i,1]*ddr[i,2]*A[r0[i,0],r1[i,1],r0[i,2],2] + \
              ddr[i,0]*ddr[i,1]*dr[i,2]*A[r0[i,0],r0[i,1],r1[i,2],2] + \
              ddr[i,0]*dr[i,1]*dr[i,2]*A[r0[i,0],r1[i,1],r1[i,2],2] + \
              dr[i,0]*ddr[i,1]*dr[i,2]*A[r1[i,0],r0[i,1],r1[i,2],2] + \
              dr[i,0]*dr[i,1]*ddr[i,2]*A[r1[i,0],r1[i,1],r0[i,2],2] + \
              dr[i,0]*dr[i,1]*dr[i,2]*A[r1[i,0],r1[i,1],r1[i,2],2]
    
    return out