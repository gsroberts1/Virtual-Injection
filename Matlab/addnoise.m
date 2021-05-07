function [MAGn,Vn,SNRtrue] = addnoise(V, MAG, SNR, Venc)
%ADDNOISE Add Gaussian noise to image 
% Note that MAG=mask of simulation

vencang = pi/Venc; %conversion factor (velocity to angle)
im = repmat(MAG, [1 1 1 3]).*exp(1i.*vencang*V); %replicate mask x3 for each vel direction
scale = sqrt(numel(MAG))/SNR; %Gaussian scaling factor for FFT

% Add complex gaussian noise in k-space for each velocity encode
for vd = 1:3
    k = ifftshift(fftn(fftshift(im(:,:,:,vd)))); %k-space
    k = k + scale .* (randn(size(MAG)) + 1j.*randn(size(MAG)));
    temp = ifftshift(ifftn(fftshift(k))); %image space
    SNRtrue(vd) = mean(abs(temp(MAG>0)))./std(abs(temp(MAG>0))); %verify SNR from image (signal/noise)
    imn(:,:,:,vd) = temp;
end

Vn = angle(imn)./vencang; %convert phase to velocity
MAGn = mean(abs(imn),4); %get mean of magnitudes from all 3 images
SNRtrue = mean(SNRtrue); %take mean SNR from all 3 images