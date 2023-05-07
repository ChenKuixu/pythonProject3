import numpy as np
from scipy.signal import butter, freqs, bilinear, tf2zpk#, zpk2tf
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei'] # 设置中文字体为SimHei
plt.rcParams['axes.unicode_minus'] = False # 解决负号无法正常显示的问题
# 巴特沃斯模拟滤波器设计
def butterworth_filter(cutoff_freq, sampling_freq, order=5, filter_type='low'):
    nyq_freq = 0.5 * sampling_freq
    normalized_cutoff_freq = cutoff_freq / nyq_freq

    b, a = butter(order, normalized_cutoff_freq, btype=filter_type, analog=True)

    return b, a

# 设计一个低通巴特沃斯滤波器，截止频率为1000Hz，采样频率为44100Hz，阶数为5
b, a = butterworth_filter(1000, 44100, order=5, filter_type='low')

# 使用双线性变换法将模拟滤波器转换为数字滤波器
sampling_freq = 44100
cutoff_freq = 1000
nyq_freq = 0.5 * sampling_freq
normalized_cutoff_freq = cutoff_freq / nyq_freq

# 计算双线性变换参数
b_digital, a_digital = bilinear(b, a, sampling_freq)

# 计算数字滤波器的幅度响应和相位响应
w, h = freqs(b_digital, a_digital, worN=8000)
magnitude = 20 * np.log10(abs(h))
phase = np.unwrap(np.arctan2(np.imag(h), np.real(h))) * 180 / np.pi

# 计算数字滤波器的零极点分布
z, p, k = tf2zpk(b_digital, a_digital)

# 计算数字滤波器的群延迟
group_delay = -(np.diff(np.unwrap(np.angle(h))) / np.diff(w))[0]

# 绘制数字滤波器的幅度响应和相位响应曲线
fig, ax = plt.subplots(2, 1, figsize=(8, 8))
ax[0].plot(w, magnitude)
ax[0].set(title='数字滤波器的幅度响应', xlabel='频率 (Hz)', ylabel='幅度 (dB)')
ax[1].plot(w, phase)
ax[1].set(title='数字滤波器的相位响应', xlabel='频率 (Hz)', ylabel='相位 (度)')
plt.tight_layout()
plt.show()

# 绘制数字滤波器的零极点分布
plt.figure(figsize=(8, 8))
plt.scatter(np.real(z), np.imag(z), marker='o', s=100, facecolors='none', edgecolors='r')
plt.scatter(np.real(p), np.imag(p), marker='x', s=100, color='b')
plt.legend(['零点', '极点'])
plt.title('数字滤波器的零极点分布')
plt.xlabel('实轴')
plt.ylabel('虚轴')
plt.grid(True)
plt.show()

# 绘制数字滤波器的群延迟曲线
plt.figure(figsize=(8, 4))
plt.plot(w[1:], group_delay)
#plt.plot(w[:-1], group_delay)
plt.title('数字滤波器的群延迟')
plt.xlabel('频率 (Hz)')
plt.ylabel('延迟 (秒)')
plt.grid(True)
plt.show()