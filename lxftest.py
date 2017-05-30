from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

import tkinter as tk
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


def onclick(event):
    print(' x=%d, y=%d, xdata=%f, ydata=%f' %
          ( event.x, event.y, event.xdata, event.ydata))

root=tk.Tk()

f = Figure(figsize=(10, 5), dpi=100)
axes = f.add_subplot(111)

map = Basemap(llcrnrlon=114.0,llcrnrlat=36.0,urcrnrlon=119.0,urcrnrlat=44.2,
             resolution='i', projection='tmerc', lat_0 = 39.76, lon_0 = 115.45,ax=axes)

#map.drawmapboundary(fill_color='aqua')
#map.fillcontinents(color='r',lake_color='aqua')
map.drawcoastlines()

map.readshapefile('beijing\县界_region', '县界_region')

canvas = FigureCanvasTkAgg(f, master=root)
#canvas.show()
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
cid = f.canvas.mpl_connect('motion_notify_event', onclick)
toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
tk.mainloop()
