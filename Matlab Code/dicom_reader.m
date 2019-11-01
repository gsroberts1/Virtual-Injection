series = '3951.';
set = {'501.'; '502.'; '503.'; '504.'; '505.'; '506.'; '507.'};
pcasl = zeros(320,320,320,numFrames);

%SET5
for i = 1:320
    for j=1:numFrames
        if i < 10
            file = [series set{j} '00' num2str(i) '.dcm.sdcopen'];
            set(:,:,i,j) = dicomread(file);
        elseif i < 100
            file = [series set{j} '0' num2str(i) '.dcm.sdcopen'];
            set(:,:,i,j) = dicomread(file);
        else
            file = [series set{j} num2str(i) '.dcm.sdcopen'];
            set(:,:,i,j) = dicomread(file);
        end 
    end 
end 




mip1 = max(pcasl,[],3);
mip2 = max(set2,[],3);
mip3 = max(set3,[],3);
mip4 = max(set4,[],3);
mip5 = max(set5,[],3);
mip6 = max(set5,[],3);
mip7 = max(set5,[],3);

new = [mip1 mip2 mip3 mip4 mip5];
new = reshape(new,256,256,5);
imshow3D(new);