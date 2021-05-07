function makeQuiverPlot(Vi,mask,patchLoc,Td)
% Make a zoomed-in figure of velocity glyphys (quiver arrows) around
% curvature for simulation study. Show the displaced velocity field leads 
% streamlines to wall. One streamline is generated within vessel to show 
% streamline going into vessel wall. 

% Zoom into first portion of curvature of phantom
patchX = Vi(patchLoc(1,1):patchLoc(1,2),patchLoc(2,1):patchLoc(2,2),:,1); %grab patch from x-velocity field
patchY = Vi(patchLoc(1,1):patchLoc(1,2),patchLoc(2,1):patchLoc(2,2),:,2); %grab patch from y-velocity field
patchZ = zeros(size(patchX)); %grab patch from z-velocity field
patchV(:,:,:,1) = patchX;
patchV(:,:,:,2) = patchY;
patchV(:,:,:,3) = patchZ;
patchVmag = sqrt( patchX.^2 + patchY.^2 + patchZ.^2); %speed
patchMask = mask(patchLoc(1,1):patchLoc(1,2),patchLoc(2,1):patchLoc(2,2),:);

patchX = imresize(patchX,[256 256],'nearest'); %upsample for larger images
patchY = imresize(patchY,[256 256],'nearest');
patchV = imresize(patchV,[256 256],'nearest');
patchVmag = imresize(patchVmag,[256 256],'nearest');
patchMask = imresize(patchMask,[256 256],'nearest');

% streamlinesT(:,:,1) = [20 10 10; 20 20 10; 20 30 10; 20 40 10; 20 50 10; ...
%     20 60 10; 20 70 10; 20 80 10; 20 90 10];
streamlinesT(:,:,1) = [5 40 10;5 80 10;5 120 10]; %create single streamline in vessel
for s = 2:450
    streamlinesT(:,:,s) = step_paths(patchV, Td, streamlinesT(:,:,s-1));
end
streamlinesT = checkoob(streamlinesT,patchMask); %cut off streamline when out of bounds
        
for i=1:size(patchX,1)-1
    if mod(i,25)
        patchX(i+1,:,10) = 0; %kill velocity vectors every 15 points...
        patchX(:,i+1,10) = 0; %for clear visualization of vector arrows
        patchY(i+1,:,10) = 0; 
        patchY(:,i+1,10) = 0;
    end 
end

figure; imshow(patchVmag(:,:,10).*patchMask(:,:,10),[0 0.8]); hold on; %show zoomed in speed and hold figure
for i = 1:size(streamlinesT,1)
    line(squeeze(streamlinesT(i,2,:)), squeeze(streamlinesT(i,1,:)), ...
        'Color', [0 0.3 0.9], 'LineWidth', 2, 'LineStyle', '-');
end
quiver(patchY(:,:,10).*patchMask(:,:,10),patchX(:,:,10).*patchMask(:,:,10),20,'Color',[0.85 0 0],'LineWidth',1.8);
plot(40, 5, 'b.', 'MarkerSize', 20);
plot(80, 5, 'b.', 'MarkerSize', 20);
plot(120, 5, 'b.', 'MarkerSize', 20);