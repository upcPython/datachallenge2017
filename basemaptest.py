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

map = Basemap(llcrnrlon=114.0,llcrnrlat=36.0,urcrnrlon=119.0,urcrnrlat=44.2,
             resolution='i', projection='tmerc', lat_0 = 39.76, lon_0 = 115.45)

# map.drawmapboundary(fill_color='aqua')
# map.fillcontinents(color='r',lake_color='aqua')
# map.drawcoastlines()


map.readshapefile('beijing\mapinfo\省界_region', '省界_region')

plt.show()
# plt.savefig('end\i_region.svg')