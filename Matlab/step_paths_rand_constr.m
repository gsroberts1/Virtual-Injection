function streamlines = step_paths_rand_constr(V,h,spread,cutoff,reducer,streamlines,s,P)
streams = streamlines(:,:,s-1); %current streamline position
if s>=3 %make sure we are at least one away from beginning of stream
    oldpos = streamlines(:,:,s-2); %previous streamline position
end 

% Standard RK4 numerical integration
k1 = vel_interp3(V, streams);
k2 = vel_interp3(V, streams + k1.*h/2);
k3 = vel_interp3(V, streams + k2.*h/2);
k4 = vel_interp3(V, streams + k3.*h);
out = streams + (k1 + 2.*k2 + 2.*k3 + k4).*h/6;

rng(0,'twister'); %make random number generator repeatable
for ind=1:size(streams,1)
    prob = 0; %reset probability to 1
    tries = 0; %reset number of tries
    killFlag = 0; %flag to kill line (if no viable steps are found)
    spreadi = spread;
    cutoffi = cutoff;
    while prob < cutoffi 
        newpos = out(ind,:) + spreadi*randn(1,3); %calculate new random step
        
        %Interpolate single 3D point
        x0 = floor(newpos(1)); y0 = floor(newpos(2)); z0 = floor(newpos(3));
        x1 = ceil(newpos(1)); y1 = ceil(newpos(2)); z1 = ceil(newpos(3));
        dx = newpos(1)-x0; dy = newpos(2)-y0; dz = newpos(3)-z0;
        ddx = 1-dx; ddy = 1-dy; ddz = 1-dz;
        if x0<=0 || y0<=0 || z0 <=0
            prob = 0;
        elseif x1>size(P,1) || y1>size(P,2) || z1>size(P,3)
            prob = 0;
        else 
            prob = ddx*ddy*ddz*P(x0,y0,z0) + dx*ddy*ddz*P(x1,y0,z0) + ...
                ddx*dy*ddz*P(x0,y1,z0) + ddx*ddy*dz*P(x0,y0,z1) + ...
                ddx*dy*dz*P(x0,y1,z1) + dx*ddy*dz*P(x1,y0,z1) + ...
                dx*dy*ddz*P(x1,y1,z0) + dx*dy*dz*P(x1,y1,z1);
        end 
        
        if s>=3 %if we have made at  least two steps
            prob = prob .* KE_prob(oldpos(ind,:), streams(ind,:), newpos); %calculate prob of KE change
        end 
        tries = tries + 1; %we've tried
        if tries == 30 %if we still don't have success...
            cutoffi = cutoffi/reducer; %reduce the probability cutoff
            spreadi = spreadi*reducer; %reduce the Gaussian sampling width
        end 
        if tries == 60 %still no success?
            cutoffi = cutoffi/reducer;
            spreadi = spreadi*reducer;
        end 
        if tries > 90 %give up, no suitable potential steps found
            killFlag = 1;
            break %break from while loop
        end 
    end
    if killFlag
        streamlines(ind,:,s) = streamlines(ind,:,s-1);
    else
        streamlines(ind,:,s) = newpos; %add random step to streamline matrix
    end 
end 

end 

%% Get Probability from kinetic energy (KE) changes
function p = KE_prob(oldpos,pos,newpos)
    % Probability based on % change in KE=1/2mV^2=1/2m|dx/dt|^2
    if length(pos) > 1
        dv1 = pos - oldpos;  %labelled dv not dx because dt will cancel out below
        dv2 = newpos - pos;
        dKE = (dot(dv1, dv1) - dot(dv2, dv2)) ./ dot(dv1, dv1);  %normalized change in KE
        % m, dt, 1/2's cancel out, leaving only dx; dKE=1-(dv2/dv1)^2
        %consider making denominator of dKE = (dot(dv1, dv1) + dot(dv2, dv2))
        if abs(dKE) > 1  
            dKE = 1; %cap dKE at 1
        end 
        p = (1 - abs(dKE)); %probability of a certain change in KE
    end 
end 
