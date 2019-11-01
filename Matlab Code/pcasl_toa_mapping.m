%blood 1.5T
T2 =  250;
T1 =  1664;

%%%Imaging Acquisition
FLIP = 10;
tr = 5;
tag_duration = floor(2000/tr); %2s of tagging
sample_window = 266; %floor(1000/tr);
inversion_efficiency = 1.0;

flips = FLIP*ones(sample_window,1);

signal_greater =1;
flip_min = 0.1;
mean_signal = 0;


while signal_greater 
flip_max = 10;
flip_min = flip_min + 0.01;

mz_control = 1;
mz_tag = -inversion_efficiency;

sxy = (mz_control - mz_tag)  *sin( flip_min/180*pi);

%mz_control  = mz_control *cos( flip_min/180*pi)*exp(-tr/T1);
%mz_tag  = mz_tag *cos( flip_min/180*pi)*exp(-tr/T1);

mz_control  = 1 - ( 1 - mz_control )*exp(-tr/T1);    
mz_tag  = 1 - ( 1 - mz_tag )*exp(-tr/T1);    


for time = 1:sample_window
    
    desired_flip = 180/pi*asin( ( sxy / ( mz_control - mz_tag )));
    
    if desired_flip > flip_max
        flips(time:end) = flip_max;
        continue;
    else
        flips(time) = desired_flip;
        sxy = (mz_control - mz_tag)  *sin( desired_flip/180*pi);
        
        %mz_control  = mz_control *cos( desired_flip/180*pi); 
        %mz_tag  = mz_tag *cos( desired_flip/180*pi);

        mz_control  = 1 - ( 1 - mz_control )*exp(-tr/T1);    
        mz_tag  = 1 - ( 1 - mz_tag )*exp(-tr/T1);    
    end
end

%Check Flip angle Aproximation
mz_control = 1;
mz_tag = -inversion_efficiency;

for time = 1:sample_window
    
        sxy = (mz_control - mz_tag)  *sin( flips(time)/180*pi);
        
        %mz_control  = mz_control *cos( flips(time)/180*pi);
        %mz_tag  = mz_tag *cos( flips(time)/180*pi);

        mz_control  = 1 - ( 1 - mz_control )*exp(-tr/T1);    
        mz_tag  = 1 - ( 1 - mz_tag )*exp(-tr/T1);   
    
        sxy_act(time) = sxy;
    
end

if  sxy_act(end) > 0.75*sxy_act(1)
    signal_greater = 1;
    %mean_signal = mean( (sxy_act).^( 1/4) )
else
    signal_greater = 0;
end
    
end


%flips(:) = 8;
    
%%simulation parmeters
GAMMA = 4258.7*2*pi;
freq = 0;  %offresonance
M0 = 1;
eddy_phase = 0/180*pi;
TI = 50e-3;
FLIP_SUB = 0.0;
freq_vals = linspace(-1900,1900,601);
init_phase =pi;
step = pi;

x = -1000:3000;
x0 = -sample_window - tag_duration:0;

s_tag = ones(size(x0));
s_control = ones(size(x0));
sxy = [];


for time = 0:tag_duration + sample_window
    
    if time < tag_duration
        flip_tag     = (x==0).*180 * inversion_efficiency;
        flip_control = zeros(size(x));
    elseif time== tag_duration
        flip_tag     = (x > 0).*180;
        flip_control = 180.*ones(size(x));
    else
        flip_tag = (x > 0)*flips(time - tag_duration);
        flip_control = (x > 0)*flips(time - tag_duration);
    end
    flipt_tag = interp1(x,flip_tag,x0+time);
    flipt_control = interp1(x,flip_control,x0+time);
        
    s_tag = s_tag.*cos( flipt_tag/180*pi);
    sxy_tag = s_tag.*sin( flipt_tag/180*pi);
    s_tag = 1 - ( 1 - s_tag)*exp(-tr/T1);    
    
    s_control = s_control.*cos( flipt_control/180*pi);
    sxy_control = s_control.*sin( flipt_control/180*pi);
    s_control = 1 - ( 1 - s_control)*exp(-tr/T1);    
    
    if time > tag_duration
%         plot(s_tag - s_control)
% %     hold on
% %     plot(s_tag,'--k')
% %     plot(s_control,'.-r')
% %     hold off
% %     legend('Diff','Tag','Control')
%         ylim([-2.1 2.1]);
%         title(num2str(time));
%         pause(0.1)
        sdiff(time - tag_duration,:)=interp1(x0+time,s_tag-s_control,x);
        sxy(time - tag_duration,:) = interp1(x0+time,sxy_tag-sxy_control,x);
    end
end

figure('Position',[100 100 400 800])
subplot(211)
imagesc(sxy,[ 0 0.25])
xlabel('Position / Arrival Time');
ylabel('Time');
ylim([0 sample_window]);
xlim([1000 1000+sample_window+tag_duration]);
subplot(212)
plot(1:sample_window,flips);
xlabel('Time');
ylabel('Flip Angle');


mean_s = mean(sxy(:,1399))
std_s = std(sxy(:,1399))

% PCASL Simulations
[IMAGE TIMES] = fractal_phantom_time;
TIMES = floor( TIMES / max(TIMES(:)) * tag_duration * 1.6);



%Treat as single shot
angles = linspace(0,pi,sample_window+1);
order = bitreverse(sample_window);
angles = angles(1+order(1:sample_window));
kr = linspace(-255,255,255*4+1);
kr = [kr]; % 1i*kr]; % kr*exp(1i*pi/4) kr*exp(-1i*pi/4)];
kx = real(kr'*exp(1i*angles));
ky = imag(kr'*exp(1i*angles));
kdata = zeros(size(kx));

idx = isnan(TIMES);
TIMES(idx) = 0;
idx = TIMES ==0;
TIMES(idx) = 1;

idx = isnan(sdiff);
sdiff(idx) = 0;

figure
for pos = 1:size(kx,2)
    signal = sdiff(pos,:);
    signal2 = interp1(x,signal,0:sample_window+2*tag_duration+10);    
    SIGNAL = signal2(TIMES).*IMAGE;
    imagesc(SIGNAL,[0 1]); title(num2str(pos));
    drawnow
    kdata(:,pos) = backward_gridfft(kx(:,pos),ky(:,pos),SIGNAL,ones(size(kx(:,pos))),[size(IMAGE,1) size(IMAGE,2)],1,1); 
end

noise_kdata = 2e3*( randn(size(kdata)) + 1i*randn(size(kdata)));
simage = forward_gridfft(kx(:),ky(:),kdata(:) + noise_kdata(:),vorDCF(kx(:),ky(:)),[size(IMAGE,1) size(IMAGE,2)],2,1); 
%simage = l1_iterative_sense(kx(:),ky(:),kdata(:) + noise_kdata(:),ones(512,512),ones(512,512),1e-2);  



signal = sdiff(1,:);
signal2 = interp1(x,signal,0:sample_window+2*tag_duration+10);    
SIGNAL = signal2(TIMES).*IMAGE;
ideal_kdata = backward_gridfft(kx(:),ky(:),SIGNAL,ones(size(kx(:))),[size(IMAGE,1) size(IMAGE,2)],1,1); 
noise_ideal_kdata = 2e3*( randn(size(ideal_kdata)) + 1i*randn(size(ideal_kdata)));

%ideal_IMAGE = iterative_sense(kx(:),ky(:),ideal_kdata(:),ones(512,512),ones(512,512));  
ideal_IMAGE = forward_gridfft(kx(:),ky(:),ideal_kdata(:) + noise_ideal_kdata(:),vorDCF(kx(:),ky(:)),[size(IMAGE,1) size(IMAGE,2)],2,1); 

figure
ideal_IMAGE = ideal_IMAGE/max(ideal_IMAGE(:));
imshow(abs(ideal_IMAGE),[]); title('Ideal Image');


figure
simage = simage / max(simage(:));
imshow(abs(simage),[]); title('Actual Image');
    
    





for SPGR=[1]
    if SPGR ==1
        FLIP = 10
    else
        FLIP= 35
    end
        
for TI_pos = 1:length(TI_vals)
    %%%TR of each simulation block
    preps= 1;
    ramp_TRS   =  ones(1,preps)*TR/2;
    time_schedule = [ramp_TRS TR*ones(1,NTRS)];
    
    %%%RF phase
    phase_schedule=zeros(size(time_schedule));
    phase_schedule(1) = init_phase;
    phase_schedule(2:end) = step*(0 : (NTRS-1));
    
    %%%get times after IR
    time_vals = 0;
    time_vals(1)=0;
    for pos = 2:length(time_schedule)
        time_vals(pos) = time_vals(pos-1)+time_schedule(pos-1);
    end
    
    flip_schedule = [FLIP/2 FLIP*ones(1,NTRS)];
    
    for IR=[0 1]
        for rep=1:length(flip_schedule)
            if( rep ==1 )
                if IR==1
                    M_init = [ 0 0 (1 - 2*exp(-TI_vals(TI_pos)/T1))]';
                else
                    M_init = [0 0 1]';
                end
            else
                M_init = [Mx_TR My_TR Mz_TR]';
            end
            
            if SPGR==1
                M_init(1)=0;
                M_init(2)=0;
            end
            
            phase_rf = phase_schedule(rep);
            Rphase = [cos(phase_rf) sin(phase_rf) 0;
                -sin(phase_rf) cos(phase_rf) 0;
                0 0 1];
            Rphase2 = [cos(-phase_rf) sin(-phase_rf) 0;
                -sin(-phase_rf) cos(-phase_rf) 0;
                0 0 1];
            Rrf    = [cos(flip_schedule(rep)/180*pi)   0 -sin(flip_schedule(rep)/180*pi);
                0                         1       0;
                sin(flip_schedule(rep)/180*pi)   0  cos(flip_schedule(rep)/180*pi)];
            Mf = Rphase2*Rrf*Rphase*M_init;
            
            Mx_post_flip = Mf(1);
            My_post_flip = Mf(2);
            Mz_post_flip = Mf(3);
            
            net_phase = 2*pi*freq*time_schedule(rep)/2;
            Mx_half_TR= ( Mx_post_flip* cos( net_phase ) + My_post_flip*sin(net_phase ))*exp(-time_schedule(rep)/2/T2);
            My_half_TR= ( Mx_post_flip*-sin( net_phase ) + My_post_flip*cos(net_phase ))*exp(-time_schedule(rep)/2/T2);
            Mz_half_TR= ( M0-Mz_post_flip)*(1.0 - exp(-time_schedule(rep)/2/T1)) + Mz_post_flip;
            
            net_phase = 2*pi*freq*time_schedule(rep);
            Mx_TR= ( Mx_post_flip* cos( net_phase ) + My_post_flip*sin(net_phase ))*exp(-time_schedule(rep)/T2);
            My_TR= ( Mx_post_flip*-sin( net_phase ) + My_post_flip*cos(net_phase ))*exp(-time_schedule(rep)/T2);
            Mz_TR= ( M0-Mz_post_flip)*(1.0 - exp(-time_schedule(rep)/T1)) + Mz_post_flip;
            
            if IR==0
                Sxy(rep,TI_pos) = (Mx_half_TR+i*My_half_TR)*exp(-i*phase_schedule(rep));
                Sz(rep,TI_pos) = Mz_half_TR;
            else
                SxyIR(rep,TI_pos) = (Mx_half_TR+i*My_half_TR)*exp(-i*phase_schedule(rep));
                SzIR(rep,TI_pos) = Mz_half_TR;
            end
        end
    end
    
end

figure
plot(abs(mean(Sxy-SxyIR,1)))
title(['SPGR=',num2str(SPGR)]);

figure,
subplot(131),imagesc(TI_vals,TR*(1:NTRS),abs(Sxy)); title('No IR');
subplot(132),imagesc(TI_vals,TR*(1:NTRS),abs(SxyIR)); title('IR');
subplot(133),imagesc(TI_vals,TR*(1:NTRS),abs(Sxy-SxyIR),[0 max(abs(Sxy(:)-SxyIR(:)))]); title('Diff');
%title(['SPGR=',num2str(SPGR)]);

 %title(num2str(init_phase));
end
%

%imagesc(time_vals,init_vals,angle(signal));

break
%
% %%%get actual times
% time_vals = 0;
% time_vals(1)=0;
% for pos = 2:length(time_schedule)
%     time_vals(pos) = time_vals(pos-1)+time_schedule(pos-1);
% end
%
% time_mat = repmat(time_vals,[length(freq_vals) 1]);
% freq_mat = repmat(freq_vals',[1 length(time_vals)]);
%
% for s =1:2
%     figure('Position',[50 50 1500 600])
%     subplot(121)
%     imagesc(freq_vals,time_vals,abs(Sxy_NIR(s:2:end,:)));
%     title(['No IR: ',num2str(FLIP)],'FontSize',24);
%     ylabel('Time','FontSize',24);
%     set(gca,'FontSize',24);
%     xlabel('Freq','FontSize',16);
%
%     subplot(122)
%     imagesc(freq_vals,time_vals,abs(Sxy_IR(s:2:end,:)));
%     title(['IR: ',num2str(FLIP)],'FontSize',24);
%     ylabel('Time','FontSize',24);
%     set(gca,'FontSize',24);
%     xlabel('Freq','FontSize',16);
%
%
%
%     figure('Position',[50 50 1500 600])
%     subplot(121)
%     imagesc(freq_vals,time_vals,angle(Sxy_NIR(s:2:end,:)));
%     title(['No IR: ',num2str(FLIP)],'FontSize',24);
%     ylabel('Time','FontSize',24);
%     set(gca,'FontSize',24);
%     xlabel('Freq','FontSize',16);
%
%     subplot(122)
%     imagesc(freq_vals,time_vals,angle(Sxy_IR));
%     title(['IR: ',num2str(FLIP)],'FontSize',24);
%     ylabel('Time','FontSize',24);
%     set(gca,'FontSize',24);
%     xlabel('Freq','FontSize',16);
%
% end
%
%
