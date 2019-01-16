import cython

import numpy as np
cimport numpy as np

cdef extern from "math.h":
    double floor(double num)
    double ceil(double num)

@cython.boundscheck(False)
@cython.wraparound(False)
def interpolate3Dpoint(np.ndarray[double, ndim=3] A,
                       np.ndarray[double, ndim=1] r):

    
    cdef int x0 = <int>floor(r[0])
    cdef int y0 = <int>floor(r[1])
    cdef int z0 = <int>floor(r[2])
    cdef int x1 = <int>ceil(r[0])
    cdef int y1 = <int>ceil(r[1])
    cdef int z1 = <int>ceil(r[2])
    
    cdef double dx = r[0]-x0
    cdef double dy = r[1]-y0
    cdef double dz = r[2]-z0
    
    cdef double ddx = (<double>1.0-dx)
    cdef double ddy = (<double>1.0-dy)
    cdef double ddz = (<double>1.0-dz)
    
    
    cdef double out = ddx*ddy*ddz*A[x0,y0,z0] + \
          dx*ddy*ddz*A[x1,y0,z0] + \
          ddx*dy*ddz*A[x0,y1,z0] + \
          ddx*ddy*dz*A[x0,y0,z1] + \
          ddx*dy*dz*A[x0,y1,z1] + \
          dx*ddy*dz*A[x1,y0,z1] + \
          dx*dy*ddz*A[x1,y1,z0] + \
          dx*dy*dz*A[x1,y1,z1]
    
    return out

@cython.boundscheck(False)
@cython.wraparound(False)
def grid3Dpoint(np.ndarray[double, ndim=3] A,
                np.ndarray[double, ndim=1] r,
                double val):
    
    cdef int x0 = <int>floor(r[0])
    cdef int y0 = <int>floor(r[1])
    cdef int z0 = <int>floor(r[2])
    cdef int x1 = <int>ceil(r[0])
    cdef int y1 = <int>ceil(r[1])
    cdef int z1 = <int>ceil(r[2])
    
    cdef double dx = r[0]-x0
    cdef double dy = r[1]-y0
    cdef double dz = r[2]-z0
    
    cdef double ddx = (<double>1.0-dx)
    cdef double ddy = (<double>1.0-dy)
    cdef double ddz = (<double>1.0-dz)
    
    A[x0,y0,z0] = A[x0,y0,z0] + val*ddx*ddy*ddz
    A[x1,y0,z0] = A[x1,y0,z0] + val*dx*ddy*ddz
    A[x0,y1,z0] = A[x0,y1,z0] + val*ddx*dy*ddz
    A[x0,y0,z1] = A[x0,y0,z1] + val*ddx*ddy*dz
    A[x0,y1,z1] = A[x0,y1,z1] + val*ddx*dy*dz
    A[x1,y0,z1] = A[x1,y0,z1] + val*dx*ddy*dz
    A[x1,y1,z0] = A[x1,y1,z0] + val*dx*dy*ddz
    A[x1,y1,z1] = A[x1,y1,z1] + val*dx*dy*dz

@cython.boundscheck(False)
@cython.wraparound(False)
def grid3Dpointarray(np.ndarray[double, ndim=3] A,
                    np.ndarray[double, ndim=2] r0,
                    np.ndarray[double, ndim=2] r1,
                    np.ndarray[double, ndim=2] dr,
                    np.ndarray[double, ndim=2] ddr,
                    double val):
    
    for i in range(r0.shape[0]):
        
        A[<int>r0[i,0],<int>r0[i,1],<int>r0[i,2]] = A[<int>r0[i,0],<int>r0[i,1],<int>r0[i,2]] + val*ddr[i,0]*ddr[i,1]*ddr[i,2]
        
        A[<int>r1[i,0],<int>r0[i,1],<int>r0[i,2]] = A[<int>r1[i,0],<int>r0[i,1],<int>r0[i,2]] + val*dr[i,0]*ddr[i,1]*ddr[i,2]
        A[<int>r0[i,0],<int>r1[i,1],<int>r0[i,2]] = A[<int>r0[i,0],<int>r1[i,1],<int>r0[i,2]] + val*ddr[i,0]*dr[i,1]*ddr[i,2]
        A[<int>r0[i,0],<int>r0[i,1],<int>r1[i,2]] = A[<int>r0[i,0],<int>r0[i,1],<int>r1[i,2]] + val*ddr[i,0]*ddr[i,1]*dr[i,2]
        
        A[<int>r0[i,0],<int>r1[i,1],<int>r1[i,2]] = A[<int>r0[i,0],<int>r1[i,1],<int>r1[i,2]] + val*ddr[i,0]*dr[i,1]*dr[i,2]
        A[<int>r1[i,0],<int>r0[i,1],<int>r1[i,2]] = A[<int>r1[i,0],<int>r0[i,1],<int>r1[i,2]] + val*dr[i,0]*ddr[i,1]*dr[i,2]
        A[<int>r1[i,0],<int>r1[i,1],<int>r0[i,2]] = A[<int>r1[i,0],<int>r1[i,1],<int>r0[i,2]] + val*dr[i,0]*dr[i,1]*ddr[i,2]
        
        A[<int>r1[i,0],<int>r1[i,1],<int>r1[i,2]] = A[<int>r1[i,0],<int>r1[i,1],<int>r1[i,2]] + val*dr[i,0]*dr[i,1]*dr[i,2]
        

@cython.boundscheck(False)
@cython.wraparound(False)
def interpolate3D3Dpoint(np.ndarray[double, ndim=4] A,
                         np.ndarray[double, ndim=1] r):
    
    cdef int x0 = <int>floor(r[0])
    cdef int y0 = <int>floor(r[1])
    cdef int z0 = <int>floor(r[2])
    cdef int x1 = <int>ceil(r[0])
    cdef int y1 = <int>ceil(r[1])
    cdef int z1 = <int>ceil(r[2])
    
    cdef double dx = r[0]-x0
    cdef double dy = r[1]-y0
    cdef double dz = r[2]-z0
    
    cdef double ddx = (<double>1.0-dx)
    cdef double ddy = (<double>1.0-dy)
    cdef double ddz = (<double>1.0-dz)
    
    cdef np.ndarray[double] out = np.zeros(3)
    
    out[0] = ddx*ddy*ddz*A[x0,y0,z0,0] + \
          dx*ddy*ddz*A[x1,y0,z0,0] + \
          ddx*dy*ddz*A[x0,y1,z0,0] + \
          ddx*ddy*dz*A[x0,y0,z1,0] + \
          ddx*dy*dz*A[x0,y1,z1,0] + \
          dx*ddy*dz*A[x1,y0,z1,0] + \
          dx*dy*ddz*A[x1,y1,z0,0] + \
          dx*dy*dz*A[x1,y1,z1,0]
    
    out[1] = ddx*ddy*ddz*A[x0,y0,z0,1] + \
          dx*ddy*ddz*A[x1,y0,z0,1] + \
          ddx*dy*ddz*A[x0,y1,z0,1] + \
          ddx*ddy*dz*A[x0,y0,z1,1] + \
          ddx*dy*dz*A[x0,y1,z1,1] + \
          dx*ddy*dz*A[x1,y0,z1,1] + \
          dx*dy*ddz*A[x1,y1,z0,1] + \
          dx*dy*dz*A[x1,y1,z1,1]
    
    out[2] = ddx*ddy*ddz*A[x0,y0,z0,2] + \
          dx*ddy*ddz*A[x1,y0,z0,2] + \
          ddx*dy*ddz*A[x0,y1,z0,2] + \
          ddx*ddy*dz*A[x0,y0,z1,2] + \
          ddx*dy*dz*A[x0,y1,z1,2] + \
          dx*ddy*dz*A[x1,y0,z1,2] + \
          dx*dy*ddz*A[x1,y1,z0,2] + \
          dx*dy*dz*A[x1,y1,z1,2]
    
    return out

@cython.boundscheck(False)
@cython.wraparound(False)
def interpolate3D3Dpointarray(np.ndarray[double, ndim=4] A,
                              np.ndarray[double, ndim=2] r0,
                              np.ndarray[double, ndim=2] r1,
                              np.ndarray[double, ndim=2] dr,
                              np.ndarray[double, ndim=2] ddr):    
    
    cdef np.ndarray[double, ndim=2] out = np.zeros((r0.shape[0], r0.shape[1]))
    
    for i in range(r0.shape[0]):
    
        out[i,0] = ddr[i,0]*ddr[i,1]*ddr[i,2]*A[<int>r0[i,0],<int>r0[i,1],<int>r0[i,2],0] + \
              dr[i,0]*ddr[i,1]*ddr[i,2]*A[<int>r1[i,0],<int>r0[i,1],<int>r0[i,2],0] + \
              ddr[i,0]*dr[i,1]*ddr[i,2]*A[<int>r0[i,0],<int>r1[i,1],<int>r0[i,2],0] + \
              ddr[i,0]*ddr[i,1]*dr[i,2]*A[<int>r0[i,0],<int>r0[i,1],<int>r1[i,2],0] + \
              ddr[i,0]*dr[i,1]*dr[i,2]*A[<int>r0[i,0],<int>r1[i,1],<int>r1[i,2],0] + \
              dr[i,0]*ddr[i,1]*dr[i,2]*A[<int>r1[i,0],<int>r0[i,1],<int>r1[i,2],0] + \
              dr[i,0]*dr[i,1]*ddr[i,2]*A[<int>r1[i,0],<int>r1[i,1],<int>r0[i,2],0] + \
              dr[i,0]*dr[i,1]*dr[i,2]*A[<int>r1[i,0],<int>r1[i,1],<int>r1[i,2],0]
        
        out[i,1] = ddr[i,0]*ddr[i,1]*ddr[i,2]*A[<int>r0[i,0],<int>r0[i,1],<int>r0[i,2],1] + \
              dr[i,0]*ddr[i,1]*ddr[i,2]*A[<int>r1[i,0],<int>r0[i,1],<int>r0[i,2],1] + \
              ddr[i,0]*dr[i,1]*ddr[i,2]*A[<int>r0[i,0],<int>r1[i,1],<int>r0[i,2],1] + \
              ddr[i,0]*ddr[i,1]*dr[i,2]*A[<int>r0[i,0],<int>r0[i,1],<int>r1[i,2],1] + \
              ddr[i,0]*dr[i,1]*dr[i,2]*A[<int>r0[i,0],<int>r1[i,1],<int>r1[i,2],1] + \
              dr[i,0]*ddr[i,1]*dr[i,2]*A[<int>r1[i,0],<int>r0[i,1],<int>r1[i,2],1] + \
              dr[i,0]*dr[i,1]*ddr[i,2]*A[<int>r1[i,0],<int>r1[i,1],<int>r0[i,2],1] + \
              dr[i,0]*dr[i,1]*dr[i,2]*A[<int>r1[i,0],<int>r1[i,1],<int>r1[i,2],1]
        
        out[i,2] = ddr[i,0]*ddr[i,1]*ddr[i,2]*A[<int>r0[i,0],<int>r0[i,1],<int>r0[i,2],2] + \
              dr[i,0]*ddr[i,1]*ddr[i,2]*A[<int>r1[i,0],<int>r0[i,1],<int>r0[i,2],2] + \
              ddr[i,0]*dr[i,1]*ddr[i,2]*A[<int>r0[i,0],<int>r1[i,1],<int>r0[i,2],2] + \
              ddr[i,0]*ddr[i,1]*dr[i,2]*A[<int>r0[i,0],<int>r0[i,1],<int>r1[i,2],2] + \
              ddr[i,0]*dr[i,1]*dr[i,2]*A[<int>r0[i,0],<int>r1[i,1],<int>r1[i,2],2] + \
              dr[i,0]*ddr[i,1]*dr[i,2]*A[<int>r1[i,0],<int>r0[i,1],<int>r1[i,2],2] + \
              dr[i,0]*dr[i,1]*ddr[i,2]*A[<int>r1[i,0],<int>r1[i,1],<int>r0[i,2],2] + \
              dr[i,0]*dr[i,1]*dr[i,2]*A[<int>r1[i,0],<int>r1[i,1],<int>r1[i,2],2]
    
    return out