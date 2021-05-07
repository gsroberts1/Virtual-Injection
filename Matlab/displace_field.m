function Vd = displace_field( V0, dt )
% DISPLACE_FIELD Displaces velocity field forward in time
% This is done to emulate a PC-MRI acquisition. Velocities are encoded at 
% a time prior to position encoding which means spins with velocity travel
% along the flow direction before position is recorded, leading to a
% 'displacement artifact'. These errors are harmful to streamlines.

xrange = 1:size(V0,1); yrange = 1:size(V0,2); zrange = 1:size(V0,3);
[sX, sY, sZ] = ndgrid(xrange, yrange, zrange); %mesh grids for all x,y,z points
seeds = [sX(:) sY(:) sZ(:)]; %make seed points at all voxels

Vtemp = V0; %set dummy velocity field for manipulation

N = 5; %displace in smaller steps
displaced = step_paths(-Vtemp, dt/N, seeds); %initial displace
for i = 1:N-1
    displaced = step_paths(-Vtemp, dt/N, displaced); %continue displace
end

% Find velocity at new forward-displaced position ON OLD VELOCITY GRID.
% This effectively moves our velocity vector forward
Vd = vel_interp3(V0, displaced); 
Vd = reshape(Vd, size(V0)); %reshape into image

end

