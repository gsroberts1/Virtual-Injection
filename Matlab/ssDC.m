function Vc = ssDC(Vd, dt)
% SSDC Single-step displacement correction for correcting velocity fields.
% See: Steinman DA, Ethier CR, Rutt BK. JMRI, 1997;7(2):339-346.

xrange = 1:size(Vd,1); yrange = 1:size(Vd,2); zrange = 1:size(Vd,3);
[sX, sY, sZ] = ndgrid(xrange, yrange, zrange); %mesh grids for all x,y,z points
seeds = [sX(:), sY(:), sZ(:)]; %make seed points at all voxels

displaced = step_paths(Vd, dt, seeds); %take full step back
Vc = vel_interp3(Vd, displaced); %get updated velocity from old velocity map
Vc = reshape(Vc, size(Vd)); %reshape to image

end

