from ecg_gudb_database import GUDb
import matplotlib.pyplot as plt
import numpy as np


def DC_notch(ecg_data, numoftaps, sample_rate):
    initsignal = np.ones(numoftaps)
    initsignal[0:int(5 / sample_rate * numoftaps)] = 0
    initsignal[numoftaps - int(5 / sample_rate * numoftaps):numoftaps] = 0
    initsignal_freq = np.fft.ifft(initsignal)
    length = numoftaps
    impuse_response = np.zeros(length)
    impuse_response[0:length // 2] = initsignal_freq[length // 2:length]
    impuse_response[length // 2:length] = initsignal_freq[0:length // 2]
    h = impuse_response * np.hamming(length)
    from fir_filter import FIR_filter
    FIR_filter = FIR_filter(h)
    filtered_ecg = []
    for i, v in enumerate(data):
        filtered_ecg.append(FIR_filter.dofilter(v))

    return filtered_ecg


def Detect_Rpeaks(signal, detect_range): # detect_range = 200
    R_peaks = []
    location = []
    for i in np.arange(1, len(signal) - 1):


        if signal[i] > signal[i - 1] and signal[i] > signal[i + 1]:  # 和信号的两边的值比较
            max_flag = 1

            ######################################修改部分#############
            if signal[i] < abs(signal[i - 1]): # 比较信号两边的绝对值
                max_flag = 0
            #########################################################

            for j in range(1, detect_range): # 和前两百个点比较

                if signal[i] < signal[i - j]:
                    max_flag = 0 # 如果小于前两百的任何一个，则不标为最大
                    break

                if signal[j] > signal[i] / 2:# 此标记的一半的值若小于前两百的任何一个点，则不标为最大
                    max_flag = 0
                    break

            if max_flag == 1: # 若为峰值，存贮信号和位置
                R_peaks.append(signal[i])
                location.append(i)
    return R_peaks, location


def Cal_mome_heartrate(location, sample_rate):
    mome_heartrate = []
    for i in range(len(location) - 1):
        interval = location[i + 1] - location[i]
        time_interval = interval / sample_rate
        heartrate = int(60 / time_interval)
        mome_heartrate.append(heartrate)
    # print(mome_heartrate)
    return mome_heartrate

#
if __name__ == '__main__':
    data = np.loadtxt('ECG_data.dat')
    # data = data[500:1300] # 心电数据
    sample_rate = 250 #采样速率

    ##############修改#####################
    detect_range = 200 # 检测范围
    #####################################

    numoftaps = 500
    time = np.arange(0, len(data)) * (1.0 / sample_rate) # 采样数据的时间长度
    filtered_ecg = DC_notch(data, numoftaps, sample_rate) # 自定义函数，直流滤波

    R_peaks, location = Detect_Rpeaks(filtered_ecg, detect_range) # 自定义函数，检测心率峰值
    plt.plot(data, label="org ECG") # 画原始数据图
    plt.plot(filtered_ecg, label="Filtered ECG") # 画滤波数据图
    plt.scatter(location, R_peaks, color="red") # 标记峰值点
    plt.xlabel('Time \s')
    plt.legend()
    plt.show() # 显示图

    mome_heartrate = Cal_mome_heartrate(location, sample_rate) # 自定义函数，计算心率
    print(mome_heartrate) # 打印显示心率

    # subject number to load, starting at 0
    subject_number = 0
    # print experiments
    print("Experiments:", GUDb.experiments)
    # experiment to load
    experiment = 'walking'
    # creating class which loads the experiment
    ecg_class = GUDb(subject_number, experiment)

    # getting the raw ECG data numpy arrays from class
    chest_strap_V2_V1 = ecg_class.cs_V2_V1
    einthoven_i = ecg_class.einthoven_I
    einthoven_ii = ecg_class.einthoven_II
    einthoven_iii = ecg_class.einthoven_III

    # getting filtered ECG data numpy arrays from class
    ecg_class.filter_data()
    chest_strap_V2_V1_filt = ecg_class.cs_V2_V1_filt # 滤波后的数据类
    einthoven_i_filt = ecg_class.einthoven_I_filt
    einthoven_ii_filt = ecg_class.einthoven_II_filt
    einthoven_iii_filt = ecg_class.einthoven_III_filt
    filtered_ecg = DC_notch(einthoven_iii_filt, numoftaps, sample_rate) # 直流滤波

    R_peaks, location = Detect_Rpeaks(filtered_ecg, detect_range) # 寻找峰值
    plt.plot(einthoven_iii_filt, label="org ECG")
    plt.plot(filtered_ecg, label="Filtered ECG")
    plt.scatter(location, R_peaks, color="red")
    plt.xlabel('Time \s')
    plt.legend()
    plt.show()

