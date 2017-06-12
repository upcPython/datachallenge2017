import matplotlib.patches as mpatches
import matplotlib.pylab as plt
import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
class Numberlegend:
    def __init__(self,ax):
        self.ax=ax

    def makedata(self,date='20170304'):
        def load(on):
            with open(on) as json_file:
                tu_1data = json.load(json_file)
                return tu_1data
        list = load('config/Phone_nums/'+date+'.json')
        return list
    def draw(self,date='20170304'):
        data = self.makedata(date)
        plt.sca(self.ax)
        label = []
        listcolor=['r','orange','yellow','#40fd14','#019529','#2afeb7','#d5ffff','#fa5ff7','#ffd1df','#fe7b7c','#770001','#6600CC','#663300','#000099','#000000']
        patch=[]
        for i in range(15):
            label.append(data[i])
            #plt.plot([], label=list[i], color=listcolor[i],marker='*')
            red_patch = mpatches.Patch(label=data[i], color=listcolor[i])
            patch.append(red_patch)
        plt.collections = []
        plt.legend(handles=[patch[0],patch[1],patch[2],patch[3],patch[4],patch[5],patch[6],patch[7],patch[8],patch[9],patch[10],patch[11],patch[12],patch[13],patch[14]],ncol=3)
        plt.axis('off')

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.gca()
    x = np.arange(1, 11, 1)
    dictAx=Numberlegend(ax)
    dictAx.draw()
    plt.show()