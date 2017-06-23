import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import math
import json

rcParams['font.sans-serif'] = ['SimHei']
rcParams['font.family'] = ['sans-serif']
dis = {0: '房山区', 1: '门头沟区', 2: '石景山区', 3: '昌平区', 4: '延庆县', 5: '怀柔区', 6: '朝阳区', 7: '大兴区', 8: '崇文区', 9: '丰台区', 10: '海淀区',
       11: '宣武区', 12: '西城区', 13: '东城区', 14: '通州区', 17: '顺义区', 19: '平谷区', 20: '密云县'}


class PieChart:
    def __init__(self, ax):
        self.ax = ax
        self.theta = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300,
                      315,
                      330, 345]
        self.thetalist =[7.5, 22.5, 37.5, 52.5, 67.5, 82.5, 97.5, 112.5, 127.5, 142.5, 157.5, 172.5, 187.5, 202.5, 217.5, 232.5, 247.5, 262.5, 277.5, 292.5, 307.5, 322.5, 337.5,352.5]
        self.colorlist=[]
        self.bars = []

    def draw(self, district=6,aDay='20170304'):
        path = 'config/pieChart/' + dis[district] + aDay + '.json'
        with open(path) as json_file:
            daydata = json.load(json_file)
        plt.sca(self.ax)
        radii = list(daydata.values())
        textlist = list(daydata.keys())
        maxval = max(radii)
        lenth = len(str(maxval))
        if lenth == 5:
            multiple = 1000
        elif lenth == 4:
            multiple = 100
        elif lenth == 3:
            multiple = 10
        else:
            multiple = 1
        for i in range(24):
            if i < len(radii):
                radii[i] /=multiple
            else:
                radii.append(0)
        theta1 = []
        for i in self.theta:
            theta1.append(i / 180 * np.pi)
        self.barColor(textlist)
        plt.cla()
        self.bars = self.ax.bar(theta1, radii, width=np.pi / 12, bottom=0.0,color=self.colorlist,alpha=0.5)
        danwei = '单位:' + str(multiple) + '条'
        plt.thetagrids(self.thetalist, textlist)
        self.ax.set_rlabel_position('-90')  # 坐标位置
        plt.text(-np.pi*0.25, maxval/multiple*1.68, danwei, fontsize=16)


    def barColor(self, textlist):
        listcolor = ['r', 'orange', 'yellow', '#40fd14', '#019529', '#2afeb7', '#d5ffff', '#fa5ff7', '#ffd1df',
                     '#fe7b7c', '#770001']
        top = [['信用卡', '我行', '冻结', '解冻', '办理', '用户', '逾期', '客服', '根据', '额度'],
               ['发票', '公司', '代开', '行业', '正规', '保真', '打扰', '增值税', '北京', '各种'],
               ['积分', '兑换', '现金', '登录', '用户', '账户', '清零', '到期', '24小时', '网址'],
               ['淘宝', '加入', '良好', '时间', '工作', 'qq', '待遇', '50元'],
               ['设备', 'apple', 'iphone', '本人', '操作', '丢失', '登录', '激活', '正在', '用户'],
               ['流量', '中国\n移动', '使用', '手机', '北京', '移动', '营业厅', '余额', '话费', '查询'],
               ['地址', '改签', '航班', '免费', '咨询', '招聘', '成功', '欢迎', '旅客', '北京'],
               ['澳门', '投注', '平台', '百家乐', '葡京', '注册', '1000\n元', '金沙', '家居', '地址'],
               ['贷款', '抵押', '办理', '放款', '信用卡', '利息', '身份证', '额度', '当天', '车辆'],
               ['退订', '验证码', '人满', '收费', '免费', '财富', 'qq群', '群友', '收益', '全部', '坐镇'],
               ['上门\n服务', '酒店', '模特', '空姐', '白领', '少妇', '公寓', '打扰', '付款', '学生']]
        for j in textlist:
            cnt=0
            for i in range(11):
                if j in top[i]:
                    self.colorlist.append(listcolor[i])
                    cnt=1
                    break
            if cnt==0:
                    self.colorlist.append('y')

if __name__ == "__main__":
    axes = plt.subplot(111, projection='polar')
    piechart = PieChart(axes)
    district = 17
    piechart.draw(district=district)
    plt.show()
