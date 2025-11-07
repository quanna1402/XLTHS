%% ================================================
%  CHỦ ĐỀ: LỌC NHIỄU TÍN HIỆU ÂM THANH GIẢ LẬP
%  Mục tiêu:
%   - Tạo tín hiệu âm thanh ảo (giọng nói mô phỏng bằng sóng sin)
%   - Thêm nhiễu trắng và nhiễu 50Hz
%   - Lọc bằng bộ lọc FIR và IIR
%   - So sánh kết quả lọc (đồ thị & âm thanh)
%  ------------------------------------------------
%  Ngôn ngữ: MATLAB
%  ------------------------------------------------

clc; clear; close all;

# 1. TẠO TÍN HIỆU ÂM THANH GIẢ LẬP
Fs = 8000;                % Tần số lấy mẫu (Hz)
t = 0:1/Fs:5;             % Thời gian 5 giây
f1 = 440; f2 = 660;       % Hai tần số mô phỏng (A4 và E5)
x = 0.6*sin(2*pi*f1*t) + 0.4*sin(2*pi*f2*t);  % Âm thanh tổng hợp

# 2. THÊM NHIỄU TRẮNG + NHIỄU 50Hz
white_noise = 0.2*randn(size(x));    % Nhiễu trắng
f_noise = 50;                        % Nhiễu 50Hz
hum_noise = 0.3*sin(2*pi*f_noise*t); % Nhiễu nguồn điện
x_noisy = x + white_noise + hum_noise;

# 3. THIẾT KẾ BỘ LỌC FIR THÔNG DẢI
Wn = [100 3000]/(Fs/2);    % Dải thông (100Hz–3kHz)
N = 80;                    % Bậc lọc FIR
b_fir = fir1(N, Wn, 'bandpass'); 
y_fir = filter(b_fir, 1, x_noisy);

#4. THIẾT KẾ BỘ LỌC IIR (BUTTERWORTH)
[b_iir, a_iir] = butter(6, Wn, 'bandpass');
y_iir = filter(b_iir, a_iir, x_noisy);

# 5. VẼ ĐỒ THỊ TÍN HIỆU
figure('Name','So sánh tín hiệu trước và sau lọc');
subplot(3,1,1);
plot(t, x_noisy); title('Tín hiệu có nhiễu');
xlabel('Thời gian (s)'); ylabel('Biên độ');

subplot(3,1,2);
plot(t, y_fir); title('Tín hiệu sau lọc FIR');
xlabel('Thời gian (s)'); ylabel('Biên độ');

subplot(3,1,3);
plot(t, y_iir); title('Tín hiệu sau lọc IIR');
xlabel('Thời gian (s)'); ylabel('Biên độ');
sgtitle('So sánh kết quả lọc tín hiệu âm thanh giả lập');

# 6. PHÂN TÍCH MIỀN TẦN SỐ
n = length(x);
f = (0:n-1)*(Fs/n);
X_noisy = abs(fft(x_noisy));
Y_fir = abs(fft(y_fir));
Y_iir = abs(fft(y_iir));

figure('Name','Phổ biên độ tín hiệu');
plot(f(1:n/2), X_noisy(1:n/2), 'r', 'DisplayName','Tín hiệu có nhiễu'); hold on;
plot(f(1:n/2), Y_fir(1:n/2), 'b', 'DisplayName','Sau lọc FIR');
plot(f(1:n/2), Y_iir(1:n/2), 'g', 'DisplayName','Sau lọc IIR');
xlabel('Tần số (Hz)'); ylabel('Biên độ');
legend; grid on;
title('Phổ biên độ tín hiệu trước và sau lọc');

#️ 7. NGHE KẾT QUẢ
disp('▶️ Phát tín hiệu có nhiễu...');
sound(x_noisy, Fs); pause(3);

disp('▶️ Phát tín hiệu sau lọc FIR...');
sound(y_fir, Fs); pause(3);

disp('▶️ Phát tín hiệu sau lọc IIR...');
sound(y_iir, Fs);

disp('✅ Hoàn tất! Đã lọc và so sánh FIR/IIR cho tín hiệu giả lập.');

