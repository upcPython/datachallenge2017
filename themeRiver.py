import numpy as np
import matplotlib.pyplot as plt
import math,os
import pandas as pd
from matplotlib import rcParams
rcParams['font.sans-serif']=['SimHei']
rcParams['font.family']=['sans-serif']
class ThemeRiver:
    def __init__(self,ax):
        self.ax=ax
        self.label = ["银行诈骗", "黑发票", "积分兑换诈骗", "淘宝刷单招聘", "Apple设备诈骗", "移动短信", "小广告", "澳门赌博", "贷款抵押", "炒股诈骗",
                 "特殊服务"]
        plt.sca(ax)

    def makedata(self,name):
        data = np.zeros((24, 11))
        df = pd.read_csv('config/riverCount/' + name + '.csv')
        count = list(df['count'])
        topic = list(df['topic'])
        hour = list(df['hour'])
        for j in range(len(topic)):
            if hour[j] < 24:
                data[hour[j]][topic[j]] = count[j]
        return data
    def draw(self, aDay='20170304'):
        data=self.makedata(aDay)
        plt.sca(self.ax)
        self.ax.collections = []
        a = plt.stackplot(range(24), data.T, baseline='wiggle')
        a[0].set_facecolor('r')
        a[1].set_facecolor('orange')
        a[2].set_facecolor('yellow')
        a[3].set_facecolor('#40fd14')
        a[4].set_facecolor('#019529')
        a[5].set_facecolor('#2afeb7')
        a[6].set_facecolor('#d5ffff')
        a[7].set_facecolor('#fa5ff7')
        a[8].set_facecolor('#ffd1df')
        a[9].set_facecolor('#fe7b7c')
        a[10].set_facecolor('#770001')

        plt.legend( self.label, bbox_to_anchor=(0.18, 0.45), ncol=1)


if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.gca()
    # ax = plt.subplots(facecolor="dodgerblue")
    dataAx=ThemeRiver(ax)
    name='20170304'
    dataAx.draw(name)
    plt.show()
