import numpy as np
import matplotlib.pyplot as plt
import json
import codecs
from math import log
from matplotlib import rcParams
from math import fsum, sqrt
from matplotlib import patches

rcParams['font.sans-serif'] = ['SimHei']
rcParams['font.family'] = ['sans-serif']
rcParams['axes.unicode_minus'] = False


class RectTreeAx:
    def __init__(self, ax):
        self.ax = ax
        self.label = ["银行\n诈骗", "黑\n发票", "积分\n诈骗", "刷单\n招聘", "Apple\n诈骗", "移动\n短信", "小\n广告", "澳门\n赌博",
                      "贷款\n抵押", "炒股\n诈骗", "特殊\n服务"]
        self.listcolor = ['r', 'orange', 'yellow', '#40fd14', '#019529', '#2afeb7', '#d5ffff', '#fa5ff7', '#ffd1df',
                          '#fe7b7c', '#770001']
        self.selected = None
        self.first = True
        self.topic = -1
        self.data = None
        self.xlim = 380
        self.ylim = 200
        self.b = []
        self.textlevel = [56, 56 / 2, 56 / 3, 56 / 4]

    def write(self, width, height, start, i, list):
        if width > 30 and height > 20:
            s = width * height
            sboard = self.xlim * self.ylim
            if s >= sboard / 2:
                textsize = self.textlevel[0]
            elif s >= sboard / 4:
                textsize = self.textlevel[1]
            elif s >= sboard / 8:
                textsize = self.textlevel[2]
            else:
                textsize = self.textlevel[3]
            self.a.append(
                plt.text(start[0] + width / 2, start[1] + height / 2,
                         list[i][0], size=textsize,
                         horizontalalignment='center', verticalalignment='center'))
        else:
            self.annote[i] = list[i][0]
            self.x[i] = start[0] + width / 2
            self.y[i] = start[1] + height / 2

    def drawrectangle(self, list):
        self.areas = []
        self.a = []
        self.annote = {}
        self.x = {}
        self.y = {}
        plt.sca(self.ax)
        widthleft = self.xlim
        heightleft = self.ylim
        self.ax.set_xlim((0, self.xlim))
        self.ax.set_ylim((0, self.ylim))
        list.sort(key=lambda x: x[1], reverse=True)
        # print(list)
        start = [0, 0]

        for i in range(len(list)):
            listsum = fsum(x[1] for x in list[i:])
            if listsum == 0:
                break
            if i % 2 == 0:
                # print(list[i][1], listsum, widthleft)
                width = (list[i][1] / listsum) * widthleft
                # print(width)
                height = heightleft
                self.ax.add_patch(
                    patches.Rectangle(
                        start,  # (x,y)
                        width,  # width
                        height,  # height
                        color=list[i][2]
                    )
                )
                self.areas.append([start[0], start[1], start[0] + width, start[1] + height])
                self.write(width, height, start, i, list)
                start[0] = start[0] + width
                widthleft = widthleft - width
            else:
                width = widthleft
                height = (list[i][1] / listsum) * heightleft
                self.ax.add_patch(
                    patches.Rectangle(
                        start,  # (x,y)
                        width,  # width
                        height,  # height
                        color=list[i][2]
                    )
                )
                self.areas.append([start[0], start[1], start[0] + width, start[1] + height])
                self.write(width, height, start, i, list)
                start[1] = start[1] + height
                heightleft = heightleft - height

    def draw(self, aDay='20170304'):
        if self.data is None:
            self.data = json.load(codecs.open('config/textCato/' + aDay + '.json', 'r', 'utf-8-sig'))
        if len(self.ax.collections) > 0:
            self.ax.collections.pop()
        self.ax.texts = []
        if self.topic == -1:
            self.topics = []
            for key, cato in self.data.items():
                Key = key[:-2] + '\n' + key[-2:]
                index = self.label.index(Key)
                color = self.listcolor[index]
                sum = 0
                for text, num in cato.items():
                    sum += num
                self.topics.append([Key, sum,color])
            self.drawrectangle(self.topics)
        else:
            keyword = []
            Key = self.topics[self.topic][0][:-3] + self.topics[self.topic][0][-2:]
            j=0
            for key in self.data[Key].keys():
                keyword.append([key, self.data[Key][key],self.listcolor[j]])
                j+=1
            self.drawrectangle(keyword)
            self.topic = -1

    def onMousePress(self, event):
        if event.xdata is None:
            return
        x = event.xdata
        y = event.ydata
        if self.first is not None:
            self.first = None
            for area in self.areas:
                if (x >= area[0] and x <= area[2]) and (y >= area[1] and y <= area[3]):
                    print('find it!!')
                    self.topic = self.areas.index(area)
                    print(self.topic)
                    break
        else:
            self.first = True
        # for t in self.a:
        #     t.set_visible(False)
        self.draw()
        self.ax.figure.canvas.draw()

    def onMouseMove(self, event):
        if event.xdata is None:
            return
        for t in self.b:
            t.set_visible(False)
        self.b = []
        x = event.xdata
        y = event.ydata
        index = -1
        plt.sca(self.ax)
        for area in self.areas:
            if (x >= area[0] and x <= area[2]) and (y >= area[1] and y <= area[3]):
                index = self.areas.index(area)
                break

        if index in self.annote.keys():
            print('find it!')
            plt.sca(self.ax)
            self.b.append(plt.annotate(self.annote[index], (self.x[index], self.y[index]),
                                       xytext=(self.x[index] + 15, self.y[index]),
                                       arrowprops=dict(facecolor='b', shrink=0.75, alpha=0.6),
                                       verticalalignment='center'))
        self.ax.figure.canvas.draw()


if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.gca()
    bubbleAx = RectTreeAx(ax)
    fig.canvas.mpl_connect('button_press_event', bubbleAx.onMousePress)
    fig.canvas.mpl_connect('motion_notify_event', bubbleAx.onMouseMove)
    # ax = plt.subplots(facecolor="dodgerblue")
    name = '20170307'
    bubbleAx.draw(name)
    plt.show()
