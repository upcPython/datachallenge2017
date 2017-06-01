from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkinter as tk
from matplotlib import rcParams
from beijing import Beijing
from dateCtrl import DateCtrl

def onClick(dt = '20170304'):
    map.countyHotmap(axes, dt)
    canvas.show()

configdir = 'config/'
if __name__ == '__main__':
    rcParams['font.sans-serif'] = ['SimHei']
    rcParams['font.family'] = 'sans-serif'
    root = tk.Tk()
    frame = tk.Frame(master=root)

    frame1 = Frame(frame)
    frame1.pack()
    f = Figure(figsize=(8, 8), dpi=100)
    axes = f.add_subplot(111)
    map = Beijing(llcrnrlon = 115.3, llcrnrlat = 39.4, urcrnrlon = 117.6, urcrnrlat = 41.1, ax=axes)
    import pandas as pd
    file = configdir+'mapcolors.csv'
    csv=pd.read_csv(file)
    map.readshapefile('beijingMapinfo/level3road_polyline', 'level3road_polyline', color='#2c7fb8',
                      linewidth=1.5)
    map.readshapefile('beijingMapinfo/level2road_polyline', 'level2road_polyline', color='#7fcdbb',
                      linewidth=1.5)
    map.readshapefile('beijingMapinfo/level1road_polyline', 'level1road_polyline', color='#edf8b1',
                      linewidth=1.5)
    # map.readshapefile('beijingMapinfo/level3road_polyline', 'level3road_polyline', color='#F9F6AB',
    #                   linewidth=1.5)
    # map.readshapefile('beijingMapinfo/level2road_polyline', 'level2road_polyline', color='#F4C03E',
    #                   linewidth=1.5)
    # map.readshapefile('beijingMapinfo/level1road_polyline', 'level1road_polyline', color='#F4C03E',
    #                   linewidth=1.5)
    map.readshapefileext('beijingMapinfo/county_region', 'county_region', color='#808080', linestyle='--')
    map.pointmarked()
    canvas = FigureCanvasTkAgg(f, master=frame1)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    # cid = f.canvas.mpl_connect('motion_notify_event', onmousemove)

    toolbar = NavigationToolbar2TkAgg(canvas, frame1)
    toolbar.update()

    frame.grid(row=0, rowspan=20)

    mainfram = DateCtrl(root,onClick,'20170304')
    # tdt =datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
    # mainfram.SetDate(tdt.replace(day=30))  # 试试重置日期

    root.mainloop()