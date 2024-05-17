#Tushare get stock data
# -*- coding: utf-8 -*-

import tushare as ts
import matplotlib.pyplot as plt
from datetime import datetime

data = ts.get_hist_data('600848',start='2018-03-01',end='2018-03-31')
print(data)
# 对时间进行降序排列
data = data.sort_index()
#data.index是一个日期字符串,将data.index通过strptime函数转换成'%Y-%m-%d'形式，然后调用toordinal()
#将日期字符串转换成时间序列形式，即是一个整数的形式
xs = [datetime.strptime(d, '%Y-%m-%d').toordinal() for d in data.index ]
plt.plot_date( xs , data['open'] , 'b-')
plt.gcf().autofmt_xdate()  # 自动旋转日期标记
plt.show()