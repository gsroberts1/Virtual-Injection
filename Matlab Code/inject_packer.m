function [images] = inject_packer()
% Organizes files and produces a .dat file to use for cine viewing
%   Raw and sqrt images are organized into folders. Axial, sagittal, and
%   coronal images are organized in subfolders within these folders. Images
%   in each subfolder are combined into a 3D dat file (output) to be used for
%   cine-viewing of virtual injection data.
base_dir = uigetdir();
cd(base_dir)

movefile *sqrt* sqrt
movefile *png raw

sqrt = fullfile(base_dir,'sqrt');
raw = fullfile(base_dir,'raw');

%% Organize sqrt files
cd('sqrt')
movefile *d0* axial %0 = axial
movefile *d1* sagittal %0 = sagittal
movefile *d2* coronal %0 = coronal

% axial-dimension
cd('axial')
DIR = dir;
numFiles = length(DIR)-2; % -2 = Don't count '.' and '..' directories
sqrt_ax = zeros(480,640,3,numFiles,'uint8'); % Python always outputs 480x640
for i=3:(numFiles+2)
    thisFile = fullfile(DIR(i).folder, DIR(i).name);
    hold = imread(thisFile);
    sqrt_ax(:,:,:,i) = hold;
end

% sagittal-dimension
cd('../sagittal')
DIR = dir;
numFiles = length(DIR)-2;
sqrt_sag = zeros(480,640,3,numFiles,'uint8');
for i=3:(numFiles+2)
    thisFile = fullfile(DIR(i).folder, DIR(i).name);
    hold = imread(thisFile);
    sqrt_sag(:,:,:,i) = hold;
end

% coronal-dimension
cd('../coronal')
DIR = dir;
numFiles = length(DIR)-2; 
sqrt_cor = zeros(480,640,3,numFiles,'uint8');
for i=3:(numFiles+2)
    thisFile = fullfile(DIR(i).folder, DIR(i).name);
    hold = imread(thisFile);
    sqrt_cor(:,:,:,i) = hold;
end

%% Organize raw files
cd('../../raw')
movefile *d0* axial %0 = axial
movefile *d1* sagittal %0 = sagittal
movefile *d2* coronal %0 = coronal

% axial-dimension
cd('axial')
DIR = dir;
numFiles = length(DIR)-2; 
raw_ax = zeros(480,640,3,numFiles,'uint8');
for i=3:(numFiles+2)
    thisFile = fullfile(DIR(i).folder, DIR(i).name);
    hold = imread(thisFile);
    raw_ax(:,:,:,i) = hold;
end

% sagittal-dimension
cd('../sagittal')
DIR = dir;
numFiles = length(DIR)-2;
raw_sag = zeros(480,640,3,numFiles,'uint8');
for i=3:(numFiles+2)
    thisFile = fullfile(DIR(i).folder, DIR(i).name);
    hold = imread(thisFile);
    raw_sag(:,:,:,i) = hold;
end

% coronal-dimension
cd('../coronal')
DIR = dir;
numFiles = length(DIR)-2;
raw_cor = zeros(480,640,3,numFiles,'uint8');
for i=3:(numFiles+2)
    thisFile = fullfile(DIR(i).folder, DIR(i).name);
    hold = imread(thisFile);
    raw_cor(:,:,:,i) = hold;
end
images.sqrt_ax = sqrt_ax;
images.sqrt_sag = sqrt_sag;
images.sqrt_cor = sqrt_cor;
images.raw_ax = raw_ax;
images.raw_sag = raw_sag;
images.raw_cor = raw_cor;

end

