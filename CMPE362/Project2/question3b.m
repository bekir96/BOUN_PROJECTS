clear;
close all;
clc;
filename = "p232_090.wav";
[ySignal, Fs] = audioread(filename);

filename = "p232_090_noise.wav";
[yNoise, Fs] = audioread(filename);
length = size(yNoise,1);
f0 = (-length/2:length/2-1)*(fs/length);

T = 1 / Fs;


%%

Y = fft(yNoise - ySignal);

L = 189269;

P2 = abs(Y/L);
P1 = P2(1:ceil(L/2));
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:(L/2))/L;

figure, plot(f,P1);


%%
Y = fft(ySignal);

L = 189269;

P2 = abs(Y/L);
P1 = P2(1:ceil(L/2));
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:(L/2))/L;

figure, plot(f,P1);

%%
zeroLele = zeros(length,1); 
upper = 24000; 
lower = 2000;
for i = 1:1:length
    if f0(i) > lower && f0(i) < upper
        zeroLele(i) = 1.0;
    end
    if f0(i) < -lower && f0(i) > -upper
        zeroLele(i) = 1.0;
    end
end
shift = ifftshift(zeroLele');
shift = ifft(shift);
c = cconv(abs(shift), y');
x = size(c);
 
c = c(1:ceil(x(2) / 2));