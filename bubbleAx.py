import numpy as np
import matplotlib.pyplot as plt
import json
import codecs
from math import log
from matplotlib import rcParams
from math import sqrt

rcParams['font.sans-serif']=['SimHei']
rcParams['font.family']=['sans-serif']
rcParams['axes.unicode_minus']=False
class BubbleAx:
    def __init__(self,ax):
        self.ax=ax
        self.label = ["银行诈骗", "黑发票", "积分诈骗", "刷单招聘", "Apple诈骗", "移动短信", "小广告", "澳门赌博", "贷款抵押", "炒股诈骗",
                 "特殊服务"]
        self.listcolor = ['r', 'orange', 'yellow', '#40fd14', '#019529', '#2afeb7', '#d5ffff', '#fa5ff7', '#ffd1df', '#fe7b7c', '#770001']
        self.selected = None
        self.sum = 0

    def draw(self, aDay='20170304'):
        data = json.load(codecs.open('config/textCato/20170223.json', 'r', 'utf-8-sig'))
        area = []
        colors = []
        self.annote = []
        plt.sca(self.ax)
        if len(self.ax.collections)>0:
            self.ax.collections.pop()
        sum = 0
        for key, cato in data.items():
            index = self.label.index(key)
            color = self.listcolor[index]
            for text, num in cato.items():
                sum += 1
                if num == 0:
                    radius = 0
                else:
                    radius = np.pi * (1.5011 * log(num)) ** 2
                    # radius = np.pi * (0.0011 * (num))**2
                area.append(radius)
                colors.append(color)
                self.annote.append(key+'\n'+text)

        self.x = np.random.rand(sum)
        self.y = np.random.rand(sum)
        plt.scatter(self.x, self.y, s=area, c=colors, alpha=0.8)
        self.ax.set_xlim(-0.05, 1.05 )
        self.ax.set_ylim(-0.08, 1.08 )
        self.sum = sum
        # if self.selected is not None:
        #     plt.annotate(annote[self.selected],(x[self.selected],y[self.selected]))
    def onMouseMove(self,event):
        if event.xdata is None:
            return
        distance = np.array([sqrt((self.x[i]-event.xdata)**2+(self.y[i]-event.ydata)**2) for i in range(len(self.x))])
        plt.sca(self.ax)
        index = np.argmin(distance)
        # print(index)
        # print(self.annote[index],(self.x[index],self.y[index]))
        self.ax.texts = []
        plt.annotate(self.annote[index],(self.x[index],self.y[index]),xytext=(self.x[index]+0.05,self.y[index]),arrowprops=dict(facecolor='b', shrink=0.75,alpha=0.6),verticalalignment='center',)
        self.ax.figure.canvas.draw()
        # paths = self.ax.collections[0].get_paths()
        # for index,path in enumerate(paths):
        #     if path.contains_point((event.xdata,event.ydata)):
        #         print(index)


if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.gca()
    bubbleAx=BubbleAx(ax)

    fig.canvas.mpl_connect('motion_notify_event', bubbleAx.onMouseMove)
    # ax = plt.subplots(facecolor="dodgerblue")
    name='20170301'
    bubbleAx.draw(name)
    plt.show()
