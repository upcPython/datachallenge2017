import numpy as np
import matplotlib.pyplot as plt
import math,os
import pandas as pd
from matplotlib import rcParams
rcParams['font.sans-serif']=['SimHei']
rcParams['font.family']=['sans-serif']
class RiverPic:
    def __init__(self,pic):
        self.pic=pic

    def makedata(self, df):
        data = np.zeros((24, 11))
        count = list(df['count'])
        topic = list(df['topic'])
        hour = list(df['hour'])
        for j in range(len(topic)):
            if hour[j] < 24:
                data[hour[j]][topic[j]] = count[j]
        return data
    def makepic(self,data):
        plt.subplots(facecolor="dodgerblue")
        a = plt.stackplot(range(24), data.T, baseline='wiggle')
        heights = np.random.randn(11)
        values = np.array(heights)
        cmap = plt.cm.Blues
        errorbar_colors = cmap(values)
        # print(a)
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

        label = ["银行诈骗", "黑发票", "积分兑换诈骗", "淘宝刷单招聘", "Apple设备诈骗", "移动短信", "小广告", "澳门赌博", "贷款抵押", "炒股诈骗",
                 "特殊服务"]
        plt.legend( label, bbox_to_anchor=(0.18, 0.45), ncol=1)


if __name__ == "__main__":
    folder = 'count/'
    filenames = os.listdir(folder)
    df = pd.read_csv('count/' + '20170304.csv')
    pic=RiverPic(00)
    data=pic.makedata(df)
    pic.makepic(data)

    plt.show()
