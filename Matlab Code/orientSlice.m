data = load_dat('CD.dat',[320 320 320]);
data = imrotate3(data,-90,[1 0 0]);
slice = squeeze(data(:,:,200));
slice = flip(slice,1);
figure; imshow(slice,[]);