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
from beijing import Beijing
import pandas as pd
import os
from matplotlib.patches import Ellipse, Circle, Polygon, FancyArrowPatch
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import json

'''进行市区的划分，将经纬度转换成投影坐标然后进行市区的划分，形成一个json文件以及对应的图表'''
def store(measurements):
    with open('measurements.json', 'w') as f:
        f.write(json.dumps(measurements))

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.03*height, '%d' % float(height))

map = Beijing(llcrnrlon=115.3,llcrnrlat=39.4,urcrnrlon=117.6,urcrnrlat=41.1,
             resolution='i', projection='tmerc', lat_0 = 39.76, lon_0 = 115.45)
map.readshapefile('beijingMap/beijingMapinfo/county_region', 'county_region')


if __name__=="__main__":
    datas = {}
    filenames = os.listdir("newCsv/")
    for filename in filenames:
        data ={}
        dicts = {}
        for i in range(21):
            dicts[i] = 0
        listx = []
        listy = []
        df = pd.read_csv('newCsv/'+filename,encoding='utf-8')
        for i in range(len(df['lng'])):
            listx.append(df['lng'][i])
            listy.append(df['lat'][i])
        xa, ya = map(listx, listy)
        #print(xa, ya)
        xy = list(zip(xa, ya))
        polygons = []
        for region in map.county_region:
            polygons.append(Polygon(region))

        for point in xy:
            for i, poly in enumerate(polygons):
                if poly.contains_point(point):
                    #print('point in region:', i)
                    dicts[i]+=1
                    break
        print(dicts.keys(),dicts.values())
        #plt.show()
        plt.close()

        '''plt.title(filename[0:8]+'  point in region')
        rcents = plt.bar(range(len(dicts.values())), dicts.values(), tick_label=range(len(dicts.keys())),color = 'b')
        autolabel(rcents)
        fig = plt.gcf()
        fig.set_size_inches(20, 10.5)
        plt.savefig('point in region/photo/' + filename[0:8] + '.png', dpi=100)
        plt.close()'''
        data[filename[0:8]]=dicts
        datas[filename[0:8]]=dicts
        json.dump(data,open('point in region/number/'+filename[0:8]+'.json', 'w'))
        print(filename+'  over!!!')
        '''with open('point in region/number/'+filename[0:8]+'.json', 'w') as f:
            jsonStr = json.dump(data,f)
            print(jsonStr)
            f.write(jsonStr)'''
    #jsonStr = json.dumps(data)
    #store(jsonStr)
    json.dump(datas, open('point in region/number/measurements.json', 'w'))
    print(datas)
    print('over')







