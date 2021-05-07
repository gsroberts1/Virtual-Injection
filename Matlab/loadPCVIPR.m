function [VMEAN,MAG,CD] = loadPCVIPR(directory)
% LOADPCVIPR Loads in time-averaged PCVIPR data

fid = fopen([directory '\pcvipr_header.txt'], 'r'); %open header
dataArray = textscan(fid, '%s%s%[^\n\r]', 'Delimiter', ' ', 'MultipleDelimsAsOne', true, 'ReturnOnError', false);
fclose(fid); 

% Turn header into readable structure
dataArray{1,2} = cellfun(@str2num,dataArray{1,2}(:), 'UniformOutput', false);
pcviprHeader = cell2struct(dataArray{1,2}(:), dataArray{1,1}(:), 1);
res = pcviprHeader.matrixx; %get matrix resolution (pixels)                  

% Read time-averaged magnitude, complex difference, and mean velocities
MAG = load_dat(fullfile(directory,'MAG.dat'),[res res res]);
CD = load_dat(fullfile(directory,'CD.dat'),[res res res]); 
VMEAN = zeros(res,res,res,3); %initialize matrix for x,y,z mean velocities
for n = 1:3
    VMEAN(:,:,:,n) = load_dat(fullfile(directory,['comp_vd_' num2str(n) '.dat']),[res res res]);
end

end 

function v = load_dat(name, res)
% LOAD_DAT Loads in dat files in current directory

[fid,errmsg]= fopen(name,'r');
if fid < 0  % If name does not exist in directory
    disp(['Error Opening Data : ',errmsg]);
end

% Reads in as short, reshapes by image res.
v = reshape(fread(fid,'short=>single'),res);
fclose(fid);
end 