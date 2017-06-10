from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import json


class DateAx:
    def __init__(self, ax,defaultday='20170304'):
        self.ax = ax
        self.day = defaultday
        self.xdata=6
        self.ydata=8
        self.days=[['20170219','20170220','20170221','20170222','20170223','20170224','20170225'],
      ['20170226','20170227','20170228','20170301','20170302','20170303','20170304'],
      ['20170305','20170306','20170307','20170308','20170309','20170310','20170311'],
      ['20170312','20170313','20170314','20170315','20170316','20170317','20170318'],
      ['20170319','20170320','20170321','20170322','20170323','20170324','20170325'],
      ['20170326','20170327','20170328','20170329','20170330','20170331','20170401'],
      ['20170402','20170403','20170404','20170405','20170406','20170407','20170408'],
      ['20170409','20170410','20170411','20170412','20170413','20170414','20170415'],
      ['20170416','20170417','20170418','20170419','20170420','20170421','20170422'],
      ['20170423','20170424','20170425','20170426','20170427','20170428','20170429']]
        self.readdata()
        plt.sca(self.ax)
        self.CutDay=plt.plot([6,6,7,7,6], [9,8,8,9,9], color='r', linewidth=1.5)

    def dateColor(self):
        with open(r'config\number.json') as json_file:
            daydata = json.load(json_file)
            daydata = sorted(daydata.items(), key=lambda abs: abs[0], reverse=1)
            val = []
            for i in range(len(daydata)):
                if daydata[i][1] >= 80000:
                    radio = 1
                    val.append(radio)
                else:
                    radio = daydata[i][1] / 80000
                    val.append(radio)
            data = []
            count = 0
            list = [0]
            for i in range(6):
                if i < 4:
                    list.insert(0, val[count])
                    count += 1
                else:
                    list.append(0)
            data.append(list)
            for i in range(8):
                list = []
                for j in range(7):
                    list.insert(0, val[count])
                    count += 1
                data.append(list)
            list = []
            for i in range(7):
                if i < 3:
                    list.insert(0, val[count])
                    count += 1
                else:
                    list.insert(0, 0)
            data.append(list)
        return data
    def readdata(self):
        data = self.dateColor()
        plt.sca(self.ax)
        plt.pcolor(data, cmap=plt.cm.Blues)
        for i in range(10):
            for j in range(7):
                self.ax.text(j+0.5,9-i+0.5,str(int(self.days[i][j][-2:])),color='k',alpha=0.8,fontsize=18,horizontalalignment='center',
                     verticalalignment='center')
        plt.plot([0, 3, 3, 7], [8, 8, 9, 9], color='y', linewidth=2)
        plt.plot([0, 6, 6, 7], [3, 3, 4, 4], color='y', linewidth=2)

        self.ax.text(3.5, 5.5, '三月', color='y', alpha=0.4, fontsize=40, horizontalalignment='center',
                     verticalalignment='center')
        self.ax.text(3.5, 1.5, '四月', color='y', alpha=0.4, fontsize=40, horizontalalignment='center',
                     verticalalignment='center')

    def onMousePressed(self,event):
        if event.inaxes is not None:
            print(event.inaxes.name)
        #self.day = '20170307'
        restday = ['20170220', '20170221', '20170222', '20170427', '20170428', '20170429', '20170219']
        rday = self.days[9 - int(event.ydata)][int(event.xdata)]
        if rday not in restday:
            self.day = rday
            plt.sca(self.ax)
            self.ax.lines.remove(self.CutDay[0])
            xdata=int(event.xdata)
            ydata=int(event.ydata)
            self.CutDay = plt.plot([xdata, xdata, xdata + 1, xdata + 1, xdata],
                                   [ydata + 1, ydata, ydata, ydata + 1, ydata + 1], color='r',
                               linewidth=1.5)


        # print(type(event.inaxes))
        # print(event.xdata,event.ydata)
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
    ax2 = f.add_subplot(222)
    ax2.name = 'right'
    dateAx1 = DateAx(ax1)
    dateAx2 = DateAx(ax2)
    # print(f.canvas)
    # canvas = FigureCanvasTkAgg(f)
    # f.canvas.mpl_connect('button_press_event',dateAx1.onKeyPressed)
    # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    data = np.random.randn(7*10)
    data = data.reshape((10,7))
    dateAx1.readdata(data)
    dateAx2.readdata(data)
    plt.show()
