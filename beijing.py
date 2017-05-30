from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Ellipse, Circle, Polygon, FancyArrowPatch
import matplotlib.pyplot as plt
import json
from gradient import getColor

class Beijing(Basemap):
    def __init__(self, llcrnrlon=None, llcrnrlat=None,
                 urcrnrlon=None, urcrnrlat=None,
                 llcrnrx=None, llcrnry=None,
                 urcrnrx=None, urcrnry=None,
                 width=None, height=None,
                 projection='cyl', resolution='c',
                 area_thresh=None, rsphere=6370997.0,
                 ellps=None, lat_ts=None,
                 lat_1=None, lat_2=None,
                 lat_0=None, lon_0=None,
                 lon_1=None, lon_2=None,
                 o_lon_p=None, o_lat_p=None,
                 k_0=None,
                 no_rot=False,
                 suppress_ticks=True,
                 satellite_height=35786000,
                 boundinglat=None,
                 fix_aspect=True,
                 anchor='C',
                 celestial=False,
                 round=False,
                 epsg=None,
                 ax=None):
        llcrnrlon = 115.3
        llcrnrlat = 39.4
        urcrnrlon = 117.6
        urcrnrlat = 41.1
        resolution = 'i'
        projection = 'tmerc'
        lat_0 = 39.76
        lon_0 = 115.45
        super(Beijing,self).__init__(llcrnrlon, llcrnrlat,
                                     urcrnrlon, urcrnrlat,
                                     llcrnrx, llcrnry,
                                     urcrnrx, urcrnry,
                                     width, height,
                                     projection, resolution,
                                     area_thresh, rsphere,
                                     ellps, lat_ts,
                                     lat_1, lat_2,
                                     lat_0, lon_0,
                                     lon_1, lon_2,
                                     o_lon_p, o_lat_p,
                                     k_0, no_rot,
                                     suppress_ticks,
                                     satellite_height,
                                     boundinglat,
                                     fix_aspect, anchor, celestial,
                                     round, epsg, ax)
        self.readshapefile('beijingMapinfo\county_region', 'county_region')
        with open(r'config\measurements.json') as json_file:
            self.countySum = json.load(json_file)
    def fillPolygon(self,xy, fill_color = None, ax=None,zorder=None,alpha=None):
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

    def countyHotmap(self,ax, aDay='20170304'):
        for key, val in self.countySum[aDay].items():
            if val >= 80000:
                radio = 1
            else:
                radio = val / 80000
            # print(getColor(radio))
            self.fillPolygon(self.county_region[int(key)], fill_color=getColor(radio), ax=ax)
    def project(self,x,y):
        '''
        :param x: longitude
        :param y: latitude
        :return: a tuple with (x,y) with projected coordinate
        '''
        x = [x]
        y = [y]
        xa, ya = self(x, y)
        # print(xa, ya)
        xy = list(zip(xa, ya))
        return xy[0]
    def projectList(self,x,y):
        '''
        :param x: longitude list
        :param y: latitude list
        :return: a list and each element is a tuple with (x,y) with projected coordinate
        '''
        xa, ya = self(x, y)
        # print(xa, ya)
        return list(zip(xa, ya))

if __name__ == "__main__":
    map= Beijing(llcrnrlon=115.3,llcrnrlat=39.4,urcrnrlon=117.6,urcrnrlat=41.1,
             resolution='i', projection='tmerc', lat_0 = 39.76, lon_0 = 115.45)

    map.readshapefile('beijingMapinfo\county_region', 'county_region')
    map.fillPolygon(map.county_region[0],color='r',fill_color='aqua')

    x = [116.46198273, 115.57, 115.58, 116.313432, 116.445303, 116.289501, 116.289501]
    y = [39.91296005, 39.82, 39.83, 39.970475, 39.927248, 39.868793, 39.868793]
    xy = map.projectList(x, y)
    print(xy)

    print(map.project(116.46198273,39.91296005))


    plt.show()