close all;

%% First part 
figure('Name','Triangle Wave','NumberTitle','off');
T = 1/25;  % period
t = 0:0.001:3*T; % time variable with 0.001 step size
x = sawtooth(2*pi*1/T*t,0.5)/2 + 0.5; % signal

plot(t,x);
title('Triangle Waveform (Period = 0.04 secs)');
xlabel('Time t(sec)'); ylabel('Amplitude'); 

%% Second part

figure('Name','Harmonic Summation','NumberTitle','off');

% DC & 1st harmonic & 3rd Harmonic
wZero = 50 * pi;    % wZero value
harmonicOne = -(2 / (pi ^ 2)) * exp(wZero * t * 1j); % 1st harmonics
harmonicThree = -(2 / (3 ^ 2 * pi ^ 2)) * exp(3 * wZero * t * 1j);  % 3rd harmonics
x3 = harmonicOne + harmonicThree + 0.5; % Sum of DC & 1st harmonic & 3rd Harmonic

subplot(2,1,1);
plot(t, abs(x3));
title('Sum of DC, 1st and 3rd Harmonics');
xlabel('Time t(sec)'); ylabel('x3(t)'); 

% DC & 1st through 11th Harmonic
harmonicFive = -(2 / (5 ^ 2 * pi ^ 2)) * exp(5 * wZero * t *1j);    % 5th harmonics
harmonicSeven = -(2 / (7 ^ 2 * pi ^ 2)) * exp(7 * wZero * t *1j);   % 7th harmonics
harmonicNine = -(2 / (9 ^ 2 * pi ^ 2)) * exp(9 * wZero * t *1j);    % 9th harmonics 
harmonicEleven= -(2 / (11 ^ 2 * pi ^ 2)) * exp(11 * wZero * t *1j); % 11th harmonics

x11 = harmonicOne + harmonicThree + harmonicFive + harmonicSeven + ...
    harmonicNine + harmonicEleven + 0.5;  % Sum of DC & 1st through 11th Harmonic
subplot(2,1,2);
plot(t,abs(x11));
title('Sum of DC and 1st through 11th Harmonics');
xlabel('Time t(sec)'); ylabel('x11(t)'); 

%% Third part

t = 0:0.001:T*50-0.001;  % time variable with 0.001 step size
x = sawtooth(2*pi*25*t,0.5)/2 + 0.5;  % signal
figure
y = fft(x);             % fft of x
n = length(x);          % number of samples

y0 = fftshift(y/n);         % shift y values
f0 = (-n/2:n/2-1)*(1000/n);
plot(f0,y0)
xlabel('Frequency Spectrum')

