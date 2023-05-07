import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei'] # 设置中文字体为SimHei
plt.rcParams['axes.unicode_minus'] = False # 解决负号无法正常显示的问题
def analog_butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    return b, a

def digital_butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    b_digital, a_digital = signal.bilinear(b, a, fs)
    return b_digital, a_digital

# 设计模拟滤波器
fs = 1000  # 采样率
lowcut = 50  # 低频边界
highcut = 200  # 高频边界
order = 4  # 阶数
b, a = analog_butter_bandpass(lowcut, highcut, fs, order)

# 将模拟滤波器转换为数字滤波器
b_digital, a_digital = digital_butter_bandpass(lowcut, highcut, fs, order)

# 绘制幅度响应
w, h = signal.freqz(b_digital, a_digital)
plt.figure()
plt.plot((fs * 0.5 / np.pi) * w, abs(h))
plt.xlabel('频率/Hz')
plt.ylabel('幅度响应')
plt.title('带通巴特沃斯数字滤波器的幅度响应')
plt.grid(True)

# 绘制相位响应
plt.figure()
plt.plot((fs * 0.5 / np.pi) * w, np.unwrap(np.angle(h)))
plt.xlabel('频率/Hz')
plt.ylabel('相位响应')
plt.title('带通巴特沃斯数字滤波器的相位响应')
plt.grid(True)

# 绘制零极点图
zeros, poles, _ = signal.tf2zpk(b, a)
plt.figure()
plt.scatter(np.real(zeros), np.imag(zeros), marker='o', color='none', edgecolors='b', label='零点')
plt.scatter(np.real(poles), np.imag(poles), marker='x', color='r', label='极点')
plt.xlabel('实部')
plt.ylabel('虚部')
plt.title('带通巴特沃斯数字滤波器的零极点图')
plt.legend()

# 绘制群延迟
plt.figure()
plt.plot((fs * 0.5 / np.pi) * w, signal.group_delay((b_digital, a_digital), w)[1])
plt.xlabel('频率/Hz')
plt.ylabel('群延迟')
plt.title('带通巴特沃斯数字滤波器的群延迟')
plt.grid(True)





plt.show()
