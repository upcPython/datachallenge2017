from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import rcParams
from dateAx import DateAx
import matplotlib as mpl
import numpy as np
from regionHotmap import RegionHotmap

plt.rcParams['savefig.facecolor'] = "0.8"

def example_plot(ax, fontsize=12):
     ax.plot([1, 2],'wx--')
     ax.locator_params(nbins=3)
     ax.set_xlabel('x-label', fontsize=fontsize)
     ax.set_ylabel('y-label', fontsize=fontsize)
     # ax.set_title('Title', fontsize=fontsize)
     # ax.axis('off')
def onMousePress(event):
    if event.inaxes is None:
        return
    if event.inaxes.name=='date':#date control
        dateCtrl.onMousePressed(event)
        regionMap.draw(dateCtrl.day)
        # print(event.xdata,event.ydata)
    if event.inaxes.name=='map':#map control
        regionMap.onMousePressed(event)
    fig.canvas.draw()

def onKeyPress(event):
    if event.inaxes is None:
        return
    if event.inaxes.name=='map':#map control
        regionMap.onKeyPress(event)

def onKeyRelease(event):
    if event.inaxes is None:
        return
    if event.inaxes.name=='map':#map control
        regionMap.onKeyRelease(event)
def onWheel(event):
    if event.inaxes is None:
        return
    if event.inaxes.name=='map':#map control
        regionMap.onWheel(event)
    fig.canvas.draw()
if __name__ == "__main__":
    rcParams['font.sans-serif'] = ['SimHei']
    rcParams['font.family'] = 'sans-serif'
    plt.close('all')


    fig = plt.figure()
    fig.subplots_adjust(left=0.0, right=1, top=1, bottom=0.0)
    fig.set_facecolor('b')
    fig.canvas.mpl_connect('button_press_event',onMousePress)
    fig.canvas.mpl_connect('key_press_event',onKeyPress)
    fig.canvas.mpl_connect('key_release_event',onKeyRelease)
    fig.canvas.mpl_connect("scroll_event", onWheel)

    rect = 0, 0.9, 1, 0.1
    axtitle = fig.add_axes(rect)
    axtitle.name = 'title'
    axtitle.patch.set_facecolor('b')
    axtitle.axis('off')
    print(axtitle)
    # w,h = axtitle.dataLim.max
    # print(w,h)
    axtitle.text(0.5,0.5,'垃圾短信数据分析系统', color = 'w', fontsize=40,horizontalalignment='center',verticalalignment='center')

    # axtitle.set_title('垃圾短信数据分析系统')
    # example_plot(axtitle)
    gs1 = gridspec.GridSpec(2, 1)
    axdate = fig.add_subplot(gs1[0])
    axdate.name = 'date'
    # axdate.axis('off')
    ax2 = fig.add_subplot(gs1[1])
    ax2.axis('off')
    dateCtrl = DateAx(axdate)
    # data = np.random.randn(7 * 10)
    # data = data.reshape((10, 7))
    # dateCtrl.readdata(data)

    # example_plot(ax1)
    example_plot(ax2)

    gs1.tight_layout(fig, rect=[0, 0, 0.3, 0.9])

    rect = 0.3, 0.3, 0.4, 0.6
    axmap = fig.add_axes(rect)
    axmap.name = 'map'
    axmap.patch.set_facecolor('b')
    axmap.axis('off')
    regionMap = RegionHotmap(axmap)
    regionMap.draw(dateCtrl.day)
    ax_colorbar = fig.add_axes([0.65, 0.354, 0.012, 0.49])
    norm = mpl.colors.Normalize(vmin=0, vmax=8)
    cmap = plt.cm.Blues
    cb = mpl.colorbar.ColorbarBase(ax_colorbar, cmap=cmap,
                                   norm=norm,
                                   orientation='vertical')
    cb.set_label('（万）', fontdict={'size': 15})

    gs0 = gridspec.GridSpec(1, 2)
    axdate = fig.add_subplot(gs0[0])
    ax2 = fig.add_subplot(gs0[1])

    example_plot(axdate)
    example_plot(ax2)

    gs0.tight_layout(fig, rect=[0.3, 0, 0.7, 0.3])
    # ax1 = fig.add_subplot(gstitle[0])
    # gstitle.tight_layout(fig, rect=[0, 0.2, 1, 0.1])
    gs2 = gridspec.GridSpec(3, 1)

    for ss in gs2:
        ax = fig.add_subplot(ss)
        example_plot(ax)
        ax.set_title("")
        ax.set_xlabel("")

    # ax.set_xlabel("x-label", fontsize=12)

    gs2.tight_layout(fig, rect=[0.7, 0, 1, 0.9])
    # gs2.tight_layout(fig, rect=[0.7, 0, 0.3, 0.9], h_pad=0.5)
    plt.show()