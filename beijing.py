from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Ellipse, Circle, Polygon, FancyArrowPatch
import matplotlib.pyplot as plt

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
    plt.show()