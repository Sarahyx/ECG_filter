# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt


def create_filtersignal(numoftaps, cutoff1, cutout2):# 500 50 2
    initsignal = np.ones(numoftaps)
# 定义buffer数组值为1，sample_rate = 250
    k1 = int((cutoff1 - 5) / sample_rate * numoftaps) # 98
    k2 = int((cutoff1 + 5) / sample_rate * numoftaps) # 110
# k1、k2计算
    initsignal[k1:k2] = 0 # k1到k2值为零

    initsignal[numoftaps - k2:numoftaps - k1] = 0  # 390到402为零
    taps = np.linspace(0, sample_rate, numoftaps) # 0-250，单位0.5
    initsignal[0] = 0
    initsignal[499] = 0

    plt.subplot(3, 1, 1)
    plt.plot(taps, initsignal)
    plt.title("Filter signal")
# 画幅频特性图

    initsignal_freq = np.fft.ifft(initsignal) # 傅里叶逆变换
    plt.subplot(3, 1, 2)
    plt.plot(initsignal_freq) #
    plt.title('freq_domain signal')

    length = numoftaps
    impuse_response = np.zeros(length)
    impuse_response[0:length // 2] = initsignal_freq[length // 2:length]
    impuse_response[length // 2:length] = initsignal_freq[0:length // 2]
    h = impuse_response * np.hamming(length) # hamming窗口

    plt.subplot(3, 1, 3)
    plt.plot(taps, h)
    plt.title('signal with window')
    plt.show()
    return h


def RealTimeFiltering(ecg_dat, impuse_resonse):
    from fir_filter import FIR_filter
    FIR_filter = FIR_filter(impuse_resonse) # impuse_resonse为计算的h系数
    filtered_ecg = []
    for i, v in enumerate(ecg_dat): # 输入信号
        filtered_ecg.append(FIR_filter.dofilter(v)) #计算滤波
    return filtered_ecg


if __name__ == '__main__':
    data = np.loadtxt('ECG_data.dat')
    sample_rate = 250
    time = np.arange(0, len(data)) * (1.0 / sample_rate)
    data_mean = np.mean(data)
    DatawithoutDC = data - data_mean
    plt.plot(time,data,label="Orginal ECG")
    plt.plot(time,DatawithoutDC, label="ECG without DC.")
    plt.legend()
    plt.show()

    freq_data = abs(np.fft.fft(data))
    freqs = np.fft.fftfreq(data.size, 1 / sample_rate)
    plt.plot(freqs, freq_data)
    plt.show()

    numoftaps = 500
    cutoff_freq50 = 50
    cutoff_DC = 2
    coefficient = create_filtersignal(numoftaps, cutoff_freq50, cutoff_DC)
    filtered_ecg_cut50_cutDC = RealTimeFiltering(data, coefficient) # 实时滤波
    filtered_ecg_cut50_cutDC -= np.mean(filtered_ecg_cut50_cutDC)

    plt.plot(time, data, label="org ECG")
    plt.plot(time, filtered_ecg_cut50_cutDC, label="Filtered ECG")
    plt.xlabel('Time \s')
    plt.legend()
    plt.show()

    # np.savetxt("filteredECG.dat",filtered_ecg_cut50_cutDC)