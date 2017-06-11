
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib import rcParams
import json
rcParams['font.sans-serif'] = ['SimHei']
rcParams['font.family'] = 'sans-serif'

def radar_factory(num_vars, frame='circle'):

    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
    # rotate theta such that the first axis is at the top
    theta += np.pi/2

    def draw_poly_patch(self):
        verts = unit_poly_verts(theta)
        return plt.Polygon(verts, closed=True, edgecolor='k')

    def draw_circle_patch(self):
        # unit circle centered on (0.5, 0.5)
        return plt.Circle((0.5, 0.5), 0.5)

    patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
    if frame not in patch_dict:
        raise ValueError('unknown value for `frame`: %s' % frame)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1
        # define draw_frame method
        draw_patch = patch_dict[frame]

        def fill(self, *args, **kwargs):
            """Override fill so that line is closed by default"""
            closed = kwargs.pop('closed', True)
            return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super(RadarAxes, self).plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels,color='k')

        def _gen_axes_patch(self):
            return self.draw_patch()

        def _gen_axes_spines(self):
            if frame == 'circle':
                return PolarAxes._gen_axes_spines(self)
            # The following is a hack to get the spines (i.e. the axes frame)
            # to draw correctly for a polygon frame.

            # spine_type must be 'left', 'right', 'top', 'bottom', or `circle`.
            spine_type = 'circle'
            verts = unit_poly_verts(theta)
            # close off polygon by repeating first vertex
            verts.append(verts[0])
            path = Path(verts)

            spine = Spine(self, spine_type, path)
            spine.set_transform(self.transAxes)
            return {'polar': spine}

    register_projection(RadarAxes)
    return theta


def unit_poly_verts(theta):
    x0, y0, r = [0.5] * 3
    verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
    return verts

def load(on):
    with open(on) as json_file:
        tu_1data = json.load(json_file)
        return tu_1data

def makedata(datename):
    # The following data is from the Denver Aerosol Sources and Health study.
    # See  doi:10.1016/j.atmosenv.2008.12.017
    #
    # The data are pollution source profile estimates for five modeled
    # pollution sources (e.g., cars, wood-burning, etc) that emit 7-9 chemical
    # species. The radar charts are experimented with here to see if we can
    # nicely visualize how the modeled source profiles change across four
    # scenarios:
    #  1) No gas-phase species present, just seven particulate counts on
    #     Sulfate
    #     Nitrate
    #     Elemental Carbon (EC)
    #     Organic Carbon fraction 1 (OC)
    #     Organic Carbon fraction 2 (OC2)
    #     Organic Carbon fraction 3 (OC3)
    #     Pyrolized Organic Carbon (OP)
    #  2)Inclusion of gas-phase specie carbon monoxide (CO)
    #  3)Inclusion of gas-phase specie ozone (O3).
    #  4)Inclusion of both gas-phase species is present...
    linshi=load('config/JsonTime/'+datename+'.json')
    tuple=('',linshi)
    data = [['银行诈骗', '黑发票', '积分兑换\n诈骗', '淘宝刷单\n招聘', 'Apple设备\n诈骗', '移动短信', '小广告', '澳门赌博', '贷款\n抵押', '炒股\n诈骗', '特殊服务']]
    data.append(tuple)
    return data


class RadarAx:
    def __init__(self, ax,theta):
        self.theta = theta
        self.ax = ax
        self.days=[['20170219','20170220','20170221','20170222','20170223','20170224','20170225'],
      ['20170226','20170227','20170228','20170301','20170302','20170303','20170304'],
      ['20170305','20170306','20170307','20170308','20170309','20170310','20170311'],
      ['20170312','20170313','20170314','20170315','20170316','20170317','20170318'],
      ['20170319','20170320','20170321','20170322','20170323','20170324','20170325'],
      ['20170326','20170327','20170328','20170329','20170330','20170331','20170401'],
      ['20170402','20170403','20170404','20170405','20170406','20170407','20170408'],
      ['20170409','20170410','20170411','20170412','20170413','20170414','20170415'],
      ['20170416','20170417','20170418','20170419','20170420','20170421','20170422'],
      ['20170423','20170424','20170425','20170426','20170427','20170428','20170429']]
        self.draw()

    def draw(self, aDay='20170304'):
        data = makedata(aDay)
        plt.sca(self.ax)
        self.ax.lines = []
        self.ax.patches = []
        colors = ['b', 'r', 'g', 'm']
        spoke_labels = data.pop(0)
        title, case_data = data[0]
        self.ax.set_rgrids([2, 4, 6, 8])
        # ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1), color='white',
        #              horizontalalignment='center', verticalalignment='center')
        for d, color in zip(case_data, colors):
            self.ax.plot(self.theta, d, color=color)
            self.ax.fill(self.theta, d, facecolor=color, alpha=0.05)
        self.ax.set_varlabels(spoke_labels)

        # add legend relative to top-left plot
        # ax = axes[0]
        # ax = axes[0, 0]
        labels = ('0am-6am', '7am-12am', '12am-7pm', '7pm-12pm')
        self.ax.legend(labels, loc=(0.9, .95),
                           labelspacing=0.1, fontsize='small')
        # fig.text(0.5, 0.965, 'Radar of Topic',
        #          horizontalalignment='center', color='white', weight='bold',
        #          size='large')
        #plt.pcolor(data, cmap=plt.cm.Blues)

if __name__ == "__main__":
    N = 11
    theta = radar_factory(N, frame='polygon')
    # data = example_data(RadarAx.day)

    fig, axes = plt.subplots(figsize=(5, 5), nrows=1, ncols=1,facecolor='b',
                             subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)


    # Plot the four cases from the example data on separate axes
    # for ax, (title, case_data) in zip(axes.flatten(), data):

    ax = axes
    Radar=RadarAx(ax,theta)
    # for ax, (title, case_data) in zip(axes, data):

    plt.show()