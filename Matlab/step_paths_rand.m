function out = step_paths_rand(V,h,spread,streams)

% Standard RK4 numerical integration
k1 = vel_interp3(V, streams);
k2 = vel_interp3(V, streams + k1.*h/2);
k3 = vel_interp3(V, streams + k2.*h/2);
k4 = vel_interp3(V, streams + k3.*h);
out = streams + (k1 + 2.*k2 + 2.*k3 + k4).*h/6;

rng(0,'twister'); %make random number generator repeatable
out = out + spread*randn(size(streams));

end
