clear
clc

%% Blood 3.0T
T2 =  250;
T1 =  1664;
inversion_efficiency = 0.95;

%% Imaging Acquisition
FLIP = 9;                   % flip angle in degrees
tr = 5.1;                   % Imaging TR in ms
matrix = [320 320 320];     % Reconstructed matrix size
tag_durations = floor( [0 200 400 600 800 1000 1200]/tr);  % Tag durations
TI = 0;                     % TI in ms
sample_window = 500;        % sample window in ms

%% Options
export_results = 1;  % Save data to
show_results   = 1;  % Show images as they are generated
downsample     = 1;  % Reduce resolution for testing


%% Bloch Sim
%------------------------------------------
%    -This will populate an expected signal curve set
%-------------------------------------------

disp('Populating Time Curve Dictionary');

max_tag = max(tag_durations);
sample_window = floor(sample_window/tr); % convert to TR's for calculations

x = -3000:3000;
x0 = -sample_window - 2*max_tag - TI - 10:0;
time_range = 0:max_tag + sample_window/2 + TI;
for tpos = 1:numel(tag_durations)
    tag_duration = tag_durations(tpos);
    
    s_tag = ones(size(x0));
    s_control = ones(size(x0));
    
    for time = time_range
        if time < max_tag
            if (max_tag - time) < tag_duration
                flip_tag     = (x==0).*180 * inversion_efficiency;
                flip_control = zeros(size(x));
            else
                flip_tag = zeros(size(x));
                flip_control = zeros(size(x));
            end
        elseif time== max_tag
            flip_tag     = (x > 0).*180;
            flip_control = 180.*ones(size(x));
        elseif time < max_tag + TI
            flip_tag     = 0.*ones(size(x));
            flip_control = 0.*ones(size(x));
        else
            flip_tag = (x > 0).*FLIP;
            flip_control = (x > 0).*FLIP;
        end
        flipt_tag = interp1(x,flip_tag,x0+time);
        flipt_control = interp1(x,flip_control,x0+time);
        
        %Flip the signal
        s_tag = s_tag.*cos( flipt_tag/180*pi);
        
        %T1 Recovery
        s_tag = 1 - ( 1 - s_tag)*exp(-tr/T1);
        
        %Same for control
        s_control = s_control.*cos( flipt_control/180*pi);
        s_control = 1 - ( 1 - s_control)*exp(-tr/T1);
        
        %plot(s_tag)
        %pause
        
        if time > max_tag + TI
            %         plot(s_tag - s_control)
            % %     hold on
            % %     plot(s_tag,'--k')
            % %     plot(s_control,'.-r')
            % %     hold off
            % %     legend('Diff','Tag','Control')
            %         ylim([-2.1 2.1]);
            %         title(num2str(time));
            %         pause(0.1)
            sdiff(time - max_tag - TI,:,tpos)=interp1(x0+time,s_tag-s_control,x);
        end
    end
end

idx = isnan(sdiff);
sdiff(idx) = 0;
Savg = squeeze(sum(sdiff(:,3001+(1:(max_tag + sample_window+TI)),:),1));
disp('Done Populating Dictionary');


%% Load Data
%
%
disp('Loading Data');
Nt = numel(tag_durations);
IMAGES = zeros(matrix(1),matrix(2),matrix(3),Nt);
for t = 1:Nt
    name = sprintf('X_%03d_000.dat',t-1);
    disp(['  frame ',num2str(t),' filename = ',name]);
    fid = fopen(name);
    raw = fread(fid,'float');
    IMAGES(:,:,:,t) = reshape(raw,matrix);
    fclose(fid);
end
disp('Done Loading Data');

if downsample > 1
    disp('Downsampling:');
    IMAGES = IMAGES(1:downsample:end,1:downsample:end,1:downsample:end,:);
    disp(['  NEW RESOLUTION IS ',num2str(size(IMAGES))])
end

%% Fitting
%-------------------------------------------
%     Search for best fit
%-------------------------------------------

AA = Savg.*Savg;
SAA = sum(AA,2);

ArrivalTime = zeros(size(IMAGES,1),size(IMAGES,2),size(IMAGES,3));
Residue = ArrivalTime;
SignalEstimate = ArrivalTime;

disp('Fitting Data to Dictionary');
for z = 1:size(IMAGES,3)
    disp(['  Slice ',num2str(z),' of ',num2str(size(IMAGES,3))]);
    %%Find the best fit
    for x =1:size(IMAGES,1)
        for y =1:size(IMAGES,2)
            StTemp = squeeze(IMAGES(x,y,z,:));
            
            %%%Get the Scale
            St = ones(size(Savg,1),1)*StTemp(:)';
            AB = Savg.*St;
            L = (sum(AB,2)./SAA) *ones(1,numel(StTemp));
            
            %%Find the error
            Error = sum((St - L.*Savg).^2,2);
            [c,t]= min(Error);
            
            %Assign
            ArrivalTime(x,y,z) = tr*t; %Arrival Time
            Residue(x,y,z) = c; %Error
            SignalEstimate(x,y,z) = L(t,1); %Density / Signal Level
        end
    end
end

if export_results==1
    fid = fopen('SignalEstimate.dat','w');
    fwrite(fid,SignalEstimate,'float');
    fclose(fid);
    
    fid = fopen('Residue.dat','w');
    fwrite(fid,Residue,'float');
    fclose(fid);
    
    fid = fopen('ArrivalTime.dat','w');
    fwrite(fid,ArrivalTime,'float');
    fclose(fid);
end

%% Color Display
RGB =  uint8( zeros([3 size(ArrivalTime)]));

%%%Make a color image
max_ARR = 1.4*max(ArrivalTime(:));
min_ARR = 0.1*max(ArrivalTime(:));
range_ARR = max_ARR - min_ARR;
map =hsv(1025);

max_signal = max(SignalEstimate(:));

disp('Colorizing');
for z = 1:size(IMAGES,3)
    disp(['  Slice ',num2str(z),' of ',num2str(size(IMAGES,3))]);
    %%Find the best fit
    for x =1:size(IMAGES,1)
        for y =1:size(IMAGES,2)
            
            
            A = ArrivalTime(x,y,z);
            pos = ( A - min_ARR)/range_ARR*1025;
            if pos > 1025
                pos = 1025;
            elseif pos < 1
                pos = 1;
            else
                pos = round(pos);
            end
            
            RGB(1,x,y,z) = 255*map(pos,1)*SignalEstimate(x,y,z)/max_signal;
            RGB(2,x,y,z) = 255*map(pos,2)*SignalEstimate(x,y,z)/max_signal;
            RGB(3,x,y,z) = 255*map(pos,3)*SignalEstimate(x,y,z)/max_signal;
        end
    end
end

if export_results==1
    fid = fopen('ArrivalTimeRGB.dat','w');
    fwrite(fid,RGB,'uint8');
    fclose(fid);
end






