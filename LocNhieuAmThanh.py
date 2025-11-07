"""
CHỦ ĐỀ: LỌC NHIỄU TÍN HIỆU ÂM THANH GIẢ LẬP
Mục tiêu:
 - Tạo tín hiệu âm thanh ảo (giọng nói mô phỏng bằng sóng sin)
 - Thêm nhiễu trắng và nhiễu 50Hz
 - Lọc bằng bộ lọc FIR và IIR
 - So sánh kết quả lọc (đồ thị & âm thanh)
 
Ngôn ngữ: Python
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Dùng backend không cần GUI
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import sounddevice as sd
import time, os

plt.rcParams['font.family'] = 'DejaVu Sans'

print("Khởi tạo chương trình lọc nhiễu tín hiệu âm thanh...")

# 1. TẠO TÍN HIỆU ÂM THANH GIẢ LẬP 
Fs = 8000                    # Tần số lấy mẫu (Hz)
duration = 5                 # Thời gian 5 giây
t = np.arange(0, duration, 1/Fs)
f1, f2 = 440, 660
x = 0.6*np.sin(2*np.pi*f1*t) + 0.4*np.sin(2*np.pi*f2*t)
print(f"# Đã tạo tín hiệu ảo {duration}s, Fs = {Fs}Hz")

# 2. THÊM NHIỄU 
white_noise = 0.2*np.random.randn(len(x))
f_noise = 50
hum_noise = 0.3*np.sin(2*np.pi*f_noise*t)
x_noisy = x + white_noise + hum_noise
print("# Đã thêm nhiễu trắng + nhiễu 50Hz")

# 3. LỌC FIR 
Wn = np.array([100, 3000]) / (Fs/2)
N = 80
b_fir = signal.firwin(N+1, Wn, pass_zero=False)
y_fir = signal.lfilter(b_fir, 1, x_noisy)
print(f"# Bộ lọc FIR bậc {N} đã tạo xong")

# 4. LỌC IIR 
b_iir, a_iir = signal.butter(6, Wn, btype='bandpass')
y_iir = signal.lfilter(b_iir, a_iir, x_noisy)
print("# Bộ lọc IIR Butterworth bậc 6 đã tạo xong")

# 5. VẼ & LƯU HÌNH MIỀN THỜI GIAN 
fig1 = plt.figure(figsize=(12, 8))
plt.subplot(3, 1, 1)
plt.plot(t, x_noisy, 'r', linewidth=0.5)
plt.title('Tín hiệu có nhiễu')
plt.xlabel('Thời gian (s)'); plt.ylabel('Biên độ'); plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(t, y_fir, 'b', linewidth=0.5)
plt.title('Sau lọc FIR'); plt.xlabel('Thời gian (s)'); plt.ylabel('Biên độ'); plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(t, y_iir, 'g', linewidth=0.5)
plt.title('Sau lọc IIR'); plt.xlabel('Thời gian (s)'); plt.ylabel('Biên độ'); plt.grid(True)

plt.suptitle('So sánh kết quả lọc tín hiệu âm thanh', fontsize=14, fontweight='bold')
plt.tight_layout()
fig1_path = "do_thi_mien_thoi_gian.png"
plt.savefig(fig1_path, bbox_inches='tight', dpi=300)
plt.close()
print(f"# Đã lưu hình miền thời gian → {fig1_path}")

# 6. VẼ VÀ LƯU PHỔ TẦN 
n = len(x)
f = np.arange(0, n) * (Fs/n)
X_noisy = np.abs(np.fft.fft(x_noisy))
Y_fir = np.abs(np.fft.fft(y_fir))
Y_iir = np.abs(np.fft.fft(y_iir))

fig2 = plt.figure(figsize=(12, 6))
plt.plot(f[:n//2], X_noisy[:n//2], 'r', label='Tín hiệu có nhiễu')
plt.plot(f[:n//2], Y_fir[:n//2], 'b', label='Sau lọc FIR')
plt.plot(f[:n//2], Y_iir[:n//2], 'g', label='Sau lọc IIR')
plt.xlabel('Tần số (Hz)'); plt.ylabel('Biên độ')
plt.title('Phổ biên độ tín hiệu trước và sau lọc')
plt.legend(); plt.grid(True)
plt.tight_layout()
fig2_path = "do_thi_pho_tan.png"
plt.savefig(fig2_path, bbox_inches='tight', dpi=300)
plt.close()
print(f"# Đã lưu hình phổ tần → {fig2_path}")

# 7. NGHE KẾT QUẢ 
print("\nĐang phát âm thanh...")
x_noisy_norm = x_noisy / np.max(np.abs(x_noisy))
y_fir_norm = y_fir / np.max(np.abs(y_fir))
y_iir_norm = y_iir / np.max(np.abs(y_iir))

try:
    print("# Phát tín hiệu có nhiễu...")
    sd.play(x_noisy_norm, Fs)
    time.sleep(duration + 0.5)
    print("# Phát sau lọc FIR...")
    sd.play(y_fir_norm, Fs)
    time.sleep(duration + 0.5)
    print("# Phát sau lọc IIR...")
    sd.play(y_iir_norm, Fs)
    time.sleep(duration + 0.5)
except Exception as e:
    print(f"???  Không thể phát âm thanh: {e}")
    print("!!! Dùng lệnh: pip install sounddevice")

# 8. LƯU FILE ÂM THANH 
wavfile.write('tin_hieu_nhieu.wav', Fs, (x_noisy_norm * 32767).astype(np.int16))
wavfile.write('tin_hieu_fir.wav', Fs, (y_fir_norm * 32767).astype(np.int16))
wavfile.write('tin_hieu_iir.wav', Fs, (y_iir_norm * 32767).astype(np.int16))
print("/SAVE/ Đã lưu 3 file WAV trong thư mục hiện tại.")

# 9. MỞ HÌNH ẢNH 
try:
    os.startfile(fig1_path)
    os.startfile(fig2_path)
except Exception:
    print("# Không thể mở ảnh tự động, hãy mở thủ công.")

print("\n# Hoàn tất chương trình lọc và lưu kết quả.")

