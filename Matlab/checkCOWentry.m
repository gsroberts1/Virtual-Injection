function [numPassLICA,numPassLMCA,numPassLACA,numPassRICA,numPassRMCA,numPassRACA] ...
    = checkCOWentry(streamlines,split,planeICA,planeLMCA,planeRMCA,planeLACA,planeRACA)
% CHECKCOWENTRY Evaluate number of streamlines entering Circle of Willis
% Entry of COW defined by plane (z-height on image)

%numLines = size(streamlines,1); %get total number of possible lines
zLines = squeeze(streamlines(:,3,:)); %get z positions of lines
yLines = squeeze(streamlines(:,1,:));

% Split to left and right ICA
% Left
left = find(yLines(:,1)>split);
zLinesLeft = zLines(left,:);
passedLICA = find(sum(zLinesLeft<planeICA,2)); %see if any have passed our z plane
numPassLICA = length(passedLICA); %calculate number that have entered COW

temp = streamlines(left,:,:);
newLinesL = temp(passedLICA,:,:); %keep only lines making it passed plane1
yLines2 = squeeze(newLinesL(:,1,:));
zLines2 = squeeze(newLinesL(:,3,:));
passedLMCA = find(sum((yLines2>planeLMCA).*(zLines2<planeICA),2));
numPassLMCA = length(passedLMCA);
passedLACA = find(sum((yLines2<planeLACA).*(zLines2<planeICA),2));
numPassLACA = length(passedLACA);

% Right
right = find(yLines(:,1)<split);
zLinesRight = zLines(right,:);
passedRICA = find(sum(zLinesRight<planeICA,2)); %see if any have passed our z plane
numPassRICA = length(passedRICA); %calculate number that have entered COW

temp = streamlines(right,:,:);
newLinesR = temp(passedRICA,:,:); %keep only lines making it passed plane1
yLines3 = squeeze(newLinesR(:,1,:));
zLines3 = squeeze(newLinesR(:,3,:));
passedRMCA = find(sum((yLines3<planeRMCA).*(zLines3<planeICA),2));
numPassRMCA = length(passedRMCA);
passedRACA = find(sum((yLines3>planeRACA).*(zLines3<planeICA),2));
numPassRACA = length(passedRACA);

end

