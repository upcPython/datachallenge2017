#updated on 5/30/2017 15:54
from matplotlib.colors import rgb2hex
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Ellipse, Circle, Polygon, FancyArrowPatch
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkinter as tk
import json
from beijing import Beijing

def onmousemove(event):
    #print(' x=%d, y=%d, xdata=%f, ydata=%f' %( event.x, event.y, event.xdata, event.ydata))
    xy = list((event.xdata, event.ydata))
    polygons = []
    for region in map.county_region:
        polygons.append(Polygon(region))

    for i, poly in enumerate(polygons):
        try:
            if poly.contains_point(xy):
                print('point in region:', i)
                break
        except TypeError:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    f = Figure(figsize=(5, 5), dpi=100)
    axes = f.add_subplot(111)
    map = Beijing(ax=axes)
    print(map.llcrnrlat)
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    cid = f.canvas.mpl_connect('motion_notify_event', onmousemove)


    # datelist=[]
    # datelist.extend(list(range(223,229)))
    # datelist.extend(list(range(301,331)))
    # datelist.extend(list(range(401,427)))
    #
    # # for date in datelist:
    # date = datelist[0]
    # day=str(20170000+date)
    day = '20170305'

    map.countyHotmap(axes,day)

    canvas.show()
        # f.savefig(day+'.png')

    toolbar = NavigationToolbar2TkAgg(canvas, root)
    toolbar.update()
    tk.mainloop()