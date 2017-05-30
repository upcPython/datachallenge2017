# from mpl_toolkits.basemap import Basemap
# import matplotlib.pyplot as plt
#
# map = Basemap(llcrnrlon=-93.,llcrnrlat=40.,urcrnrlon=-75.,urcrnrlat=50.,
#              resolution='i', projection='tmerc', lat_0 = 40., lon_0 = -80)
# shp_info=map.readshapefile('d:\mapinfo文件\县界_region',drawbounds=False)
# map.drawmapboundary(fill_color='aqua')
# map.fillcontinents(color='#cc9955', lake_color='aqua')
#
# map.drawcounties()
#
# plt.savefig('i.svg',format='svg')
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from beijing import Beijing
import numpy as np

from matplotlib.patches import Ellipse, Circle, Polygon, FancyArrowPatch
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

map = Beijing(llcrnrlon=115.3,llcrnrlat=39.4,urcrnrlon=117.6,urcrnrlat=41.1,
             resolution='i', projection='tmerc', lat_0 = 39.76, lon_0 = 115.45,
              width=640, height=480)


map.readshapefile('beijingMapinfo\county_region', 'county_region')
x = [116.46198273,115.57,115.58,116.313432,116.445303,116.289501,116.289501]
y = [39.91296005,39.82,39.83,39.970475,39.927248,39.868793,39.868793]
xy = map.projectList(x,y)

polygons = []
for region in map.county_region:
    polygons.append(Polygon(region))

j = 0
for point in xy:
    print(j)
    j+=1
    for i,poly in enumerate(polygons):
        if poly.contains_point(point):
            print('point in region:',i)
            break
parallels = np.arange(0., 81, 2.)
# labels = [left,right,top,bottom]
map.drawparallels(parallels, labels=[False, True, True, False])
meridians = np.arange(10., 351., 5.)
map.drawmeridians(meridians, labels=[True, False, False, True])
# map.fillPolygon(map.county_region[0],color='r',fill_color='aqua')
# x, y = self(lons,lats)
# xy = list(zip(x,y))
# limb = Polygon(xy)
# map.drawmapboundary(color='r',fill_color='aqua')
# map.fillcontinents(color='r',lake_color='aqua')
# map.drawcoastlines()
# print(plt.Figure)
# print(map.county_region[0])
plt.show()
# plt.savefig('end\i_region.svg')
# plt.savefig('end\i_region.svg')