import numpy as np
import matplotlib.pyplot as plt
import math,os
import pandas as pd
from matplotlib import rcParams
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
rcParams['font.sans-serif']=['SimHei']
rcParams['font.family']=['sans-serif']
rcParams['axes.unicode_minus']=False
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
        max=0
        for i in range(24):
            for j in range(11):
                if data[i][j]>max:
                    max=data[i][j]
        plt.sca(self.ax)
        self.ax.yaxis.set_ticks_position('right')
        #self.ax.spines['top'].set_color('gold')
        #self.ax.spines['bottom'].set_color('gold')
        #self.ax.spines['right'].set_color('gold')
        #self.ax.spines['left'].set_color('gold')
        # self.ax.set_xticks([])
        # self.ax.set_yticks([])
        self.ax.collections = []
        a = plt.stackplot(range(24), data.T, baseline='wiggle')
        listcolor=['r','orange','yellow','#40fd14','#019529','#2afeb7','#d5ffff','#fa5ff7','#ffd1df','#fe7b7c','#770001']
        for i in range(11):
            #print(listcolor[i])
            a[i].set_facecolor(listcolor[i])
        plt.plot(facecolor='b')
        legend = plt.legend(self.label,frameon=False, bbox_to_anchor=(0.05, 1), ncol=1)
        ltext = legend.get_texts()
        plt.setp(ltext, fontsize=12)
        plt.xlabel('(小时)')
        plt.xticks(np.arange(0, 25, 4))
        plt.ylim(-max*1.8,max*1)

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.gca()
    # ax = plt.subplots(facecolor="dodgerblue")
    dataAx=ThemeRiver(ax)
    name='20170301'
    dataAx.draw(name)
    plt.show()
