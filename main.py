from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import rcParams
from dateAx import DateAx
import numpy as np

plt.rcParams['savefig.facecolor'] = "0.8"

def example_plot(ax, fontsize=12):
     ax.plot([1, 2],'wx--')
     ax.locator_params(nbins=3)
     ax.set_xlabel('x-label', fontsize=fontsize)
     ax.set_ylabel('y-label', fontsize=fontsize)
     # ax.set_title('Title', fontsize=fontsize)
     # ax.axis('off')

if __name__ == "__main__":
    rcParams['font.sans-serif'] = ['SimHei']
    rcParams['font.family'] = 'sans-serif'
    plt.close('all')
    fig = plt.figure()
    fig.set_facecolor('b')

    rect = 0, 0.9, 1, 0.1
    axtitle = fig.add_axes(rect)
    axtitle.name = 'title'
    axtitle.patch.set_facecolor('b')
    axtitle.axis('off')
    print(axtitle)
    # w,h = axtitle.dataLim.max
    # print(w,h)
    axtitle.text(0.5,0.97,'垃圾短信数据分析系统', fontsize=24,horizontalalignment='center',verticalalignment='bottom')
    # axtitle.set_title('垃圾短信数据分析系统')
    example_plot(axtitle)

    rect = 0.3, 0.3, 0.4, 0.6
    axmap = fig.add_axes(rect)
    axmap.name = 'map'
    axmap.patch.set_facecolor('b')
    axmap.axis('off')
    # axmap.text(0.5,0.5,'垃圾短信数据分析系统', fontsize=24,horizontalalignment='center',verticalalignment='center')
    example_plot(axmap)

    gs0 = gridspec.GridSpec(1, 2)
    ax1 = fig.add_subplot(gs0[0])
    ax2 = fig.add_subplot(gs0[1])

    example_plot(ax1)
    example_plot(ax2)

    gs0.tight_layout(fig, rect=[0.3, 0, 0.7, 0.3])
    # ax1 = fig.add_subplot(gstitle[0])
    # gstitle.tight_layout(fig, rect=[0, 0.2, 1, 0.1])
    gs1 = gridspec.GridSpec(2, 1)
    ax1 = fig.add_subplot(gs1[0])
    ax1.axis('off')
    ax2 = fig.add_subplot(gs1[1])
    ax2.axis('off')
    dateAx1 = DateAx(ax1)
    data = np.random.randn(7*10)
    data = data.reshape((10,7))
    dateAx1.readdata(data)

    # example_plot(ax1)
    example_plot(ax2)

    gs1.tight_layout(fig, rect=[0, 0, 0.3, 0.9])
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