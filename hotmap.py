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
from gradient import getColor

def onclick(event):
    #print(' x=%d, y=%d, xdata=%f, ydata=%f' %( event.x, event.y, event.xdata, event.ydata))
    xy = list((event.xdata, event.ydata))
    polygons = []
    for region in map.country_region:
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
    map = Beijing(llcrnrlon=115.3, llcrnrlat=39.4, urcrnrlon=117.6, urcrnrlat=41.1,
                  resolution='i', projection='tmerc', lat_0=39.76, lon_0=115.45, ax=axes)
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    map.readshapefile('beijingMapinfo\county_region', 'county_region')
    cid = f.canvas.mpl_connect('motion_notify_event', onclick)

    with open(r'frequencydata\measurements.json') as json_file:
        datas = json.load(json_file)

    datelist=[]
    for date in range(223,229):
        datelist.append(date)
    for date in range(301,331):
        datelist.append(date)
    for date in range(401,427):
        datelist.append(date)

    for date in datelist:
        day=str(20170000+date)
        daydatas=datas[day]
        frequencyvalue=sorted(list(daydatas.values()))
        sorteddata=sorted(daydatas.items(),key=lambda item:item[1])
        print(sorteddata)
        listindex=0
        for val in sorteddata:
            if val[1]>=80000:
                radio=1
            else :
                radio = val[1]/80000
            print(getColor(radio))
            map.fillPolygon(map.country_region[int(val[0])], color=getColor(radio), fill_color='aqua', ax=axes)
            listindex += 1
            canvas.show()
            f.savefig(day+'.png')

    toolbar = NavigationToolbar2TkAgg(canvas, root)
    toolbar.update()
    tk.mainloop()