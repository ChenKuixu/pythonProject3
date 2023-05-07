import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
plt.rcParams['font.sans-serif'] = ['SimHei'] # 设置中文字体为SimHei
plt.rcParams['axes.unicode_minus'] = False # 解决负号无法正常显示的问题
# 定义高通巴特沃斯模拟滤波器函数
def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=True)
    return b, a

# 定义数字滤波器函数
def bilinear_transform(b, a, fs):
    # 将模拟滤波器转换为数字滤波器
    bz, az = signal.bilinear(b, a, fs)
    return bz, az

# 设计一个高通巴特沃斯模拟滤波器，截止频率为100Hz
fs = 1000 # 采样率
cutoff = 100 # 截止频率
order = 4 # 阶数
b, a = butter_highpass(cutoff, fs, order)

# 将模拟滤波器转换为数字滤波器
bz, az = bilinear_transform(b, a, fs)

# 计算数字滤波器的幅度响应、相位响应、零极点和群延迟
w, h = signal.freqz(bz, az)
magnitude = np.abs(h)
phase = np.angle(h)
zeros, poles, _ = signal.tf2zpk(bz, az)
w, gd = signal.group_delay((bz, az))

# 绘制幅度响应图像
plt.figure()
plt.plot(w/np.pi*fs/2, magnitude)
plt.xlabel('频率 (Hz)')
plt.ylabel('幅度响应')
plt.title('高通巴特沃斯数字滤波器幅度响应')
plt.grid(True)
#plt.show()

# 绘制相位响应图像
plt.figure()
plt.plot(w/np.pi*fs/2, phase)
plt.xlabel('频率 (Hz)')
plt.ylabel('相位响应')
plt.title('高通巴特沃斯数字滤波器相位响应')
plt.grid(True)
#plt.show()

# 绘制零极点图
plt.figure()
plt.scatter(np.real(zeros), np.imag(zeros), marker='o', color='blue', label='零点')
plt.scatter(np.real(poles), np.imag(poles), marker='x', color='red', label='极点')
plt.xlabel('实部')
plt.ylabel('虚部')
plt.title('高通巴特沃斯数字滤波器零极点图')
plt.legend()
plt.grid(True)
#plt.show()

# 绘制群延迟图像
plt.figure()
plt.plot(w/np.pi*fs/2, gd)
plt.xlabel('频率 (Hz)')
plt.ylabel('群延迟 (样本)')
plt.title('高通巴特沃斯数字滤波器群延迟')
plt.grid(True)
plt.show()