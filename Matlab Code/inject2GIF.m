npies = dir('TOA*.npy');
for t=1:length(npies)
    numC = sprintf( '%04d', (t*20)-1 ) ;
    title = ['TOAf1_t' numC '.npy'];
    TOA(:,:,:,t) = int16(readNPY(title));
end 

sagittal = squeeze(double(max(TOA,[],3)));
coronal = squeeze(double(max(TOA,[],2)));
axial = squeeze(double(max(TOA,[],1)));

% sagittal = imresize(sagittal,[1024 1024],'bicubic');
% coronal = imresize(coronal,[1024 1024],'bicubic');
% axial = imresize(axial,[1024 1024],'bicubic');

fig = figure;
for t=1:length(npies)
    imshow(sagittal(:,:,t),[0 max(sagittal,[],'all')*0.01]);drawnow;
    frame = getframe(fig);
    sag{t} = frame2im(frame);
end 

filename = 'sagittal_inject.gif'; % Specify the output file name
for t = 1:length(npies)
    [A,map] = rgb2ind(sag{t},256);
    if t == 1
        imwrite(A,map,filename,'gif','LoopCount',Inf,'DelayTime',0.2);
    else
        imwrite(A,map,filename,'gif','WriteMode','append','DelayTime',0.2);
    end
end

fig = figure;
for t=1:length(npies)
    imshow(coronal(:,:,t),[0 max(coronal,[],'all')*0.25]);
    drawnow
    frame = getframe(fig);
    cor{t} = frame2im(frame);
end 

filename = 'coronal_inject.gif'; % Specify the output file name
for t = 1:length(npies)
    [A,map] = rgb2ind(cor{t},256);
    if t == 1
        imwrite(A,map,filename,'gif','LoopCount',Inf,'DelayTime',0.2);
    else
        imwrite(A,map,filename,'gif','WriteMode','append','DelayTime',0.2);
    end
end

fig = figure;
for t=1:length(npies)
    imshow(axial(:,:,t),[0 max(axial,[],'all')*0.25]);
    drawnow
    frame = getframe(fig);
    ax{t} = frame2im(frame);
end 

filename = 'axial_inject.gif'; % Specify the output file name
for t = 1:length(npies)
    [A,map] = rgb2ind(ax{t},256);
    if t == 1
        imwrite(A,map,filename,'gif','LoopCount',Inf,'DelayTime',0.2);
    else
        imwrite(A,map,filename,'gif','WriteMode','append','DelayTime',0.2);
    end
end