%% Initiate
% MASTER SCRIPT FOR IN VIVO VIRTUAL INJECTION ANALYSIS
clear all; close all; clc

%% U-Bend Phantom
%[V,MAG,CD] = loadPCVIPR('E:\InjectionPaper\100913_rawImages');
load vivo_AVM1.mat

CD = CD./max(CD(:)); %normalize complex difference
V = V*(320/220); %convert to pixels/ms
threshLow = 0.11; %threshold below=0
threshHigh = 0.25; %threshold above =1
mask = CD>threshLow;
P = CD.*mask;
P(P>threshHigh) = threshHigh;
P = P./max(P(:)); %normalized probability (for 'step_paths_rand.m')
Vmag = sqrt(sum(abs(V.^2),4)); %speed image

%% Initiate Seeding
% slice = size(CD,3)-10; %need to be sufficiently upstream to account for displacements
% sliceForROI = mask(:,:,slice);
% figure; imshow(sliceForROI,[]);
% 
% circ = drawcircle;
% radius = circ.Radius; %get radius of circle
% center = round(circ.Center); %get center coordinates
% [X,Y] = ndgrid(1:size(sliceForROI,1),1:size(sliceForROI,2));
% X = X-center(2); %shift coordinate grid
% Y = Y-center(1);
% roiMask1 = sqrt(X.^2+Y.^2)<=radius; %anything outside radius is ignored
% roiMask1 = imdilate(roiMask1,strel('disk',1)).*mask(:,:,slice); %blow up
% 
% circ = drawcircle;
% radius = circ.Radius; %get radius of circle
% center = round(circ.Center); %get center coordinates
% [X,Y] = ndgrid(1:size(sliceForROI,1),1:size(sliceForROI,2));
% X = X-center(2); %shift coordinate grid
% Y = Y-center(1);
% roiMask2 = sqrt(X.^2+Y.^2)<=radius; %anything outside radius is ignored
% roiMask2 = imdilate(roiMask2,strel('disk',1)).*mask(:,:,slice);
% 
% roiMask = roiMask1 + roiMask2;
% [x,y] = ind2sub(size(roiMask),find(roiMask)); %get seed coords
% 
% X = repmat(x,1,3);
% Y = repmat(y,1,3);
% Z = [(slice+1)*ones(length(y),1), slice*ones(length(y),1), (slice-1)*ones(length(y),1)];
% %z = slice*ones(length(y),1);
% %seeds = squeeze(cat(3,x,y,z));
% seeds = squeeze(cat(3,X(:),Y(:),Z(:)));

%% Displacement Loop (3 displacements)
Td = 2.6; %displacement times in ms (TE - moment center time)
for t=1:length(Td)
    %%% Streamline Generator
    N = 1000; %number of streamline steps
%     streamlines = zeros([size(seeds) N]);

    % Single-step displacement correction streamlines (Steinman et al)
%     V_SSDC(:,:,:,:,t) = ssDC(V, Td(t)); %correct 
%     streamlines = zeros([size(seeds) N]); %initialize streamlines matrix
%     streamlines(:,:,1) = seeds; %place seed points at streamline start
%     for s = 2:N
%         streamlines(:,:,s) = step_paths(V_SSDC(:,:,:,:,t), Td(t), streamlines(:,:,s-1));
%     end
%     streamlines = checkoob(streamlines,mask); %check if out of bounds
%     plot_streams(streamlines, CD, ['ssDC - Td=' num2str(Td(t)) ' ms']);
%     streamlinesSSDC(:,:,:,t) = streamlines; %add to master matrix

    % Iterative displacement correction streamlines (Thunberg et al)
%     n_iter = 10;
%     V_IDC(:,:,:,:,t) = iDC(V, Td(t), n_iter);
%     streamlines = zeros([size(seeds) N]);
%     streamlines(:,:,1) = seeds;
%     for s = 2:N
%         streamlines(:,:,s) = step_paths(V_IDC(:,:,:,:,t), Td(t), streamlines(:,:,s-1));
%     end
%     streamlines = checkoob(streamlines,mask);
%     plot_streams(streamlines, CD, ['iDC - Td=' num2str(Td(t)) ' ms'])
%     streamlinesIDC(:,:,:,t) = streamlines;

    % Modified iterative displacement correction streamlines
%     n_iter = 10;
%     V_MIDC(:,:,:,:,t) = miDC(V, Td(t), n_iter);
%     streamlines = zeros([size(seeds) N]);
%     streamlines(:,:,1) = seeds;
%     for s = 2:N
%         streamlines(:,:,s) = step_paths(V_MIDC(:,:,:,:,t), Td(t), streamlines(:,:,s-1));
%     end
%     streamlines = checkoob(streamlines,mask);
%     plot_streams(streamlines, CD, ['miDC - Td=' num2str(Td(t)) ' ms'])
%     streamlinesMIDC(:,:,:,t) = streamlines;
    
    % Modified iterative displacement correction streamlines
    n_iter = 10;
    upscaleFactor = 10;
    V_PS(:,:,:,:,t) = miDC(V, Td(t), n_iter);
    streamlines = zeros([size(seeds) N]);
    streamlines(:,:,1) = seeds;
    streamlines = repmat(streamlines,[upscaleFactor 1 1]); %upscale for MC sampling
    for s = 2:N
        streamlines = step_paths_rand(V_PS(:,:,:,:,t),Td(t),streamlines,s,P);
    end
    streamlines = checkoob(streamlines,mask);
    plot_streams(streamlines, CD, ['miDC+ps - Td=' num2str(Td(t)) ' ms'])
    streamlinesPS(:,:,:,t) = streamlines;
end 

plane = 140; %plane at circle of willis
for t=1:length(Td)
    pctPass(t,1) = checkCOWentry(streamlinesSSDC(:,:,:,t),plane);    
    RMSE(t,1) = vrmse(V_SSDC(:,:,:,:,t), V, mask);
    meanLength(t,1) = line_lengths(streamlinesSSDC(:,:,:,t));

    pctPass(t,2) = checkCOWentry(streamlinesIDC(:,:,:,t),plane);  
    RMSE(t,2) = vrmse(V_IDC(:,:,:,:,t), V, mask);
    meanLength(t,2) = line_lengths(streamlinesIDC(:,:,:,t));

    pctPass(t,3) = checkCOWentry(streamlinesMIDC(:,:,:,t),plane);  
    RMSE(t,3) = vrmse(V_MIDC(:,:,:,:,t), V, mask);
    meanLength(t,3) = line_lengths(streamlinesMIDC(:,:,:,t));
end 

clear x y z s N n_iter xSectionTop xSectionTopBin seq_param

%figure; quiver(V(:,:,20,2), V(:,:,20,1)); title('Ground Truth');
%figure; quiver(Vdn(:,:,20,2,1,1), Vdn(:,:,20,1,1,1)); title('Displaced');
%figure; quiver(V_SSDC(:,:,20,2,1,1), V_SSDC(:,:,20,1,1,1)); title('SSDC');
%figure; quiver(V_MIDC(:,:,20,2,1,1), V_MIDC(:,:,20,1,1,1)); title('MIDC');