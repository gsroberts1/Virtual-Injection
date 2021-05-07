function lengths = line_lengths( paths )
% LINE_LENGTHS Calculates mean length of all streamlines

numLines = size(paths,1); %get total number of lines
lengths = zeros(size(paths,1), 1); %intialize length matrix
for i=1:numLines %for each line...
    line = squeeze(paths(i,:,:)); %grab line i
    dr = diff(line,1,2); %calculate all step lengths in x,y,z
    DR = sqrt(sum(dr.^2,1)); %turn step lengths to distances
    lengths(i) = nansum(DR); %sum all (non-NaN) lengths
end