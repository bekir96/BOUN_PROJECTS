%%  IDEAL FILTER SECTION
clear;
close all;
clc;
filename = "p232_090.wav";
[ySignal, Fs] = audioread(filename);

filename = "p232_090_noise.wav";
[yNoise, Fs] = audioread(filename);

T = 1 / Fs;

% fft transform of clean
fftY = fft(y);
fftY = fftshift(fftY);

% fft transform of noisy
fftYNoise = fft(yNoise);
fftYNoise = fftshift(fftYNoise);
 
% divide of clean / noise
fftDivide = fftY' ./ fftYNoise';
 
figure,plot(abs(fftDivide));
 
a = ifftshift(fftDivide);
a = ifft(a); 
figure,plot(a); 
c = cconv(a, yNoise');
figure, plot(y); 
x=size(c);
 
c = c(1:ceil(x(2) / 2));
 
figure, plot(c);