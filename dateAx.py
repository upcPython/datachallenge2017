from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


class DateAx:
    def __init__(self, ax):
        self.ax = ax

    def readdata(self,data):
        plt.sca(self.ax)
        plt.pcolor(data, cmap=plt.cm.Blues)

    def onKeyPressed(self,event):
        if event.inaxes is not None:
            print(event.inaxes.name)
        print(event.inaxes)
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
    f.canvas.mpl_connect('button_press_event',dateAx1.onKeyPressed)
    # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    data = np.random.randn(7*10)
    data = data.reshape((10,7))
    dateAx1.readdata(data)
    dateAx2.readdata(data)
    plt.show()
