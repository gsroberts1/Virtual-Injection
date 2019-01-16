function dcm2nii(srcDir,outFileName)

    curDir = pwd; 
    if nargin<1 || (~ischar(srcDir) && ~isstring(srcDir)) || ~exist(srcDir, 'dir')
        srcDir = curDir;
        fprintf("Setting source directory to %s\n", srcDir);
    end
    srcDir = string(srcDir);

    if nargin>=2 && (ischar(outFileName) || isstring(outFileName)) 
        outFile = fullfile(srcDir, string(outFileName));
    else
        outFile = fullfile(srcDir, "out.nii.gz");
        fprintf("Setting output file to %s\n", outFile);
    end
   
    dirContents = dir(fullfile(srcDir,"*.dcm"));
    counter = 1;
    for contentsIndex = 1:length(dirContents)
        dicomFilePath = fullfile(dirContents(contentsIndex).folder, dirContents(contentsIndex).name);
        info = dicominfo(dicomFilePath);
        if counter==1
            xSize = double(info.Height);
            ySize = double(info.Width);
            p = double(info.ImagePositionPatient);
            R = double(info.ImageOrientationPatient);
            spacing = double([info.PixelSpacing',info.SpacingBetweenSlices]);
            nT = double(info.CardiacNumberOfImages);
            dT = double(60000/info.HeartRate/nT);
        end
        img(:,:,floor((counter-1)/nT)+1,mod(counter-1,nT)+1) = single(dicomread(dicomFilePath))'; %#ok<AGROW>
        counter = counter+1;
    end
    img = int16(img.*(2^15)./max(img(:)));
    zSize = (counter-1)/nT;
    
    lastPos = double(info.ImagePositionPatient);
    if ~all(lastPos-p==[0;0;0])
        R(7:9) = (lastPos-p)./(zSize-1)./spacing(3);
    else
        R(7:9) = cross(R(1:3),R(4:6));
    end
    R = reshape(R, [3,3]);
    
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
    R = R'*diag([-1,-1,1]);
    p = p'.*[-1,-1,1];

    info.Transform = affine3d([[diag(spacing)*R;p],[0;0;0;1]]);
    info.AuxiliaryFile = 'none';
    
    if nT==1
        info.ImageSize = [xSize, ySize, zSize];
        info.PixelDimensions = spacing';
        info.TimeUnits = 'None';
        niftiwrite(img, outFile, info);
    elseif nT>1
        info.ImageSize = [xSize, ySize, zSize, nT];
        info.PixelDimensions = [spacing, dT];
        info.TimeUnits = 'Millisecond';
        niftiwrite(img, outFile, info);
        info.raw.dim(5) = 1;
        
        if zSize>1
            info.ImageSize = info.ImageSize(1:3);
            info.PixelDimensions = info.PixelDimensions(1:3);
            info.raw.dim(1) = 3;
        else
            info.ImageSize = info.ImageSize(1:2);
            info.PixelDimensions = info.PixelDimensions(1:2);
            info.raw.dim(1) = 2;
        end
        info.TimeUnits = 'None';
        niftiwrite(int16(mean(img,4)), strrep(outFile,".nii","_avg.nii"), info);
    end
    
end