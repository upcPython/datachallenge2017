from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import rcParams
from dateAx import DateAx
import matplotlib as mpl
import cv2
import numpy as np
from matplotlib.widgets import Button
from regionHotmap import RegionHotmap
from themeRiver import ThemeRiver
from radar import RadarAx,radar_factory
from roadCloud import RoadCloud

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
        riverCtrl.draw(dateCtrl.day)
        radarCtrl.draw(dateCtrl.day)
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


    fig = plt.figure(facecolor='#00BFFF')
    fig.subplots_adjust(left=0.0, right=1, top=1, bottom=0.0)
    fig.canvas.mpl_connect('button_press_event',onMousePress)
    fig.canvas.mpl_connect('key_press_event',onKeyPress)
    fig.canvas.mpl_connect('key_release_event',onKeyRelease)
    fig.canvas.mpl_connect("scroll_event", onWheel)

    rect = 0, 0.9, 1, 0.1
    axtitle = fig.add_axes(rect)
    axtitle.name = 'title'
    axtitle.patch.set_facecolor('#00BFFF')
    axtitle.axis('off')
    print(axtitle)
    # w,h = axtitle.dataLim.max
    # print(w,h)
    axtitle.text(0.5,0.5,'垃圾短信数据分析系统', color = 'w', fontsize=40,horizontalalignment='center',verticalalignment='center')

    gs2 = gridspec.GridSpec(3, 1)

    axr1 = fig.add_subplot(gs2[2])
    example_plot(axr1)
    axr1.set_title("")
    axr1.set_xlabel("")

    axcloud = fig.add_subplot(gs2[1])
    axcloud.name = 'road'
    axcloud.axis('off')
    cloudCtrl = RoadCloud(axcloud)
    cloudCtrl.draw()

    axdate = fig.add_subplot(gs2[0])
    axdate.name = 'date'
    axdate.axis('off')
    dateCtrl = DateAx(axdate)
    gs2.tight_layout(fig, rect=[0.7, 0, 1, 0.9])

    gs1 = gridspec.GridSpec(2, 1)
    axriver = fig.add_subplot(gs1[0])
    axriver.name = 'river'
    axriver.patch.set_facecolor('#00BFFF')
    riverCtrl = ThemeRiver(axriver)
    # axriver.axis('off')
    riverCtrl.draw(dateCtrl.day)
    # axtitle.set_title('垃圾短信数据分析系统')
    # example_plot(axtitle)

    theta = radar_factory(11, frame='polygon')
    kw = {'projection': 'radar'}
    axradar = fig.add_subplot(gs1[1],**kw)
    axradar.name = 'radar'
    # ax2.axis('off')
    radarCtrl=RadarAx(axradar,theta)
    gs1.tight_layout(fig, rect=[0, 0, 0.3, 0.9])



    rect = 0.3, 0.3, 0.4, 0.6
    axmap = fig.add_axes(rect)
    axmap.name = 'map'
    axmap.patch.set_facecolor('#00BFFF')
    axmap.axis('off')
    regionMap = RegionHotmap(axmap)
    regionMap.draw(dateCtrl.day)
    ax_colorbar = fig.add_axes([0.67, 0.354, 0.011, 0.53])
    norm = mpl.colors.Normalize(vmin=0, vmax=8)
    cmap = plt.cm.Blues
    cb = mpl.colorbar.ColorbarBase(ax_colorbar, cmap=cmap,
                                   norm=norm,
                                   orientation='vertical')
    cb.set_label('（万）', fontdict={'size': 15})

    homeimg = cv2.imread('image\home.png')
    enlargeimg = cv2.imread('image\enlarge.png')
    shrinkimg = cv2.imread('image\shrink.png')
    translationimg = cv2.imread('image/translation.png')
    homeset = plt.axes([0.31, 0.81, 0.035, 0.035])
    enlargeset = plt.axes([0.31, 0.76, 0.035, 0.035])
    shrinkset = plt.axes([0.31, 0.71, 0.035, 0.035])
    translationset = plt.axes([0.31, 0.66, 0.035, 0.035])
    home = Button(homeset, '', homeimg, hovercolor='0.2')
    enlarge = Button(enlargeset, '', enlargeimg)
    shrink = Button(shrinkset, '', shrinkimg)
    translation = Button(translationset, '', translationimg)
    home.on_clicked(regionMap.on_homebutton_clicked)
    enlarge.on_clicked(regionMap.on_enlargebutton_clicked)
    shrink.on_clicked(regionMap.on_shrinkbutton_clicked)
    translation.on_clicked(regionMap.on_translationbutton_clicked)


    gs0 = gridspec.GridSpec(1, 2)
    axdate = fig.add_subplot(gs0[0])
    ax2 = fig.add_subplot(gs0[1])

    example_plot(axdate)
    example_plot(ax2)

    gs0.tight_layout(fig, rect=[0.3, 0, 0.7, 0.3])
    # ax1 = fig.add_subplot(gstitle[0])
    # gstitle.tight_layout(fig, rect=[0, 0.2, 1, 0.1])

    # example_plot(axr3)
    # axr3.set_title("")
    # axr3.set_xlabel("")
    # ax.set_xlabel("x-label", fontsize=12)

    # gs2.tight_layout(fig, rect=[0.7, 0, 0.3, 0.9], h_pad=0.5)
    plt.show()