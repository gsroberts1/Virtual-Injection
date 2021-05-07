function streamlines = checkoob(streamlines,mask)
%CHECKOOB Check if streamlines have exited mask
% Check on a line-by-line basis if x,y,z positions are outside of the
% bounds of our defined mask. Make NaN if out of bounds (oob)

for p=1:size(streamlines,1) %for each line...
    Line = squeeze(streamlines(p,:,:)); %grab specific line
    for s=1:size(streamlines,3) %for all steps...
        step = Line(:,s); %look at each step
        if (sum(int16(step)<1)>0) || ... %off of the grid?
           (sum((int16(size(mask) - step'))<=0)) || ... %off the grid?
           (mask(int16(step(1)),int16(step(2)),int16(step(3)))==0) %within mask?         
            Line(:,s:end) = NaN; %if so, make rest of steps NaN
            break %exit step loop
        end
    end 
    streamlines(p,:,:) = Line; %update streamline matrix with Line
end 

end

