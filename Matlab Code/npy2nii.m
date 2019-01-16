function npy2nii(srcDir)

    curDir = pwd; 
    if nargin<1 || (~ischar(srcDir) && ~isstring(srcDir)) || ~exist(srcDir, 'dir')
        srcDir = curDir;    
        fprintf('Setting source directory to %s\n', srcDir);
    end
    srcDir = char(srcDir);
    
    pcVIPRHeaderFilePath = fullfile(srcDir,'pcvipr_header.txt');
    if exist(pcVIPRHeaderFilePath, 'file')==2
        fid = fopen(pcVIPRHeaderFilePath);
        if fid<0
            error('Could not open pcvipr_header.txt file.');
        else
            C = textscan(fid,'%s %s');
            field = C{1};
            value = C{2};
            fclose(fid);
            
            fov = lookup(field,value,'fovx',3);
            xSize = lookup(field,value,'matrixx',1);
            ySize = lookup(field,value,'matrixy',1);
            zSize = lookup(field,value,'matrixz',1);
            steps = 1200;                           %%%%%%% CHANGE
            offset = 0.0025;                        %%%%%%% CHANGE
            dT = 30*2.5;                            %%%%%%% CHANGE
            time = steps*offset;                    %%%%%%% CHANGE
 
            
            spacing = (fov./[xSize;ySize;zSize]);
            p = lookup(field,value,'sx',3)';
            R = reshape(lookup(field,value,'ix',9),[3,3])';          
           
            %% Change .npy to .dat %%
            
            DIR = dir([srcDir '/*.npy']);
            nT = size(DIR,1)-2;
            TOA = zeros(xSize,ySize,zSize,nT,'int16');           

            for i=1:nT
                if (i*30)-1 < 100
                    name = ['TOAf1_t00' num2str((i*30)-1) '.npy'];
                    TOA(:,:,:,i) = readNPY(name);
                elseif  (i*30)-1 < 1000
                    name = ['TOAf1_t0' num2str((i*30)-1) '.npy'];
                    TOA(:,:,:,i) = readNPY(name);
                else 
                    name = ['TOAf1_t' num2str((i*30)-1) '.npy'];
                    TOA(:,:,:,i) = readNPY(name);
                end 
            end 
        end
    else
        error('Could not find pcvipr_header.txt file.');
    end
    
    info.Filename = '';
    info.Filemoddate = '';
    info.Filesize = 0;
    info.Description = '';
    info.Datatype = 'int16';
    info.BitsPerPixel = 16;   
    info.SpaceUnits = 'Millimeter';
    info.AdditiveOffset = 0;
    info.MultiplicativeScaling = 0;
    info.TimeOffset = 0;
    info.SliceCode = 'Unknown';
    info.FrequencyDimension = 0;
    info.PhaseDimension = 0;
    info.SpatialDimension = 0;
    info.DisplayIntensityRange = [0 0];
    info.TransformName = 'Sform';
    info.Qfactor = 1;
    R = R.*repmat([-1,-1,1],3,1);
    p = p.*[-1,-1,1];
%     if det(R)>0
        info.Qfactor = 1;
%     else
%         info.Qfactor = -1;
%         R(:,3) = -R(:,3);
%     end
    info.Transform = affine3d([[R;p],[0;0;0;1]]);
    info.AuxiliaryFile = 'none';
    info.ImageSize = [xSize, ySize, zSize, nT];
    info.PixelDimensions = [spacing', dT];
    info.TimeUnits = 'Millisecond';
    niftiwrite(TOA, fullfile(srcDir,"VirtInject.nii"), info);
end

function value = lookup(fields,values,field, length)
    index = find(cellfun(@(s) strcmp(field, s), fields));
    value = cellfun(@str2num,values(index:(index+length-1)));
end

