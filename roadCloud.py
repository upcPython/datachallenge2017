import codecs,random
import jieba,  jieba.analyse
import matplotlib.pylab as plt
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import  re,os
import json
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.sans-serif']=['SimHei']
rcParams['font.family']=['sans-serif']
dis={0:'房山区',1:'门头沟区',2:'石景山区',3:'昌平区',4:'延庆县',5:'怀柔区',6:'朝阳区',7:'大兴区',8:'崇文区',9:'丰台区',10:'海淀区',11:'宣武区',12:'西城区',13:'东城区',14:'通州区',17:'顺义区',19:'平谷区',20:'密云县'}
class RoadCloud:
    def __init__(self,ax):
        self.ax=ax
        plt.sca(ax)

    def makedata(self,district,date):
        def load(on):
            with open(on) as json_file:
                tu_1data = json.load(json_file)
                return tu_1data
        dict = load('config/dicofblock/'+dis[district]+date+'.json')
        return dict
    def draw(self,district=6,date='20170304'):
        content = self.makedata(district,date)
        if len(content)==0:
            return
        plt.sca(self.ax)
        if len(self.ax.texts)>0:
            self.ax.texts.pop()
        plt.text(235,85,dis[district],fontsize=25)
        backgroud_Image= plt.imread('config/districtmap/'+dis[district]+'_'+str(district)+'.jpg')
        #plt.imshow(backgroud_Image)
        #plt.show()
        wc = WordCloud(
                       background_color='white',  # 设置背景颜色
                       mask=backgroud_Image,  # 设置背景图片
                       max_words=2000,  # 设置最大现实的字数
                       stopwords=STOPWORDS,  # 设置停用词
                       font_path='simfang.ttf',  # 设置字体格式，如不设置显示不了中文
                       max_font_size=500,  # 设置字体最大值
                       random_state=1,  # 设置有多少种随机生成状态，即有多少种配色方案
                       ).fit_words(content)
        plt.imshow(wc)
        #plt.title(dis[district],fontsize=25)


if __name__ == '__main__':
    #dis={'0':'房山区','1':'门头沟区','2':'石景山区','3':'昌平区','4':'延庆县','5':'怀柔区','6':'朝阳区','7':'大兴区','8':'崇文区','9':'丰台区','10':'海淀区','11':'宣武区','12':'西城区','13':'东城区','14':'通州区','17':'顺义区','19':'平谷区','20':'密云县'}
    fig = plt.figure()
    ax = fig.gca()
    dataAx = RoadCloud(ax)
    district=6
    date='20170323'
    # if district in dis.keys():
    dataAx.draw(district,date)
    plt.axis('off')
    plt.show()
