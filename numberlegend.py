import matplotlib.patches as mpatches
import matplotlib.pylab as plt
import json
import matplotlib.colors as colors

import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.sans-serif']=['SimHei']
rcParams['font.family']=['sans-serif']
class Numberlegend:
    def __init__(self,ax):
        self.ax=ax

    def makedata(self,date='20170304'):
        def load(on):
            with open(on) as json_file:
                tu_1data = json.load(json_file)
                return tu_1data
        dict = load('config/Phone_nums/'+date+'.json')
        return dict
    def draw(self,aDay):
        dict = self.makedata(aDay)
        plt.sca(self.ax)
        list=sorted(dict, key=dict.get, reverse=True)
        sum=0
        for i in list:
            sum=sum+dict[i]
        sum=sum/25
        label = []
        #listcolor=['r','orange','yellow','#40fd14','#019529','#2afeb7','#d5ffff','#fa5ff7','#ffd1df','#fe7b7c','#770001','#6600CC','#663300','#000099','#000000']
        patch=[]
        for i in range(10):
            label.append(list[i])
            #plt.plot([], label=list[i], color=listcolor[i],marker='*')
            a = plt.cm.Blues
            c=colors.rgb2hex(a(dict[list[i]]/sum))
            red_patch = mpatches.Patch(label=list[i], color=c)
            patch.append(red_patch)
        plt.collections = []

        plt.legend(handles=patch[:10],ncol=2,fontsize=20,loc='center')
        # plt.legend(handles=[patch[0],patch[1],patch[2],patch[3],patch[4],patch[5],patch[6],patch[7],patch[8],patch[9],patch[10],patch[11],patch[12],patch[13],patch[14],patch[15],patch[16],patch[17],patch[18],patch[19]],ncol=2,fontsize=20,loc='center')

        #plt.legend(handles=[patch[0],patch[1]],ncol=2)
        plt.title('Top10 伪基站号码', fontsize=25,loc='center')
        plt.axis('off')

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.gca()
    dictAx=Numberlegend(ax)
    dict=dictAx.makedata('20170304')
    dictAx.draw(dict)
    plt.show()