base_dir = uigetdir();
cd(base_dir)

movefile *sqrt* raw
movefile *png raw

sqrt = fullfile(base_dir,'sqrt');
raw = fullfile(base_dir,'raw');

%% Organize sqrt files
cd ('../sqrt')
movefile *d0* axial %0 = axial
movefile *d1* sagittal %0 = sagittal
movefile *d2* coronal %0 = coronal

% axial-dimension
cd('axial')
dir = dir;
numFiles = length(dir)-2; % -2 = Don't count '.' and '..' directories
sqrt_images_ax = zeros(480,640,numFiles); % Python always outputs 480x640
for i=1:numFiles
    thisFile = fullfile(dir(i).folder, dir(i).name);
    hold = importdata(thisFile);
    sqrt_images_ax(:,:,i) = hold;
end

% sagittal-dimension
cd('sagittal')
dir = dir;
numFiles = length(dir)-2; % -2 = Don't count '.' and '..' directories
sqrt_images_sag = zeros(480,640,numFiles); % Python always outputs 480x640
for i=1:numFiles
    thisFile = fullfile(dir(i).folder, dir(i).name);
    hold = importdata(thisFile);
    sqrt_images_sag(:,:,i) = hold;
end

% coronal-dimension
cd('coronal')
dir = dir;
numFiles = length(dir)-2; % -2 = Don't count '.' and '..' directories
sqrt_images_cor = zeros(480,640,numFiles); % Python always outputs 480x640
for i=1:numFiles
    thisFile = fullfile(dir(i).folder, dir(i).name);
    hold = importdata(thisFile);
    sqrt_images_cor(:,:,i) = hold;
end

%% Organize raw files
cd('raw')
movefile *d0* axial %0 = axial
movefile *d1* sagittal %0 = sagittal
movefile *d2* coronal %0 = coronal

% axial-dimension
cd('axial')
dir = dir;
numFiles = length(dir)-2; % -2 = Don't count '.' and '..' directories
raw_images_ax = zeros(480,640,numFiles); % Python always outputs 480x640
for i=1:numFiles
    thisFile = fullfile(dir(i).folder, dir(i).name);
    hold = importdata(thisFile);
    raw_images_ax(:,:,i) = hold;
end

% sagittal-dimension
cd('sagittal')
dir = dir;
numFiles = length(dir)-2; % -2 = Don't count '.' and '..' directories
raw_images_sag = zeros(480,640,numFiles); % Python always outputs 480x640
for i=1:numFiles
    thisFile = fullfile(dir(i).folder, dir(i).name);
    hold = importdata(thisFile);
    raw_images_sag(:,:,i) = hold;
end

% coronal-dimension
cd('coronal')
dir = dir;
numFiles = length(dir)-2; % -2 = Don't count '.' and '..' directories
raw_images_cor = zeros(480,640,numFiles); % Python always outputs 480x640
for i=1:numFiles
    thisFile = fullfile(dir(i).folder, dir(i).name);
    hold = importdata(thisFile);
    raw_images_cor(:,:,i) = hold;
end

