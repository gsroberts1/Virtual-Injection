function VI = vel_interp3(V, r)
% VEL_INTERP3 Velocity interpolation in 3D space
% % Interpolates velocities at new query points (r) using old velocity field

% Mike's old code used compiled C++ for linear 3D interpolation.
% Slightly faster but had issues with newer version of MATLAB; fixed now.
% VI = mirt3D_mexinterp(V,r(:,2),r(:,1),r(:,3));
% VI(isnan(out)) = 0.0;

vx = V(:,:,:,1); %grab velocity fields in x,y,z
vy = V(:,:,:,2);
vz = V(:,:,:,3);
x = 1:size(vx,1); %create vectors for original grid
y = 1:size(vx,2);
z = 1:size(vy,3);

VI(:,1) = interp3(y,x,z,vx,r(:,2),r(:,1),r(:,3),'linear'); %3D interpolate 
VI(:,2) = interp3(y,x,z,vy,r(:,2),r(:,1),r(:,3),'linear');
VI(:,3) = interp3(y,x,z,vz,r(:,2),r(:,1),r(:,3),'linear');
VI(isnan(VI)) = 0.0; %force NaN's to 0


end

