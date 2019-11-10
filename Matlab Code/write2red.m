dirInfo = dir('*.png');
for i=1:numel(dirInfo)
    temp(:,:,:,i) = imread(dirInfo(i).name);
    temp(:,:,2,i) = 0;
    temp(:,:,3,i) = 0;
end 
mkdir red
cd red
for i=1:numel(dirInfo)
    name = dirInfo(i).name;
    name = name(1:(end-4));
    imwrite(temp(:,:,:,i),[name '_red.png']);
end 