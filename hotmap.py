#updated on 5/30/2017 15:54
from matplotlib.colors import rgb2hex
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Ellipse, Circle, Polygon, FancyArrowPatch
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkinter as tk
import json

def LerpColour(c1,c2,t):
    return (int(c1[0]+(c2[0]-c1[0])*t),int(c1[1]+(c2[1]-c1[1])*t),int(c1[2]+(c2[2]-c1[2])*t))

def gradient(color_list,no_steps = 100):
    colors = []
    for i in range(len(color_list)-1):
        for j in range(no_steps):
            colors.append(LerpColour(color_list[i],color_list[i+1],j/no_steps))
    return colors

def getColor(radio):
    '''0<=radio<=1'''
    list_of_colors = [(254, 240, 217), (253, 204, 138), (252, 141, 89), (227, 74, 51), (179, 0, 0)]
    colors = gradient(list_of_colors)
    return '#%02x%02x%02x' % colors[int((len(colors)-1)*radio)]

class Beijing(Basemap):
    def fillPolygon(self,xy,color = None, fill_color = None, ax=None,zorder=None,alpha=None):
        if self.resolution is None:
            raise AttributeError('there are no boundary datasets associated with this Basemap instance')
        # get current axes instance (if none specified).
        ax = ax or self._check_ax()
        # get axis background color.
        axisbgc = ax.get_axis_bgcolor()
        npoly = 0
        polys = []
        # xa, ya = list(zip(*map.county_region[0]))
        # check to see if all four corners of domain in polygon (if so,
        # don't draw since it will just fill in the whole map).
        # ** turn this off for now since it prevents continents that
        # fill the whole map from being filled **
        # xy = list(zip(xa.tolist(),ya.tolist()))
        if self.coastpolygontypes[npoly] not in [2,4]:
            poly = Polygon(xy,facecolor=color,edgecolor=color,linewidth=0)
        else: # lakes filled with background color by default
            if fill_color is None:
                poly = Polygon(xy,facecolor=axisbgc,edgecolor=axisbgc,linewidth=0)
            else:
                poly = Polygon(xy,facecolor=fill_color,edgecolor=fill_color,linewidth=0)
        if zorder is not None:
            poly.set_zorder(zorder)
        if alpha is not None:
            poly.set_alpha(alpha)
        ax.add_patch(poly)
        polys.append(poly)
        npoly = npoly + 1
        # set axes limits to fit map region.
        self.set_axes_limits(ax=ax)
        # clip continent polygons to map limbs
        polys,c = self._cliplimb(ax,polys)
        return polys

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
    map.readshapefile('beijing\country_region', 'country_region')
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