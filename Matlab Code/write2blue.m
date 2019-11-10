dirInfo = dir('*.png');
for i=1:numel(dirInfo)
    temp(:,:,:,i) = imread(dirInfo(i).name);
    temp(:,:,1,i) = 0;
    temp(:,:,2,i) = 0;
end 
mkdir blue
cd blue
for i=1:numel(dirInfo)
    name = dirInfo(i).name;
    name = name(1:(end-4));
    imwrite(temp(:,:,:,i),[name '_blue.png']);
end 