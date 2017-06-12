from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
from beijing import Beijing
from math import log


configdir = 'config/'
mapRect=(115.3,39.4,117.6,41.1)
class RegionHotmap:
    def __init__(self, ax):
        self.ax = ax
        self.beijing = Beijing(llcrnrlon=mapRect[0], llcrnrlat=mapRect[1], urcrnrlon=mapRect[2], urcrnrlat=mapRect[3], ax=ax)
        self.controlKey = False
        self.roads = []
        self.readdata()
        self.button=None
        self.selectedregion = 6  #6 means 朝阳区

    def readdata(self):
        with open(configdir+'measurements.json') as json_file:
            self.countySum = json.load(json_file)
        self.region = self.beijing.loadlines('county_region',linewidth=2.5)
        for i in range(1,6):
            road = self.beijing.loadlines('level'+str(i)+'road_polyline',linewidth=1.5,color='#edf8b1',linesalpha=0.2)
            if i>2:
                road.set_visible(False)
            self.roads.append(road)
        self.canvas_width,self.canvas_height = self.ax.dataLim.max
        listcolor = ['r', 'orange', 'yellow', '#40fd14', '#fa5ff7', '#ffd1df',
                     '#fe7b7c']
        # self.topic0 = self.beijing.loadlines('one_load',curdir='config/regionTopic',linewidth=1.5,color='r',linesalpha=0.9)
        for i in range(7):
            self.beijing.loadlines('topic_'+str(i),curdir='config/regionTopic',linewidth=1.5,color=listcolor[i],linesalpha=0.9)

    def onMousePressed(self,event):
        if event.inaxes == None:
            print("none")
            return
        if event.button == 1:  # left button
            # if event.dblclick:
            #     self.ax.set_xlim(0, self.canvas_width)
            #     self.ax.set_ylim(0, self.canvas_height)
            #     self.beijing.level = 1
            # else:
            #     self.onLeftClick(event)
            self.onLeftClick(event)
        # elif event.button == 3:  # right button
        #     self.onRightClick(event)

    def countyHotmap(self, aDay='20170304'):
        values = []
        adict = {}
        for key,value in self.countySum[aDay].items():
            adict[int(key)] = value
        for key in sorted(adict.keys()):
            if adict[key]==0:
                val = 0
            else:
                val = log(adict[key])
            if val >= log(80000):
                radio = 1
            else:
                radio = val / log(80000)
            values.append(radio)
        values = np.array(values)
        cmap = plt.cm.Blues
        errorbar_colors = cmap(values)
        self.region.set_facecolors(errorbar_colors)



        # cb.set_ticks(np.linspace(0,8,9))
        # cb.set_ticklabels(('0','1','2','3','4','5','6','7','8'))

    def draw(self,day):
        self.countyHotmap(day)

    def moveMapCenter(self,x, y):
        for i in range(3,6):
            self.roads[i-1].set_visible(i<=self.beijing.level+1)
        width = self.canvas_width / (2 ** self.beijing.level)
        height = self.canvas_height / (2 ** self.beijing.level)
        self.ax.set_xlim(x - width, x + width)
        self.ax.set_ylim(y - height, y + height)

    def onLeftClick(self,event):
        # print(event.xdata,event.ydata)
        region = -1
        for index,aPath in enumerate(self.region.get_paths()):
            if aPath.contains_point((event.xdata,event.ydata)):
                region = index
        if region in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,17,19,20]:#rational region
            self.selectedregion = region
        if self.button=='enlargebutton':
            # print('enlargebutton')
            if self.beijing.level < 4:
                self.beijing.level += 1
            self.moveMapCenter(event.xdata, event.ydata)
        elif self.button=='shrinkbutton':
            # print('shrinkbtton')
            if self.beijing.level > 1:
                self.beijing.level -= 1
            self.moveMapCenter(event.xdata, event.ydata)
        # elif self.button=='translationbutton':
        #     self.moveMapCenter(event.xdata, event.ydata)
    # def onRightClick(self,event):
    #     # print(event.xdata,event.ydata)
    #     if self.beijing.level > 1:
    #         self.beijing.level -= 1
    #     self.moveMapCenter(event.xdata, event.ydata)


    def onWheel(self,event):
        if self.button=='translationbutton':
            if self.controlKey:
                left, right = self.ax.get_xlim()
                width = (right - left) / 16 * event.step
                left += width
                right += width
                self.ax.set_xlim(left, right)
            else:
                top, bottom = self.ax.get_ylim()
                height = (bottom - top) / 16 * event.step
                top += height
                bottom += height
                self.ax.set_ylim(top, bottom)
                # canvas.show()
                # if event.step > 0:
                #     print(event.step)
                # else:
                #     print(event.step)
                # 滚轮往下滚动，缩小

    def onKeyPress(self,event):
        global controlKey
        if event.key == 'control':
            self.controlKey = True

    def onKeyRelease(self,event):
        if event.key == 'control':
            self.controlKey = False
        # print(type(event.inaxes))
        # print(event.xdata,event.ydata)

    def on_homebutton_clicked(self,event):
        self.ax.set_xlim(0, self.canvas_width)
        self.ax.set_ylim(0, self.canvas_height)
        self.beijing.level = 1
        for i in range(3,6):
            self.roads[i-1].set_visible(i<=self.beijing.level+1)
        self.ax.figure.canvas.draw()

    def on_enlargebutton_clicked(self,event):
        self.button='enlargebutton'

    def on_shrinkbutton_clicked(self,event):
        self.button='shrinkbutton'

    def on_translationbutton_clicked(self,event):
        self.button='translationbutton'
if __name__ == "__main__":
    # t1 = np.arange(0, 5, 0.1)
    # t2 = np.arange(0, 5, 0.02)
    #
    # aa = plt.figure(13)
    # bb = plt.subplot(221)
    # plt.plot(t1, f(t1), 'bo', t2, f(t2), 'r--')
    #
    # cc = plt.subplot(222)
    # plt.plot(t2, np.cos(2 * np.pi * t2), 'r--')
    #
    # plt.subplot(212)
    # plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    #
    # plt.show()
    # exit()
    # f = Figure(figsize=(10, 7), dpi=10)
    f = plt.figure(figsize=(50, 35), dpi=20)
    f.subplots_adjust(left=0.0, right=1, top=1, bottom=0.0)
    ax1 = f.add_subplot(221)
    ax1.name = 'left'
    dateAx1 = RegionHotmap(ax1)
    # print(f.canvas)
    # canvas = FigureCanvasTkAgg(f)
    # f.canvas.mpl_connect('button_press_event',dateAx1.onKeyPressed)
    # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    data = np.random.randn(7*10)
    data = data.reshape((10,7))
    dateAx1.readdata()
    plt.show()