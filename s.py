import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

'''显示中文'''
matplotlib.rc("font", family='YouYuan')

data_address = "实验数据/共享单车租用影响因素分析/share bike.csv"
# 以只读模式打开一个CSV文件
data = pd.read_csv(data_address)
columns_name = data.columns

'''查找算法'''


def data_find(data_data, num):
    oooo = 0
    for i in range(0, len(data_data)):
        if data_data[i] == num:
            oooo = 1
            return i
    if (oooo == 0):
        return -1

data_time_ = pd.to_datetime(data['datetime'])
#   时间的影响
average_time_data = pd.DataFrame(columns=['time', 'num', 'count', 'casual', 'registered'])

for i in range(0, 24):
    average_time_data.loc[i] = [i, 0, 0, 0, 0]
for i in range(0, len(data)):
    index = data_find(average_time_data['time'], data_time_[i].hour)
    average_time_data.loc[index] = [average_time_data['time'][index], average_time_data['num'].loc[index] + 1,
                                    data['count'][i] + average_time_data['count'].loc[index],
                                    data['casual'][i] + average_time_data['casual'].loc[index],
                                    data['registered'][i] + average_time_data['registered'].loc[index]]
average_time_data.sort_values(by='time', axis=0, ascending=True, inplace=True)
time = np.array([*average_time_data['time']])
fig = plt.figure(figsize=(12, 8))
# 创建一个子图，然后在子图上操作
ax1 = fig.add_subplot(1, 1, 1)

width = 0.3
rects1 = ax1.bar(time, average_time_data['count'], width=width, color='gray',
                 label='所有用户')
rects2 = ax1.bar(time - width, average_time_data['casual'], width=width, color='lightgray',
                 label='未注册')
rects3 = ax1.bar(time + width, average_time_data['registered'], width=width, color='darkgray',
                 label='注册')

ax1.xaxis.set_ticks_position('bottom')
# 刻度线只显示在 y 轴 右侧。
ax1.yaxis.set_ticks_position('left')
# 显示label 里面设置的图例
ax1.legend(title="类别",
           fontsize=16,
           title_fontsize=15,
           bbox_to_anchor=(0.25, 0.35))
ax1.set_title('时间影响的柱状图\n时间影响的折线图')
ax1.plot(average_time_data['time'], average_time_data['count']/len(average_time_data['count']), c='black')
plt.show()
