function plot_streams(paths, mag, Title)

%%% Show Sagittal Image
% im = squeeze(max(abs(mag), [], 3));
% figure; imshow(im,[]); title(Title)
% 
% for i = 1:size(paths,1)
%     line(squeeze(paths(i,2,:)), squeeze(paths(i,1,:)), 'Color', rand(3,1));
% end

%%% Show Axial Image
% im = squeeze(max(abs(mag), [], 2));
% figure; imshow(im,[]); title(Title)
% 
% for i = 1:size(paths,1)
%     line(squeeze(paths(i,3,:)), squeeze(paths(i,1,:)), 'Color', rand(3,1));
% end

%%% Show Coronal Image
im = squeeze(max(abs(mag), [], 1));
figure; imshow(im,[]); title(Title)

for i = 1:size(paths,1)
    line(squeeze(paths(i,3,:)), squeeze(paths(i,2,:)), 'Color', rand(3,1));
end

end

