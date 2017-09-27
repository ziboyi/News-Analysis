# -*- encoding: utf-8 -*-
# Written by Zibo


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.font_manager import FontManager
import subprocess
from pylab import mpl

def get_matplot_zh_font():
    fm = FontManager()
    mat_fonts = set(f.name for f in fm.ttflist)

    output = subprocess.check_output('fc-list :lang=zh -f "%{family}\n"', shell=True)
    zh_fonts = set(f.split(',', 1)[0] for f in output.split('\n'))
    available = list(mat_fonts & zh_fonts)

    print '*' * 10, '可用的字体', '*' * 10
    for f in available:
        print f
    return available

def set_matplot_zh_font():
    available = get_matplot_zh_font()
    if len(available) > 0:
        mpl.rcParams['font.sans-serif'] = [available[0]]    # 指定默认字体
        mpl.rcParams['axes.unicode_minus'] = False          # 解决保存图像是负号'-'显示为方块的问题

set_matplot_zh_font()

rc('font', size=20)

xData = range(0, 19)

yData1 = (0.0122156942586, 0.0170810420603, 0.0213370029695, 0.0176102220254, 0.0186724004139, 0.0139551964745, 0.015475732855, 0.0125046817045, 0.0138979799979, 0.0160960591133, 0.0170920763364, 0.0198259483974, 0.0161920966343, 0.0165643428763, 0.0188748741539, 0.0203221523007, 0.0136971704784, 0.0141913781405, 0.01607999799) #中国
yData2 = (0.00820196614508, 0.0090766258307, 0.0110813355544, 0.0100575621481, 0.00832578892913, 0.0103562247521, 0.00771651077037, 0.00495354540951, 0.00599759487312, 0.00652709359606, 0.00474779898232, 0.00644522073094, 0.00500298601643, 0.0061860088132, 0.00351959925679, 0.00624345344627, 0.00515339087307, 0.0082568018272, 0.00685912414261) #美国
yData3 = (0.00395555814089, 0, 0.00443253422177, 0, 0.00397697878945, 0.0027910392949, 0.0037301214425, 0, 0.0030444644026, 0, 0, 0.00383036097322, 0, 0, 0, 0, 0.00404909282884, 0.00469223344578, 0) #日本
yData4 = (0, 0, 0, 0.00280852678854, 0.00368598034144, 0, 0, 0, 0, 0.00374384236453, 0.0155232384118, 0.0145758002901, 0.0187161256155, 0.00647481344153, 0.0118847863276, 0.0222685922126, 0.01244757006, 0.0142678300093, 0.014296123213) #印度
yData5 = (0.00290849863301, 0.0034183315994, 0.00420076772652, 0.00422544120438, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) #韩国
yData6 = (0, 0, 0.00320127471572, 0.00365614523373, 0, 0, 0, 0.00339499087823, 0.00286179653844, 0.00678571428571, 0, 0.00273743130886, 0.00305362434787, 0, 0, 0, 0.0032353995331, 0, 0) #台湾
yData7 = (0.00471176778547, 0.00365188220557, 0.0033026725574, 0, 0, 0, 0, 0, 0, 0.00332512315271, 0.00366406225809, 0, 0, 0, 0, 0, 0, 0, 0) #航母
yData8 = (0, 0.00667742414913, 0.00341855580503, 0, 0, 0, 0.00244878201569, 0, 0.00293790814851, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) #飞机
yData9 = (0, 0.00409775154462, 0.00446150503368, 0.00301094313366, 0.00278065183652, 0.0045354388542, 0.0026196272726, 0.00326209087944, 0, 0.00349753694581, 0.00343699361111, 0.00340136054422, 0.00313250025353, 0.00276693466494, 0, 0, 0, 0.00344989057826, 0.00293962463255) #海军
yData10 = (0, 0.00319539692987, 0.00372274933005, 0, 0.00402547853078, 0.00411311053985, 0, 0.00329833633365, 0, 0.0034236453202, 0, 0.00319707462565, 0.00296348045568, 0, 0, 0, 0.00279949241037, 0.00303896178362, 0) #导弹


plt.figure(num=1, figsize=(8, 6.5))
plt.axis([0, 25, 0, 0.025])
#plt.title('Plot 1', size=14)
plt.xlabel('Week')
plt.ylabel('Frequency')
#plt.plot(xData1, yData1, color='b', linestyle='--', marker='o', label='lambda=1')
plt.plot(xData, yData1, color='r', linestyle='-', label=u'中国')
plt.plot(xData, yData2, color='r', linestyle='--', label=u'美国')
plt.plot(xData, yData3, color='g', linestyle='-', label=u'日本')
plt.plot(xData, yData4, color='g', linestyle='--', label=u'印度')
plt.plot(xData, yData5, color='b', linestyle='-', label=u'韩国')
plt.plot(xData, yData6, color='b', linestyle='--', label=u'台湾')
plt.plot(xData, yData7, color='c', linestyle='-', label=u'航母')
plt.plot(xData, yData8, color='c', linestyle='--', label=u'飞机')
plt.plot(xData, yData9, color='m', linestyle='-', label=u'海军')
plt.plot(xData, yData10, color='m', linestyle='--', label=u'导弹')
plt.legend(loc='upper right', fontsize='small')
plt.savefig('word_frequency.pdf', format='pdf')
