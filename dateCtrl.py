from tkinter import *
import calendar
from datetime import *
from matplotlib.patches import Polygon
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkinter as tk
from beijing import Beijing


class DateCtrl(Frame):
    def __init__(self, master=None, cnf={}, **kw):
        Frame.__init__(self, master=root)
        self.count = 0
        self.master = master
        self.master.size = (100, 110)
        # self.master.resizable(False, False)
        self.time = "2017-3-4"
        self.date = datetime.strptime(self.time, '%Y-%m-%d')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid(sticky=W + E + N + W)
        self.dayid = []
        self.UpdateUI()

    def SetDate(self, date):
        self.date = date
        self.UpdateUI()

    def GetDate(self):
        return self.date

    def MonthBack(self):

        if date == date.min:
            return
        if self.date.month == 1:
            self.date = self.date.replace(year=self.date.year - 1, month=12)
        else:
            if self.date.day > calendar.monthrange(self.date.year, self.date.month - 1)[1]:
                self.date = self.date.replace(month=self.date.month - 1,
                                              day=calendar.monthrange(self.date.year, self.date.month - 1)[1])
            else:
                self.date = self.date.replace(month=self.date.month - 1)
        self.UpdateUI()

    def MonthFoeward(self):
        if date == date.max:
            return
        if self.date.month == 12:
            self.date = self.date.replace(year=self.date.year + 1, month=1)
        else:
            if self.date.day > calendar.monthrange(self.date.year, self.date.month + 1)[1]:
                self.date = self.date.replace(month=self.date.month + 1,
                                              day=calendar.monthrange(self.date.year, self.date.month + 1)[1])
            else:
                self.date = self.date.replace(month=self.date.month + 1)
        self.UpdateUI()

    def UpdateUI(self):
        lendayid = len(self.dayid)
        for i in range(lendayid):
            self.dayid[lendayid - i - 1].destroy()
            del (self.dayid[lendayid - i - 1])
        self.backwardBt = Button(text='<', command=self.MonthBack).grid(row=0, column=6, sticky=W + E + N + S)
        self.YMBtn = Button(text='%d-%d' % (self.date.year, self.date.month),
                            command=lambda sf=self: print(sf.date)).grid(row=0, column=7, columnspan=5,
                                                                         sticky=W + E + N + S)
        self.forwardBt = Button(text='>', command=self.MonthFoeward).grid(row=0, column=12, sticky=W + E + N + S)
        col = 6
        for wk in ['一', '二', '三', '四', '五', '六', '日']:
            Label(text=wk).grid(row=1, column=col, sticky=W + E + N + S)
            col += 1
        row = 2
        col = 6
        today = date.today()
        for weekday in calendar.monthcalendar(self.date.year, self.date.month):
            for dayt in weekday:
                if dayt == 0:
                    col += 1
                    continue
                bkcolour = 'lightgray'
                # if col == 5 + 6:
                # bkcolour = 'green'
                # if col == 6 + 6:
                # bkcolour = 'blue'
                if dayt == self.date.day:
                    bkcolour = 'red'
                    # canvas.show()

                tdrelief = FLAT
                if self.date.year == today.year and self.date.month == today.month and dayt == today.day:
                    tdrelief = GROOVE
                bt = Button(self.master, text='%d' % dayt, relief=tdrelief, bg=bkcolour,
                            command=lambda sf=self, dt=dayt: sf.rpday(dt))
                bt.grid(row=row, column=col, sticky=W + E + N + S)
                self.dayid.append(bt)
                col += 1
            row += 1
            col = 6

    def rpday(self, dt):

        day = str(self.date).replace('-', '')
        day = day[0:6] + '%02d' % dt
        # print(day)
        self.onClick(day)

        self.date = self.date.replace(day=dt)
        self.UpdateUI()

# def onmousemove(event):
#     # print(' x=%d, y=%d, xdata=%f, ydata=%f' %( event.x, event.y, event.xdata, event.ydata))
#     xy = list((event.xdata, event.ydata))
#     polygons = []
#     for region in map.county_region:
#         polygons.append(Polygon(region))
#
#     for i, poly in enumerate(polygons):
#         try:
#             if poly.contains_point(xy):
#                 print('point in region:', i)
#                 break
#         except TypeError:
#             pass

def onClick(dt = '20170304'):
    map.countyHotmap(axes, dt)
    canvas.show()

if __name__ == '__main__':
    root = tk.Tk()
    frame = tk.Frame(master=root)

    frame1 = Frame(frame)
    frame1.pack()
    f = Figure(figsize=(8, 8), dpi=100)
    axes = f.add_subplot(111)
    map = Beijing(ax=axes)
    canvas = FigureCanvasTkAgg(f, master=frame1)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    # cid = f.canvas.mpl_connect('motion_notify_event', onmousemove)

    toolbar = NavigationToolbar2TkAgg(canvas, frame1)
    toolbar.update()

    frame.grid(row=0, rowspan=20)

    mainfram = DateCtrl(root)
    mainfram.onClick = onClick
    # tdt =datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
    # mainfram.SetDate(tdt.replace(day=30))  # 试试重置日期

    root.mainloop()
