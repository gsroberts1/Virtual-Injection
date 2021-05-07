function RMSE = vrmse_angle(V, Vref, mask)
% VRMSE Velocity root mean square error 
% Computes root mean square error (RMSE) of velocity field and ground truth
    mask = imerode(mask,strel('sphere',2)); %erode mask to remove edges
    mask = repmat(mask, [1 1 1 3]); %replicate mask for x,y,z
    mask(1:10,1:20,:,:) = 0;
    mask(1,:,:,:) = 0; mask(end,:,:,:) = 0;
    mask(:,1,:,:) = 0; mask(:,end,:,:) = 0;
    mask(:,:,1,:) = 0; mask(:,:,end,:) = 0;
    
    V = V .* mask; %mask new velocities outside of vessel
    Vref = Vref .* mask; %mask references velocities
    
    Vs = reshape(V,[],3); %reshape in x,y,z vectors
    Vrefs = reshape(Vref,[],3);
    %angle = rad2deg(acos(dot(y, x) / (norm(y) * norm(x))))-90;
    angle = rad2deg(atan2(vecnorm(cross(Vs',Vrefs')), dot(Vs',Vrefs')));
    RMSE = sqrt(mean(angle.^2)); 
end

