function A = grid3Dpointarray(A,pos,val)
% def grid3Dpointarray(np.ndarray[double, ndim=3] TOA,
%                     np.ndarray[double, ndim=3) r0,
%                     np.ndarray[double, ndim=3) r1,
%                     np.ndarray[double, ndim=3) dr,
%                     np.ndarray[double, ndim=3) ddr,
%                     double val):

for i=1:size(pos,1)
    r0 = floor(pos);
    r1 = ceil(pos);
    dr = pos - r0;
    ddr = 1.0 - dr;
    if ~isnan(r0(i,1))
        A(r0(i,1),r0(i,2),r0(i,3)) = A(r0(i,1),r0(i,2),r0(i,3)) + val*ddr(i,1)*ddr(i,2)*ddr(i,3);
        A(r1(i,1),r0(i,2),r0(i,3)) = A(r1(i,1),r0(i,2),r0(i,3)) + val*dr(i,1)*ddr(i,2)*ddr(i,3);
        A(r0(i,1),r1(i,2),r0(i,3)) = A(r0(i,1),r1(i,2),r0(i,3)) + val*ddr(i,1)*dr(i,2)*ddr(i,3);
        A(r0(i,1),r0(i,2),r1(i,3)) = A(r0(i,1),r0(i,2),r1(i,3)) + val*ddr(i,1)*ddr(i,2)*dr(i,3);
        A(r0(i,1),r1(i,2),r1(i,3)) = A(r0(i,1),r1(i,2),r1(i,3)) + val*ddr(i,1)*dr(i,2)*dr(i,3);
        A(r1(i,1),r0(i,2),r1(i,3)) = A(r1(i,1),r0(i,2),r1(i,3)) + val*dr(i,1)*ddr(i,2)*dr(i,3);
        A(r1(i,1),r1(i,2),r0(i,3)) = A(r1(i,1),r1(i,2),r0(i,3)) + val*dr(i,1)*dr(i,2)*ddr(i,3);
        A(r1(i,1),r1(i,2),r1(i,3)) = A(r1(i,1),r1(i,2),r1(i,3)) + val*dr(i,1)*dr(i,2)*dr(i,3);
    end 
end

