function Vc = iDC(Vd, dt0, n_iter)
% IDC Iterative displacement correction for correcting displaced velocities
% See: Thunberg P, Wigstrom L, Ebbers T, Karlsson M. JMRI, 2002;16(5):591-597.

xrange = 1:size(Vd,1); yrange = 1:size(Vd,2); zrange = 1:size(Vd,3);
[sX, sY, sZ] = ndgrid(xrange, yrange, zrange); %mesh grids for all x,y,z points
seeds = [sX(:), sY(:), sZ(:)]; %make seed points at all voxels

Vc = Vd; %make space for corrected velocities
for j = 1:n_iter
    N = 3;
    displaced = step_paths(Vc, dt0/N, seeds); %displace from original seeds
    for n = 1:N-1
        displaced = step_paths(Vc, dt0/N, displaced); %displace from original seeds
    end 
    Vc = vel_interp3(Vd, displaced); %get updated velocity from corrected velocity map
    Vc = reshape(Vc, size(Vd)); %reshape to image
end

end

