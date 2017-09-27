# -*- encoding: utf-8 -*-
# Written by Zibo


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.font_manager import FontManager
import subprocess
from pylab import mpl
import pandas as pd

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
yTopic0 = []
yTopic1 = []
yTopic2 = []
yTopic3 = []
yTopic4 = []
yTopic5 = []
yTopic6 = []
yTopic7 = []


df = pd.read_csv('../data/news_topic.csv', sep='\t')
for i in range(19):
    df_topic_per_week = df[df['news week'].isin([i])]
    yTopic0.append(df_topic_per_week['topic0'].mean())
    yTopic1.append(df_topic_per_week['topic1'].mean())
    yTopic2.append(df_topic_per_week['topic2'].mean())
    yTopic3.append(df_topic_per_week['topic3'].mean())
    yTopic4.append(df_topic_per_week['topic4'].mean())
    yTopic5.append(df_topic_per_week['topic5'].mean())
    yTopic6.append(df_topic_per_week['topic6'].mean())
    yTopic7.append(df_topic_per_week['topic7'].mean())


plt.figure(num=1, figsize=(8, 6.5))
plt.axis([0, 25, 0, 0.5])
#plt.title('Plot 1', size=14)
plt.xlabel('Week')
plt.ylabel('topic composition')
#plt.plot(xData1, yData1, color='b', linestyle='--', marker='o', label='lambda=1')
plt.plot(xData, yTopic0, color='r', linestyle='-', label='Topic0')
plt.plot(xData, yTopic1, color='r', linestyle='--', label='Topic1')
plt.plot(xData, yTopic2, color='g', linestyle='-', label='Topic2')
plt.plot(xData, yTopic3, color='g', linestyle='--', label='Topic3')
plt.plot(xData, yTopic4, color='b', linestyle='-', label='Topic4')
plt.plot(xData, yTopic5, color='b', linestyle='--', label='Topic5')
plt.plot(xData, yTopic6, color='c', linestyle='-', label='Topic6')
plt.plot(xData, yTopic7, color='c', linestyle='--', label='Topic7')

plt.legend(loc='upper right', fontsize='small')
plt.savefig('topic_trend.pdf', format='pdf')
