import wave
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei'] # 设置中文字体为SimHei
plt.rcParams['axes.unicode_minus'] = False # 解决负号无法正常显示的问题



def plot_waveform_and_spectrum(wav_file):
    # 打开wav文件
    with wave.open(wav_file, 'r') as wf:
        num_channels = wf.getnchannels() # 声道数
        sample_width = wf.getsampwidth() # 采样宽度（字节数）
        frame_rate = wf.getframerate() # 采样率
        num_frames = wf.getnframes() # 采样点数

        # 读取所有采样点的数据
        binary_data = wf.readframes(num_frames)
        # 将二进制数据转换为采样值
        if sample_width == 1:
            # 对于8位采样宽度的数据，将其映射到[-1, 1]范围内
            data = (np.frombuffer(binary_data, dtype=np.uint8)-128)/128.0
        else:
            # 对于16位采样宽度的数据，将其映射到[-1, 1]范围内
            data = np.frombuffer(binary_data, dtype=np.int16)/32768.0

    # 创建窗口并显示时域和频域的两幅图像
    fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(14, 10))
    fig.suptitle('时域和频域波形')

    # 绘制时域波形
    x = np.arange(num_frames)/float(frame_rate)
    ax1.plot(x, data,color='green')
    ax1.set_title('时域波形')
    ax1.set_xlabel('时间（秒）')
    ax1.set_ylabel('幅值')

    # 计算频域波形
    freq_data = np.fft.fft(data)

    # 绘制频域波形
    freqs = np.fft.fftfreq(num_frames, 1.0/frame_rate)#计算频率
    freqs = freqs[:num_frames//2]#只取一半区间
    freq_data = np.abs(freq_data[:num_frames//2]) / num_frames#归一化
    ax2.plot(freqs, freq_data,color='red')
    ax2.set_title('频域波形')
    ax2.set_xlabel('频率（Hz）', color='Cyan')
    ax2.set_ylabel('幅值')

    plt.subplots_adjust(hspace=0.5)#调整子图间距
    plt.show()

#调用
plot_waveform_and_spectrum('test.wav')#test.wav是文件名