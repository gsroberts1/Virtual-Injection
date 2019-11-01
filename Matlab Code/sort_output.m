function [dataFolder] = sort_output(srcDir)
    %% Sorts python output from 'new_test.py' virtual injection code
    
    % Source directory needs to 'inject_data' folder
    if nargin<1 || (~ischar(srcDir) && ~isstring(srcDir)) || ~exist(srcDir, 'dir')
        srcDir = uigetdir();    
        fprintf('Setting source directory to %s\n', srcDir);
    end
    srcDir = char(srcDir);
    cd(srcDir); % Move to inject_data folder
    
    % Create data folder and move .npy files to it
    mkdir('data')
    movefile *.npy data
    
    % Create sqrt folder and move sqrt png files to it
    mkdir('sqrt')
    movefile *sqrt* sqrt
    % Create raw folder and move the rest of the pngs to that folder
    mkdir('raw')
    movefile *.png raw
    
    % Organize sqrt images into axial (d0), sagittal (d1), coronal (d2)
    cd('sqrt')
    mkdir('axial'); mkdir('sagittal'); mkdir('coronal')
    movefile *d0* axial
    movefile *d1* sagittal
    movefile *d2* coronal
    cd('../raw')
    mkdir('axial'); mkdir('sagittal'); mkdir('coronal')
    movefile *d0* axial
    movefile *d1* sagittal
    movefile *d2* coronal
    
    %% Convert npy to dat
    
    % Save dataFolder for input into npytonii function
    cd('../data')
    dataFolder = pwd;
    % Move pcvipr_header into data folder (for npytonii function)
    copyfile ../../dat/pcvipr_header.txt .
    
    % List all .npy files, convert to Matlab, save them as .dat files
    DIR = dir('*.npy');
    for i=1:length(DIR)
        pyFile = DIR(i).name;
        hold = readNPY(pyFile);
          offset = 2.5; % time increment in ms
          iter = str2double(pyFile(end-7:end-4))+1; % iteration number
          time = offset*iter; % absolute time after virtual injection (ms)
        tempName = ['injectData_' num2str(time) '.dat'];
        save(tempName,'hold');
    end 
end

