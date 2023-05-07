import numpy as np
from scipy import signal
from scipy.signal import butter, freqz, freqs, bilinear, tf2zpk
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为SimHei
plt.rcParams['axes.unicode_minus'] = False  # 解决负号无法正常显示的问题


# 巴特沃斯模拟滤波器设计
def butterworth_lowpass(cutoff_freq, sampling_freq, order=5, filter_type='low'):  # 截止频率，采样频率，阶数
    nyq_freq = 0.5 * sampling_freq
    normalized_cutoff_freq = cutoff_freq / nyq_freq

    b, a = butter(order, normalized_cutoff_freq, btype=filter_type, analog=True)

    return b, a


# 设计一个低通巴特沃斯模拟滤波器，截止频率为1000Hz，采样频率为44100Hz，阶数为5
b, a = butterworth_lowpass(1000, 44100, order=5, filter_type='low')

# 使用双线性变换法将模拟滤波器转换为数字滤波器
sampling_freq = 44100
cutoff_freq = 1000
nyq_freq = 0.5 * sampling_freq
normalized_cutoff_freq = cutoff_freq / nyq_freq

# 计算双线性变换参数
b_digital, a_digital = bilinear(b, a, sampling_freq)

# 计算数字滤波器的幅度响应、相位响应和零极点分布以及群迟延
w_digital, h_digital = freqz(b_digital, a_digital)
magnitude_digital = 20 * np.log10(abs(h_digital))
phase_digital = np.angle(h_digital)
zeros_digital, poles_digital, gain_digital = tf2zpk(b_digital, a_digital)
w, h = freqs(b, a, worN=8000)
w1, gd = signal.group_delay((b, a))  # 这里用了w1，因为上面已经用了w

# #绘制数字滤波器的幅度响应曲线
plt.figure()
plt.plot(w_digital, magnitude_digital)
plt.title('数字滤波器的幅度响应')
plt.xlabel('频率 (弧度/秒)')
plt.ylabel('幅度 (dB)')
plt.grid(True)

# 绘制数字滤波器的相位响应曲线
plt.figure()
plt.plot(w_digital, phase_digital)
plt.title('数字滤波器的相位响应')
plt.xlabel('频率 (弧度/秒)')
plt.ylabel('相位 (弧度)')
plt.grid(True)

# 绘制数字滤波器的零极点分布
plt.figure()
plt.scatter(np.real(zeros_digital), np.imag(zeros_digital), marker='o', color='b')
plt.scatter(np.real(poles_digital), np.imag(poles_digital), marker='x', color='r')
plt.title('数字滤波器的零极点分布')
plt.xlabel('实部')
plt.ylabel('虚部')
plt.legend(['零点', '极点'])
plt.grid(True)

# 绘制数字滤波器的群迟延
plt.figure()
plt.plot(w1 / (2 * np.pi), gd)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Group Delay (seconds)')
plt.title('Group Delay Response of Butterworth Lowpass Analog Filter')
plt.grid(True)
plt.show()
