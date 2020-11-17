# -*- coding: utf-8 -*-
import unittest
import numpy as np
class FIR_filter:
    def __init__(self, coeffiients):
        self.bufferlength = 500
        self.newbuffer = list(np.zeros(self.bufferlength - 1))
        self.coeffiients = coeffiients # 计算的h系数
        self.output = 0

    def dofilter(self, v):
        self.newbuffer.append(v) # 499个为零的list加上一个data_x[i]
        # self.newbuffer[0] = 1
        self.output = 0
        for i in range(self.bufferlength):
            self.output += self.coeffiients[i] * self.newbuffer[(self.bufferlength-1 ) - i]
            # h正序列系数点乘newbuffer反序列并迭代相加
        self.newbuffer = self.newbuffer[1:] # 变成一维数组
        return self.output

class Checkfilter(unittest.TestCase):
    def test_dofilter(self, h=np.zeros(500), v=6):
        print("test filter")
        test = FIR_filter(h)
        print(test.dofilter(v))

if __name__ == '__main__':
    unittest.main()
