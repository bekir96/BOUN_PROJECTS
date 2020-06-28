clear;
clc;
close all;

t = 0:0.001:20; % time variable with 0.001 step size

a = cos(2 * pi * 1 / 2 * t);    % first cos signal
b = cos(2 * pi * 1 / 3 * t);    % second cos signal

c = a + b;  % sum of these signals

%% UNDERSAMPLING

figure('Name','UNDERSAMPLING','NumberTitle','off');
plot(t, c); hold on;

Fs = 0.5;   % sampling rate

n = 0:1/Fs:20;  

x = c(1:1/Fs*1000:20*1000+1);   % sampled points at fs 0.5

stem(n, x); hold on;

% sign interpolation
y = zeros(1,size(t,2));
for i = 1:size(x,2)
    
    y = y + x(i) * sinc((t - ((i - 1) * 1 /Fs)) * Fs);

end

plot(t, y);


%% NYQUIST SAMPLING

figure('Name','NYQUIST SAMPLING','NumberTitle','off');
plot(t, c); hold on;

Fs = 1.1;

n = 0:1/Fs:20;  

x = c(1:1/Fs*1000:20*1000+1);   % sampled points at fs 1.1

stem(n, x); hold on;

% sign interpolation
y = zeros(1,size(t,2));
for i = 1:size(x,2)
    
    y = y + x(i) * sinc((t - ((i - 1) * 1 /Fs)) * Fs);

end

plot(t, y);

%% OVERSAMPLING

figure('Name','OVERSAMPLING','NumberTitle','off');
plot(t, c); hold on;

Fs = 5;

n = 0:1/Fs:20;  

x = c(1:1/Fs*1000:20*1000+1);   % sampled points at fs 5.0

stem(n, x); hold on;

% sign interpolation
y = zeros(1,size(t,2));
for i = 1:size(x,2)
    
    y = y + x(i) * sinc((t - ((i - 1) * 1 /Fs)) * Fs);

end

plot(t, y);

