series = '9637.';
set = {'500.'; '501.'; '502.'; '503.'; '504.'};
start = 83;
End = 216;

set1 = zeros(256,256,256);
set2 = zeros(256,256,256);
set3 = zeros(256,256,256);
set4 = zeros(256,256,256);
set5 = zeros(256,256,256);
% set6 = zeros(320,320,320);
% set7 = zeros(320,320,320);

%SET1
for i = start:End
    if i < 10
        file = [series set{1} '00' num2str(i) '.dcm.sdcopen'];
        set1(:,:,i) = dicomread(file);
    elseif i < 100
        file = [series set{1} '0' num2str(i) '.dcm.sdcopen'];
        set1(:,:,i) = dicomread(file);
    else
        file = [series set{1} num2str(i) '.dcm.sdcopen'];
        set1(:,:,i) = dicomread(file);
    end 
end 

%SET2
for i = start:End
    if i < 10
        file = [series set{2} '00' num2str(i) '.dcm.sdcopen'];
        set2(:,:,i) = dicomread(file);
    elseif i < 100
        file = [series set{2} '0' num2str(i) '.dcm.sdcopen'];
        set2(:,:,i) = dicomread(file);
    else
        file = [series set{2} num2str(i) '.dcm.sdcopen'];
        set2(:,:,i) = dicomread(file);
    end 
end 

%SET3
for i = start:End
    if i < 10
        file = [series set{3} '00' num2str(i) '.dcm.sdcopen'];
        set3(:,:,i) = dicomread(file);
    elseif i < 100
        file = [series set{3} '0' num2str(i) '.dcm.sdcopen'];
        set3(:,:,i) = dicomread(file);
    else
        file = [series set{3} num2str(i) '.dcm.sdcopen'];
        set3(:,:,i) = dicomread(file);
    end 
end 

%SET4
for i = start:End
    if i < 10
        file = [series set{4} '00' num2str(i) '.dcm.sdcopen'];
        set4(:,:,i) = dicomread(file);
    elseif i < 100
        file = [series set{4} '0' num2str(i) '.dcm.sdcopen'];
        set4(:,:,i) = dicomread(file);
    else
        file = [series set{4} num2str(i) '.dcm.sdcopen'];
        set4(:,:,i) = dicomread(file);
    end 
end 

%SET5
for i = start:End
    if i < 10
        file = [series set{5} '00' num2str(i) '.dcm.sdcopen'];
        set5(:,:,i) = dicomread(file);
    elseif i < 100
        file = [series set{5} '0' num2str(i) '.dcm.sdcopen'];
        set5(:,:,i) = dicomread(file);
    else
        file = [series set{5} num2str(i) '.dcm.sdcopen'];
        set5(:,:,i) = dicomread(file);
    end 
end 

% %SET6
% for i = 83:216
%     if i < 10
%         file = ['5894.505.00' num2str(i) '.dcm.sdcopen'];
%         set1(:,:,i) = dicomread(file);
%     elseif i < 100
%         file = ['5894.505.0' num2str(i) '.dcm.sdcopen'];
%         set1(:,:,i) = dicomread(file);
%     else
%         file = ['5894.505.' num2str(i) '.dcm.sdcopen'];
%         set1(:,:,i) = dicomread(file);
%     end 
% end 
% 
% %SET7
% for i = 83:216
%     if i < 10
%         file = ['5894.506.00' num2str(i) '.dcm.sdcopen'];
%         set1(:,:,i) = dicomread(file);
%     elseif i < 100
%         file = ['5894.506.0' num2str(i) '.dcm.sdcopen'];
%         set1(:,:,i) = dicomread(file);
%     else
%         file = ['5894.506.' num2str(i) '.dcm.sdcopen'];
%         set1(:,:,i) = dicomread(file);
%     end 
% end 

mip1 = max(set1,[],3);
mip2 = max(set2,[],3);
mip3 = max(set3,[],3);
mip4 = max(set4,[],3);
mip5 = max(set5,[],3);
% mip6 = max(set6,[],3);
% mip7 = max(set7,[],3);

new = [mip1 mip2 mip3 mip4 mip5];
new = reshape(new,256,256,5);
imshow3D(new);