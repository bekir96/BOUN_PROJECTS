image = imread("jokerimage.png");
image_red   = image(:, :, 1);
image_green = image(:, :, 2);
image_blue  = image(:, :, 3);
figure, imshow(image);

% Question 1 %
filter = [1 1 1 1 1 1 1; 1 1 1 1 1 1 1; 1 1 1 1 1 1 1; 1 1 1 1 1 1 1; 1 1 1 1 1 1 1; ...
        1 1 1 1 1 1 1; 1 1 1 1 1 1 1; ] / 49;
[f_size, p_size, new_image, filter, filter_image] = new_image_creator(7, image, filter);
a = filtering(filter_image, p_size, new_image, filter, f_size);
figure, imshow(uint8(a));


% Question 2 %
filter = [1 1 1; 1 1 1; 1 1 1] / 9;
[f_size, p_size, new_image, filter, filter_image] = new_image_creator(3, image, filter);
a = filtering(filter_image, p_size, new_image, filter, f_size);
figure, imshow(uint8(a));


filter = [-0.17 -0.67 -0.17; -0.67 4.33 -0.67; -0.17 -0.67 -0.17];
[f_size, p_size, new_image, filter, filter_image] = new_image_creator(3, a, filter);
a = filtering(filter_image, p_size, new_image, filter, f_size);
figure, imshow(uint8(a));


% Question 3 %
filter = [-1 -2 -1 ; 0 0 0; 1 2 1];
[f_size, p_size, new_image, filter, filter_image] = new_image_creator(3, image, filter);
a = filtering(filter_image, p_size, new_image, filter, f_size);
figure, imshow(uint8(a));

% Question 4 %
filter = [-2 -1 0 ; -1 1 1; 0 1 2];
[f_size, p_size, new_image, filter, filter_image] = new_image_creator(3, image, filter);
a = filtering(filter_image, p_size, new_image, filter, f_size);
figure, imshow(uint8(a));

function a = filtering(filter_image, p_size, new_image, filter, f_size)
    a = filter_image;
    for n = 1 :3
        for i = 1 + p_size:size(new_image, 1) - p_size
            for j = 1 + p_size:size(new_image, 2) - p_size
                sum = 0;
                for k = -(f_size - 1) / 2:(f_size - 1) / 2
                    for m = -(f_size - 1) / 2:(f_size - 1) / 2
                        sum = sum + new_image(i + k, j + m, n) * filter(k + ...
                        (f_size - 1) / 2 + 1, m + (f_size - 1) / 2 + 1);
                    end
                end
                a(i - p_size,j - p_size, n) = sum;
            end
        end
    end
end

function [f_size, p_size, new_image, filter, filter_image] = ...
        new_image_creator(size1, image, filter)
    f_size  = size1;
    p_size = (f_size - 1) / 2;

    new_image = zeros(2 * p_size + size(image,1), 2 * p_size + size(image,1), 3);
    new_image(1 + p_size:size(new_image, 1) - p_size, 1 + p_size:size(new_image, 1) ...
                - p_size, 1) = image(:, :, 1);
    new_image(1 + p_size:size(new_image, 1) - p_size, 1 + p_size:size(new_image, 1) ...
                - p_size, 2) = image(:, :, 2);
    new_image(1 + p_size:size(new_image, 1) - p_size, 1 + p_size:size(new_image, 1) ...
                - p_size, 3) = image(:, :, 3);

    filter = flip(filter, 1);
    filter = flip(filter, 2);
    filter_image = zeros(size(image,1), size(image,1), 3);
end