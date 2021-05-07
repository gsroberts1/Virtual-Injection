function [pctPass1,pctPass2,pctPass3,pctPass4] ...
    = checkPlaneCrossings(streamlines,plane1,plane2,plane3,plane4)
% CHECKPLANECROSSINGS Check if streamlines have passed plane#
% Looking here to see how many streamlines have passed a defined plane
% (x,y) on the image. 

numLines = size(streamlines,1); %get total number of possible lines

% Check how many planes have made it to plane immediately before curve
xLines = squeeze(streamlines(:,1,:)); %get x-values of all lines
passed = find(sum(xLines>plane1,2)); %see which lines have passed plane1
pctPass1 = length(passed)./numLines; %get percent of passing lines
newLines = streamlines(passed,:,:); %keep only lines making it passed plane1

% Check if lines now pass 90 degree of curvature
yLines = squeeze(newLines(:,2,:)); %get y-values of lines
passed = find(sum(yLines>plane2,2)); %see if lines have passed y-value=plane2
pctPass2 = length(passed)./numLines; 
newLines = newLines(passed,:,:); %keep only lines making it passed plane2

% Check if lines have made it around U-bend (180 degrees)
xLines2 = squeeze(newLines(:,1,:));
yLines2 = squeeze(newLines(:,2,:));
passed = find(sum((xLines2<plane3).*(yLines2>plane2),2));
pctPass3 = length(passed)./numLines;
newLines = newLines(passed,:,:);

% Check if planes have made it to phantom outlet distal to stenosis
xLines3 = squeeze(newLines(:,1,:));
passed = find(sum(xLines3<plane4,2));
pctPass4 = length(passed)./numLines;

end

