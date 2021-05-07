%% Initiate
% MASTER SCRIPT FOR IN SILICO (U-BEND PHANTOM) ANALYSIS
clear all; close all; clc

%% U-Bend Phantom
load sten_ubend_1mm.mat
%load patch.mat
%mask = padarray(mask,[10 10 10]);
V = cat(4, Vy_matrix, Vx_matrix, Vz_matrix); %3D velocities (x,y,z)
%V = padarray(V,[10 10 10 0]);
V(isnan(V)) = 0.0; %force NaNs to 0
mask(:,1,:) = [];
V(:,1,:,:) = [];
Venc = max(abs(V(:)))*1.2;
Vmag = sqrt(sum(abs(V.^2),4)); %speed image
clear Vx_matrix Vy_matrix Vz_matrix TKE_matrix

%% Initiate Seeding
slice = 25; %need to be sufficiently upstream to account for displacements
xSectionTop = squeeze(Vmag(slice,1:length(Vmag)/2,:)); %cut slice near inlet
xSectionTopBin = xSectionTop>0; %keep non-zeros (could've just used mask)
%figure; imshow(xSectionTopBin); title('Seeding Region (Cross Section of Inlet)');

[y,z] = ind2sub(size(xSectionTopBin),find(xSectionTopBin)); %get seed coords
x = slice*ones(length(y),1);
seeds = squeeze(cat(3,x,y,z));

%% Displacement Loop (3 displacements)
Td = [2.0, 5.0, 8.0]; %displacement times in ms (TE - moment center time)
for t=1:length(Td)
    Vd(:,:,:,:,t) = displace_field(V, Td(t)); %displaced velocity field

    %% Add Noise Loop (4 SNRs)
    SNR = [5, 25, 50]; %SNR ranges (5,15,40)
    for n=1:length(SNR) %for each SNR value
        [MAGn(:,:,:,n),Vdn(:,:,:,:,t,n),SNRtrue(n)] = addnoise(Vd(:,:,:,:,t), double(mask), SNR(n), Venc);
        [~,Vn(:,:,:,:,t,n),~] = addnoise(V, double(mask), SNR(n), Venc);
        %mask3D = repmat(mask, [1 1 1 3]);
        %Vdn(:,:,:,:,t,n) = Vdn(:,:,:,:,t,n).*mask3D;
        
        %%% Streamline Generator
        N = 400; %number of streamline steps 
        streamlines = zeros([size(seeds) N]); %initialize streamline matrix
        
        %% Original Velocity Field Streamlines
        streamlines = zeros([size(seeds) N]);
        streamlines(:,:,1) = seeds;
        for s = 2:N
            streamlines(:,:,s) = step_paths(Vn(:,:,:,:,t,n).*mask, 3, streamlines(:,:,s-1));
        end
        streamlines = checkoob(streamlines,mask);
        plot_streams(streamlines, Vmag, ['Grount Truth - Td=' num2str(Td(t))])
        streamlinesGT(:,:,:,t,n) = streamlines;
        
        %% Displaced streamlines with noise 
        streamlines(:,:,1) = seeds; %place seed points at streamline start
        for s = 2:N %for each iteration, step along path
            streamlines(:,:,s) = step_paths(Vdn(:,:,:,:,t,n).*mask, 3, streamlines(:,:,s-1));
        end
        streamlines = checkoob(streamlines,mask); %check if out of bounds
        plot_streams(streamlines, Vmag, ['Displaced - Td=' num2str(Td(t)) ' ms - SNR=' num2str(SNR(n))]);
        streamlinesD(:,:,:,t,n) = streamlines; %put in master matrix
        
        %% Single-step displacement correction streamlines (Steinman et al)
        V_SSDC(:,:,:,:,t,n) = ssDC(Vdn(:,:,:,:,t,n), Td(t)); %correct field
        streamlines = zeros([size(seeds) N]);
        streamlines(:,:,1) = seeds;
        for s = 2:N
            streamlines(:,:,s) = step_paths(V_SSDC(:,:,:,:,t,n).*mask, 3, streamlines(:,:,s-1));
        end
        streamlines = checkoob(streamlines,mask);
        plot_streams(streamlines, Vmag, ['ssDC - Td=' num2str(Td(t)) ' ms - SNR=' num2str(SNR(n))]);
        streamlinesSSDC(:,:,:,t,n) = streamlines;
        
        %% Iterative displacement correction streamlines (Thunberg et al)
        n_iter = 12;
        V_IDC(:,:,:,:,t,n) = iDC(Vdn(:,:,:,:,t,n).*mask, Td(t), n_iter);
        streamlines = zeros([size(seeds) N]);
        streamlines(:,:,1) = seeds;
        for s = 2:N
            streamlines(:,:,s) = step_paths(V_IDC(:,:,:,:,t,n), 3, streamlines(:,:,s-1));
        end
        streamlines = checkoob(streamlines,mask);
        plot_streams(streamlines, Vmag, ['iDC - Td=' num2str(Td(t)) ' ms - SNR=' num2str(SNR(n))])
        streamlinesIDC(:,:,:,t,n) = streamlines;
        
        %% Modified iterative displacement correction streamlines
%         n_iter = 10;
%         V_MIDC(:,:,:,:,t,n) = miDC(Vdn(:,:,:,:,t,n), Td(t), n_iter);
%         streamlines = zeros([size(seeds) N]);
%         streamlines(:,:,1) = seeds;
%         for s = 2:N
%             streamlines(:,:,s) = step_paths(V_MIDC(:,:,:,:,t,n), 3, streamlines(:,:,s-1));
%         end
%         streamlines = checkoob(streamlines,mask);
%         plot_streams(streamlines, Vmag, ['miDC - Td=' num2str(Td(t)) ' ms - SNR=' num2str(SNR(n))])
%         streamlinesMIDC(:,:,:,t,n) = streamlines;
    end 
end 

plane1 = 102; %first plane at 0 degrees (x value)
plane2 = 66; %second plane at 90 degrees (y value)
plane3 = 102; %third plane at 180 degrees (x value) (before stenosis)
plane4 = slice; %fourth plane past outlet (x value)

for t=1:length(Td)
    for n=1:length(SNR) 
        % Analyze ground-truth images (velocity field with noise)
        [pctPass1(t,n,1),pctPass2(t,n,1),pctPass3(t,n,1),pctPass4(t,n,1)] ...
        = checkPlaneCrossings(streamlinesGT(:,:,:,t,n),plane1,plane2,plane3,plane4);  
        meanLength(t,n,1) = mean(line_lengths(streamlinesGT(:,:,:,t,n)));
        RMSE(t,n,1) = vrmse(Vn(:,:,:,:,t,n), V, mask);
        RMSE_angle(t,n,1) = vrmse_angle(Vn(:,:,:,:,t,n), V, mask);
        RMSE_mag(t,n,1) = vrmse_mag(Vn(:,:,:,:,t,n), V, mask);
        
        % Analyze displaced images (with noise)
        [pctPass1(t,n,2),pctPass2(t,n,2),pctPass3(t,n,2),pctPass4(t,n,2)] ...
        = checkPlaneCrossings(streamlinesD(:,:,:,t,n),plane1,plane2,plane3,plane4);  
        meanLength(t,n,2) = mean(line_lengths(streamlinesD(:,:,:,t,n)));
        RMSE(t,n,2) = vrmse(Vdn(:,:,:,:,t,n), V, mask);
        RMSE_angle(t,n,2) = vrmse_angle(Vdn(:,:,:,:,t,n), V, mask);
        RMSE_mag(t,n,2) = vrmse_mag(Vdn(:,:,:,:,t,n), V, mask);
        
        % Analyze ssDC correction
        [pctPass1(t,n,3),pctPass2(t,n,3),pctPass3(t,n,3),pctPass4(t,n,3)] ...
        = checkPlaneCrossings(streamlinesSSDC(:,:,:,t,n),plane1,plane2,plane3,plane4);    
        meanLength(t,n,3) = mean(line_lengths(streamlinesSSDC(:,:,:,t,n)));
        RMSE(t,n,3) = vrmse(V_SSDC(:,:,:,:,t,n), V, mask);
        RMSE_angle(t,n,3) = vrmse_angle(V_SSDC(:,:,:,:,t,n), V, mask);
        RMSE_mag(t,n,3) = vrmse_mag(V_SSDC(:,:,:,:,t,n), V, mask);
        
        % Analyze iDC correction
        [pctPass1(t,n,4),pctPass2(t,n,4),pctPass3(t,n,4),pctPass4(t,n,4)] ...
        = checkPlaneCrossings(streamlinesIDC(:,:,:,t,n),plane1,plane2,plane3,plane4);  
        meanLength(t,n,4) = mean(line_lengths(streamlinesIDC(:,:,:,t,n)));
        RMSE(t,n,4) = vrmse(V_IDC(:,:,:,:,t,n), V, mask);
        RMSE_angle(t,n,4) = vrmse_angle(V_IDC(:,:,:,:,t,n), V, mask);
        RMSE_mag(t,n,4) = vrmse_mag(V_IDC(:,:,:,:,t,n), V, mask);
        
        % Analyze miDC correction
%         [pctPass1(t,n,5),pctPass2(t,n,5),pctPass3(t,n,5),pctPass4(t,n,5)] ...
%         = checkPlaneCrossings(streamlinesMIDC(:,:,:,t,n),plane1,plane2,plane3,plane4);  
%         meanLength(t,n,5) = mean(line_lengths(streamlinesMIDC(:,:,:,t,n)));
%         RMSE(t,n,5) = vrmse(V_MIDC(:,:,:,:,t,n), V, mask);
%         RMSE_angle(t,n,5) = vrmse_angle(V_MIDC(:,:,:,:,t,n), V, mask);
%         RMSE_mag(t,n,5) = vrmse_mag(V_MIDC(:,:,:,:,t,n), V, mask);
    end 
end 

clear x y z s N n_iter xSectionTop xSectionTopBin seq_param 

%patchLoc = [111 1 10; 150 40 10];
%makeQuiverPlot(Vd,mask,patchLoc',3);
%figure; quiver(V(:,:,20,2), V(:,:,20,1)); title('Ground Truth');
%figure; quiver(Vdn(:,:,20,2,1,1), Vdn(:,:,20,1,1,1)); title('Displaced');
%figure; quiver(V_SSDC(:,:,20,2,1,1), V_SSDC(:,:,20,1,1,1)); title('SSDC');
%figure; quiver(V_MIDC(:,:,20,2,1,1), V_MIDC(:,:,20,1,1,1)); title('MIDC');