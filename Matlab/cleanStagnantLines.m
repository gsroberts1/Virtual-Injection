function streamlines = cleanStagnantLines(streamlines)

dX = diff(squeeze(streamlines(:,1,:)),1,2);
for i=1:size(dX,1)
    line = dX(i,:);
    if ~sum(isnan(line))
        idx = find(~line,1,'first');
        streamlines(i,:,idx+1:end) = NaN;
    end 
end 

end

