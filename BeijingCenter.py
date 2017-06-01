import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rcParams
from beijing import Beijing

if __name__ == "__main__":
    rcParams['font.sans-serif'] = ['SimHei']
    rcParams['font.family'] = 'sans-serif'
    #the map of Beijing Center
    plt.figure(0)
    map= Beijing(llcrnrlon=116.03,llcrnrlat=39.76,urcrnrlon=116.651419,urcrnrlat=40.17)
    map.readshapefile('beijingMapinfo/level3road_polyline', 'level3road_polyline', color='#F9F6AB',
                      linewidth=1.5)
    map.readshapefile('beijingMapinfo/level2road_polyline', 'level2road_polyline', color='#F4C03E',
                      linewidth=1.5)
    map.readshapefile('beijingMapinfo/level1road_polyline', 'level1road_polyline', color='#F4C03E',
                      linewidth=1.5)
    map.readshapefileext('beijingMapinfo/chaoyang_region', 'chaoyang_region', color='#808080', linestyle='--')
    map.pointmarked()

    #the map of Chaoyang district
    plt.figure(1)
    map= Beijing(llcrnrlon=116.304512,llcrnrlat=39.793666,urcrnrlon=116.651419,urcrnrlat=40.139684)
    map.readshapefile('beijingMapinfo/level6road_polyline', 'level6road_polyline', color='#ACACAC',
                      linewidth=0.5)
    map.readshapefile('beijingMapinfo/level4road_polyline', 'level4road_polyline', color='#FFECBF',
                      linewidth=0.8)
    map.readshapefile('beijingMapinfo/level3road_polyline', 'level3road_polyline', color='#F9F6AB',
                      linewidth=1.5)
    map.readshapefile('beijingMapinfo/level2road_polyline', 'level2road_polyline', color='#F4C03E',
                      linewidth=1.5)
    map.readshapefile('beijingMapinfo/level1road_polyline', 'level1road_polyline', color='#F4C03E',
                      linewidth=1.5)
    map.readshapefileext('beijingMapinfo/chaoyang_region', 'chaoyang_region',color='#808080',linestyle='--')
    x,y=map(116.467471, 39.920593)
    plt.text(x,y, '朝阳区',size=12)
    x,y=map(116.596774, 40.065848)
    plt.text(x,y, '朝阳区')
    plt.show()