from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkinter as tk
from matplotlib import rcParams
from beijing import Beijing
import numpy as np
import matplotlib.pyplot as plt
from dateCtrl import DateCtrl
import json
import codecs

def onClick(dt = '20170304'):
    beijing.countyHotmap(region, dt)
    # axes.draw()
    canvas.show()

def closeWindow():
    root.quit()

def moveMapCenter(x,y):
    width = canvas_width/(2**beijing.level)
    height = canvas_height/(2**beijing.level)
    axes.set_xlim(x- width , x+ width)
    axes.set_ylim(y- height, y+ height)
    canvas.draw()

def onLeftClick(event):
    # print(event.xdata,event.ydata)
    if beijing.level<4:
        beijing.level += 1
    moveMapCenter(event.xdata,event.ydata)

def onRightClick(event):
    # print(event.xdata,event.ydata)
    if beijing.level>1:
        beijing.level -= 1
    moveMapCenter(event.xdata,event.ydata)

controlKey = False
def onWheel(event):
    global controlKey
    if controlKey:
        left, right = axes.get_xlim()
        width = (right - left) / 16 * event.step
        left += width
        right += width
        axes.set_xlim(left, right)
    else:
        top,bottom = axes.get_ylim()
        height =(bottom-top)/16*event.step
        top+= height
        bottom+=height
        axes.set_ylim(top,bottom)
    canvas.draw()
    # canvas.show()
    # if event.step > 0:
    #     print(event.step)
    # else:
    #     print(event.step)
            # 滚轮往下滚动，缩小
def onMouse(event):
    if event.inaxes == None:
        print("none")
        return
    if event.button==1:#left button
        onLeftClick(event)
    elif event.button==3:#right button
        onRightClick(event)
    # print(event.button)
def onKeyPress(event):
    global controlKey
    if event.key == 'control':
        controlKey = True
def onKeyRelease(event):
    global controlKey
    if event.key == 'control':
        controlKey = False

configdir = 'config/'
if __name__ == '__main__':
    rcParams['font.sans-serif'] = ['SimHei']
    rcParams['font.family'] = 'sans-serif'
    root = tk.Tk()
    root.protocol('WM_DELETE_WINDOW', closeWindow)

    frame = tk.Frame(master=root)

    frame1 = Frame(frame)
    frame1.pack()
    f = Figure(figsize=(512, 512), dpi=1)
    # f = plt.figure(figsize=(512, 512), dpi=1)
    f.subplots_adjust(left=0.0, right=1, top=1, bottom=0.0)

    axes = f.add_subplot(111)
    # a= plt.cm.Blues
    axes.patch.set_facecolor('#0000ff')
    # left,right = axes.get_xlim()
    # print(left,right)
    # axes.set_xlim(left,right*2)
    axes.plot()
    # left,right = axes.get_xlim()
    # print(left,right)


    beijing = Beijing(llcrnrlon = 115.3, llcrnrlat = 39.4, urcrnrlon = 117.6, urcrnrlat = 41.1, ax=axes)
    import pandas as pd
    file = configdir+'mapcolors.csv'
    csv=pd.read_csv(file)
    # road3 = beijing.loadlines('level3road_polyline',linewidth=3.5)
    # road2 = beijing.loadlines('level2road_polyline',linewidth=3.5)
    # road1 = beijing.loadlines('level1road_polyline',linewidth=3.5)
    region = beijing.loadlines('county_region',linewidth=5)


    # region.set_facecolor('None')
    # road3.set_visible(False)
    # road2.set_visible(False)
    # verts = beijing.readmapinfo('beijingMapinfo/level3road_polyline', 'lever3')
    # beijing.saveCoords('beijingJson/level3road_polyline.json',verts)
    # verts = beijing.readmapinfo('beijingMapinfo/level2road_polyline', 'level2')
    # beijing.saveCoords('beijingJson/level2road_polyline.json',verts)
    # verts = beijing.readmapinfo('beijingMapinfo/level1road_polyline', 'level1')
    # beijing.saveCoords('beijingJson/level1road_polyline.json',verts)
    # beijing.readshapefile('beijingMapinfo/level3road_polyline', 'level3road_polyline', color='#2c7fb8',
    #                   linewidth=1.5)
    # beijing.readshapefile('beijingMapinfo/level2road_polyline', 'level2road_polyline', color='#7fcdbb',
    #                   linewidth=1.5)
    # beijing.readshapefile('beijingMapinfo/level1road_polyline', 'level1road_polyline', color='#edf8b1',
    #                       linewidth=1.5)
    # map.readshapefile('beijingMapinfo/level3road_polyline', 'level3road_polyline', color='#F9F6AB',
    #                   linewidth=1.5)
    # map.readshapefile('beijingMapinfo/level2road_polyline', 'level2road_polyline', color='#F4C03E',
    #                   linewidth=1.5)
    # map.readshapefile('beijingMapinfo/level1road_polyline', 'level1road_polyline', color='#F4C03E',
    #                   linewidth=1.5)
    # left,right = axes.get_xlim()
    # top,bottom = axes.get_ylim()
    # canvas_width = right-left
    # canvas_height = bottom-top
    # print(left,right,top,bottom)
    # axes.set_xlim(right/2,right*2)
    # axes.set_ylim(bottom+right*2-right/2,bottom)
    # f.subplots_adjust(left=0.0, right=1, top=1, bottom=0.0)
    # f.set_figwidth(8)
    beijing.pointmarked()
    # cid = f.canvas.mpl_connect('motion_notify_event', onmousemove)

    canvas_width,canvas_height = axes.dataLim.max
    canvas = FigureCanvasTkAgg(f, master=frame1)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.mpl_connect('key_press_event',onKeyPress)
    canvas.mpl_connect('key_release_event',onKeyRelease)
    canvas.mpl_connect('button_press_event',onMouse)
    canvas.mpl_connect("scroll_event", onWheel)
    # verts = beijing.readmapinfo('beijingMapinfo/county_region', 'county_region')
    # beijing.saveCoords('beijingJson/county_region.json',verts)
    # verts = json.load(codecs.open('result.json','r','utf-8-sig'))
    # beijing.readshapefileext('beijingMapinfo/county_region', 'county_region', color='#ff8080', linestyle='--',ax=axes)
    mainfram = DateCtrl(root,onClick,'20170304')
    # toolbar = NavigationToolbar2TkAgg(canvas, frame1)
    # toolbar.update()

    frame.grid(row=0, rowspan=20)

    # tdt =datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
    # mainfram.SetDate(tdt.replace(day=30))  # 试试重置日期

    root.mainloop()