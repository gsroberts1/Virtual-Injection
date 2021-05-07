function angio = calc_angio(MAG,vMean,Venc)
%CALC_ANGIO: Calculates angiogram from pcvipr header and velocity data

Vmag = sqrt(sum(vMean.^2,4)); %get speed image
idx = find(Vmag > Venc); %find where flow velocity > VENC.
Vmag(idx) = Venc; %cap Vmag at VENC

% Create complex-difference angiogram
% Bernstein MA, Ikezaki Y. JMRI, 1991;1(6):725-729.
angio = 2*MAG.*sin( (pi/2*Vmag) / Venc); 
return

