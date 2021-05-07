function out = step_paths( V, h, seeds )
% STEP_PATHS Take physical step along velocity field to get new position
% % Numerical integration: Runge-Kutta 4th order method 

%RK4
k1 = vel_interp3(V, seeds); %velocity(dr/dt) at r0
k2 = vel_interp3(V, seeds + k1.*h/2); %velocity at position= r0 + k1*h/2
k3 = vel_interp3(V, seeds + k2.*h/2); %velocity at position = r0 + k2*h/2
k4 = vel_interp3(V, seeds + k3.*h); %velocity at position = r0 + k3*h
out = seeds + (k1 + 2.*k2 + 2.*k3 + k4).*h/6; %get weighted average slopes

end

