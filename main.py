import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

'''显示中文'''
matplotlib.rc("font", family='YouYuan')

data_address = "./实验数据/共享单车租用影响因素分析/share bike.csv"
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


'''----------------------------------------------------------------------------------------------------------------'''
# 注册用户与非注册用户的占比
casual_num = 0
registered_num = 0

# 节假日与非节假日平均骑车人数
holiday_num = 0
holiday_times = 0
unholiday_num = 0
unholiday_times = 0

# 工作日与非工作日
working_num = 0
working_times = 0
unworking_num = 0
unworking_times = 0

# 天气
weather_num = [0, 0, 0, 0]

for i in range(0, len(data)):
    casual_num += data['casual'].loc[i]
    registered_num += data['registered'].loc[i]
    if data['holiday'].loc[i] == 1:
        holiday_num += data['count'].loc[i]
        holiday_times += 1
    else:
        unholiday_num += data['count'].loc[i]
        unholiday_times += 1
    if data['workingday'].loc[i] == 1:
        working_num += data['count'].loc[i]
        working_times += 1
    else:
        unworking_num += data['count'].loc[i]
        unworking_times += 1
    weather_num[data['weather'].loc[i] - 1] += 1

'''------------------------------------------------------------------------------------------------------------------'''
fig = plt.figure(figsize=(8, 5))
ax1 = fig.add_subplot(1, 1, 1)
# ax1注册用户和非注册用户的图片
ax1.pie([casual_num, registered_num], labels=['未注册用户', '注册用户'], autopct='%.2f%%', colors=['lightgray', 'gray'])
ax1.set_title('注册用户与非注册用户的关系')
plt.show()

''''''
fig = plt.figure(figsize=(8, 5))
ax2 = fig.add_subplot(1, 2, 1)
ax3 = fig.add_subplot(1, 2, 2)
# 节假日与非节假日数量关系
ax2.pie([holiday_num * 24 / holiday_times, unholiday_num * 24 / unholiday_times], labels=['节假日', '非节假日'],
        autopct='%.2f%%', colors=['lightgray', 'gray'])
ax2.set_title('节假日与非节假日平均骑行数量')

ax3.pie([holiday_num * 24, unholiday_num * 24], labels=['节假日', '非节假日'],
        autopct='%.2f%%', colors=['lightgray', 'gray'])
ax3.set_title('节假日与非节假日总骑行数量')
plt.show()

''''''
fig = plt.figure(figsize=(8, 5))
ax2 = fig.add_subplot(1, 2, 1)
ax3 = fig.add_subplot(1, 2, 2)

# 工作日与非工作日数量关系
ax2.pie([working_num, unworking_num], labels=['工作日', '非工作日'],
        autopct='%.2f%%', colors=['lightgray', 'gray'])
ax2.set_title('工作日与非工作日平均骑行数量')

ax3.pie([working_num / working_times, unworking_num / unworking_times], labels=['工作日', '非工作日'],
        autopct='%.2f%%', colors=['lightgray', 'gray'])
ax3.set_title('工作日与非工作日总骑行数量')
plt.show()

''''''
fig = plt.figure(figsize=(8, 5))
ax2 = fig.add_subplot(1, 1, 1)

# 天气
ax2.pie(weather_num, labels=['晴天，多云', '雾天，阴天', '小雪，小雨', '大雨，大雪，大雾'],
        autopct='%.2f%%', colors=['gainsboro', 'lightgray', 'gray', 'black'])
ax2.set_title('天气的分布')
plt.show()


''''''
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(1, 1, 1)


data_time_ = pd.to_datetime(data['datetime'])
#温度#体感温度
temp_data = pd.DataFrame(columns=['temp'])
atemp_data =pd.DataFrame(columns=['atemp'])
time_ = 0
time_lines = 0
temp_24hour = []
atemp_24hour = []


def average(list_data):
    all = 0
    all_times = 0
    for i in list_data:
        all+=i
        all_times+=1
    return all/all_times

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
for i in range(0, len(data)):

    if time_==0:
        temp_data.loc[time_lines] = [0]
        atemp_data.loc[time_lines] = [0]
    temp_24hour.append(data['temp'][i])
    atemp_24hour.append(data['atemp'][i])

    time_+=1
    if time_ == 24:
        time_ = 0
        temp_data.loc[time_lines] = [average(temp_24hour)]
        atemp_data.loc[time_lines] = [average(atemp_24hour)]
        time_lines+=1
        temp_24hour.clear()
        atemp_24hour.clear()


xtick = np.arange(len(temp_data))
rects1 = ax1.plot(temp_data['temp'],label='大气温度',color='slategray')
rects2 = ax1.plot(atemp_data['atemp'],label='体感温度',color = 'black')

ax1.set_title("比较每天平均温度")
ax1.legend(title="类别",
           fontsize=16,
           title_fontsize=15,
           bbox_to_anchor=(0.3, 0.2))
month = [1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12]
# 设置 X轴刻度

ax1.set_xticks(xtick,minor=True)
# 设置 X轴刻度标签
ax1.set_xlabel('日期(以日为单位)，中间缺失部分天数', fontsize=15)
# Y 轴
ax1.yaxis.set_tick_params(which="both", labelsize=10)
ax1.set_ylabel('温度')

plt.show()
'''------------------------------------------------------------------------------------------------------------------'''

#   天气的影响
average_weather_data = pd.DataFrame(columns=['weather', 'num', 'count', 'casual', 'registered'])
average_weather_lines = 0
for i in range(0, len(data)):

    index = data_find(average_weather_data['weather'], data['weather'][i])
    if index == -1:
        average_weather_data.loc[average_weather_lines] = [data['weather'][i], 1, data['count'][i], data['casual'][i],
                                                           data['registered'][i]]
        average_weather_lines += 1
    else:
        average_weather_data.loc[index] = [data['weather'][i], average_weather_data['num'].loc[index] + 1,
                                           data['count'][i] + average_weather_data['count'].loc[index],
                                           data['casual'][i] + average_weather_data['casual'].loc[index],
                                           data['registered'][i] + average_weather_data['registered'].loc[index]]

average_weather_data.sort_values(by='weather', axis=0, ascending=True, inplace=True)
weather = ['晴天\n多云', '雾天\n阴天', '小雪\n小雨', '大雨\n大雪\n大雾']
weather_data = pd.DataFrame(columns=['weather', 'num', 'count', 'casual', 'registered'])
for i in range(0, 4):
    weather_data.loc[weather[i]] = [average_weather_data['weather'][i], average_weather_data['num'][i],
                                    average_weather_data['count'][i], average_weather_data['casual'][i],
                                    average_weather_data['registered'][i]]
fig = plt.figure(figsize=(12, 8))
# 创建一个子图，然后在子图上操作
ax1 = fig.add_subplot(2, 1, 1)
customers_index = np.arange(len(weather))
width = 0.3
rects1 = ax1.bar(customers_index, weather_data['count'], width=width, align='center', color='black',
                 label='所有用户')
rects2 = ax1.bar(customers_index - width, weather_data['casual'], width=width, align='center', color='lightgray',
                 label='未注册(左侧)')
rects3 = ax1.bar(customers_index + width, weather_data['registered'], width=width, align='center', color='gray',
                 label='注册(右侧)')
ax1.bar_label(rects1, padding=3, **{'fontsize': 14})
ax1.bar_label(rects2, padding=3)
ax1.bar_label(rects3, padding=3)
ax1.xaxis.set_ticks_position('bottom')
# 刻度线只显示在 y 轴 右侧。
ax1.yaxis.set_ticks_position('left')
# 显示label 里面设置的图例
ax1.legend(title="类别",
           fontsize=16,
           title_fontsize=15,
           bbox_to_anchor=(1.01, 0.7))
# 设置 X轴刻度
ax1.set_xticks(customers_index)
# 设置 X轴刻度标签
ax1.set_xticklabels(weather)
# 设置 X 轴标签，字体大小
ax1.xaxis.set_tick_params( labelsize=12)
# 设置 X轴标签
ax1.set_xlabel('天气', fontsize=15)
# Y 轴
ax1.yaxis.set_tick_params(which="both", labelsize=10)
ax1.set_ylabel('人数')
ax1.set_title('各天气下骑行总人数')
ax2 = fig.add_subplot(2, 1, 2)
ax2.bar(customers_index, weather_data['count'] / weather_data['num'], width=width, align='center', color='gray',
        label='all')

# 设置 X轴刻度
ax2.set_xticks(customers_index)
# 设置 X轴刻度标签
ax2.set_xticklabels(weather)
ax2.xaxis.set_tick_params(labelsize=12)
# 设置 X轴标签
ax2.set_xlabel('天气', fontsize=15)
# Y 轴
ax2.yaxis.set_tick_params(which="both", labelsize=10)
ax2.set_ylabel('人数')
ax2.set_title('每小时平均骑行总人数')
ax1.legend(title="类别",
           fontsize=16,
           title_fontsize=15,
           bbox_to_anchor=(1.01, 0.7))
plt.show()

#   温度的影响
# 画出温度和租车人数的散点图以及同温度下租车人数的平均值与温度的曲线图
average_temp_data = pd.DataFrame(columns=['temp', 'num', 'count', 'casual', 'registered'])
average_temp_lines = 0
for i in range(0, len(data)):

    index = data_find(average_temp_data['temp'], data['temp'][i])
    if index == -1:
        average_temp_data.loc[average_temp_lines] = [data['temp'][i], 1, data['count'][i], data['casual'][i],
                                                     data['registered'][i]]
        average_temp_lines += 1
    else:
        average_temp_data.loc[index] = [data['temp'][i], average_temp_data['num'].loc[index] + 1,
                                        data['count'][i] + average_temp_data['count'].loc[index],
                                        data['casual'][i] + average_temp_data['casual'].loc[index],
                                        data['registered'][i] + average_temp_data['registered'].loc[index]]
average_temp_data.sort_values(by='temp', axis=0, ascending=True, inplace=True)

fig = plt.figure(figsize=(12, 8))
# 创建一个子图，然后在子图上操作
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)
# ax1
ax1.scatter(data['temp'], data['count'], c="black", marker=".", alpha=0.2)
ax1.set_xlabel('温度')
ax1.set_ylabel('数量')
ax1.plot(average_temp_data['temp'], average_temp_data['count'] / average_temp_data['num'], c="black")
ax1.set_title('使用量与温度的散点图关系（一个温度包含多个数据）\n平均每小时使用量与温度的曲线关系')

# ax2
customers_index = [*average_temp_data['temp']]

customers_index = np.array(customers_index)

width = len(average_temp_data) * 0.008
rects1 = ax2.bar(customers_index, average_temp_data['count'], width=width / 2, color='gray',
                 label='所有用户')
rects2 = ax2.bar(customers_index - width / 2, average_temp_data['casual'], width=width / 2, color='lightgray',
                 label='未注册')
rects3 = ax2.bar(customers_index + width / 2, average_temp_data['registered'], width=width / 2, color='darkgray',
                 label='注册')

ax2.xaxis.set_ticks_position('bottom')
# 刻度线只显示在 y 轴 右侧。
ax2.yaxis.set_ticks_position('left')
ax2.plot(average_temp_data['temp'], average_temp_data['count'], c='black')
# 显示label 里面设置的图例
ax2.legend(title="类别",
           fontsize=16,
           title_fontsize=15,
           bbox_to_anchor=(0.25, 0.35))
ax2.set_title('温度影响（总数版）')
plt.show()

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
ax1.plot(average_time_data['time'], average_time_data['count'], c='black')
plt.show()

# 风速的影响
average_windspeed_data = pd.DataFrame(columns=['windspeed', 'num', 'count', 'casual', 'registered'])
average_windspeed_lines = 0


def float_int(float_num):  # 四舍五入函数
    if ((int(float_num * 10)) % 10) >= 5:
        return int(float_num) + 1
    else:
        return int(float_num)
wind_loss = 0;#记录缺失
for i in range(0, len(data)):
    if data['windspeed'][i] == 0:
        wind_loss +=1
        continue
    index = data_find(average_windspeed_data['windspeed'], float_int(data['windspeed'][i]))
    if index == -1:
        average_windspeed_data.loc[average_windspeed_lines] = [float_int(data['windspeed'][i]), 1, data['count'][i],
                                                               data['casual'][i],
                                                               data['registered'][i]]
        average_windspeed_lines += 1
    else:
        average_windspeed_data.loc[index] = [float_int(data['windspeed'][i]),
                                             average_windspeed_data['num'].loc[index] + 1,
                                             data['count'][i] + average_windspeed_data['count'].loc[index],
                                             data['casual'][i] + average_windspeed_data['casual'].loc[index],
                                             data['registered'][i] + average_windspeed_data['registered'].loc[index]]
average_windspeed_data.sort_values(by='windspeed', axis=0, ascending=True, inplace=True)

wind = np.array([*average_windspeed_data['windspeed']])
fig = plt.figure(figsize=(12, 8))
# 创建一个子图，然后在子图上操作
ax1 = fig.add_subplot(1, 1, 1)

k = ax1.bar(wind, average_windspeed_data['count'], width=0.5, color='ghostwhite')

rects1 = ax1.plot(average_windspeed_data['windspeed'], average_windspeed_data['count'], c='black', label='所有用户')
rects2 = ax1.plot(average_windspeed_data['windspeed'], average_windspeed_data['casual'], color='lightgray',
                  label='未注册用户')
rects3 = ax1.plot(average_windspeed_data['windspeed'], average_windspeed_data['registered'], c='gray', label='注册用户')
ax1.xaxis.set_ticks_position('bottom')
# 刻度线只显示在 y 轴 右侧。
ax1.yaxis.set_ticks_position('left')
# 显示label 里面设置的图例
ax1.legend(title="类别",
           fontsize=16,
           title_fontsize=15,
           bbox_to_anchor=(0.9, 0.35))
ax1.set_title('风速影响的折线图')
plt.show()

#   季节的影响
average_season_data = pd.DataFrame(columns=['season', 'num', 'count', 'casual', 'registered'])
season = ['春', '夏', '秋', '冬']
for i in range(0, 4):
    average_season_data.loc[i] = [i, 0, 0, 0, 0]
for i in range(0, len(data)):
    average_season_data.loc[data['season'].loc[i] - 1] = [data['season'].loc[i] - 1, average_season_data['num'].loc[data['season'].loc[i] - 1] +
                                                          1,data['count'][i] + average_season_data['count'].loc[data['season'].loc[i] - 1],
                                                          data['casual'][i] + average_season_data['casual'].loc[data['season'].loc[i] - 1],
                                                          data['registered'][i] + average_season_data['registered'].loc[
                                                              data['season'].loc[i] - 1]]


fig = plt.figure(figsize=(12, 8))
# 创建一个子图，然后在子图上操作
ax1 = fig.add_subplot(2, 1, 1)
customers_index = np.arange(len(season))
width = 0.3
rects1 = ax1.bar(customers_index, average_season_data['count'], width=width, align='center', color='black',
                 label='所有用户')
rects2 = ax1.bar(customers_index - width, average_season_data['casual'], width=width, align='center', color='lightgray',
                 label='未注册(左侧)')
rects3 = ax1.bar(customers_index + width, average_season_data['registered'], width=width, align='center', color='gray',
                 label='注册(右侧)')
ax1.bar_label(rects1, padding=3, **{'fontsize': 14})
ax1.bar_label(rects2, padding=3)
ax1.bar_label(rects3, padding=3)
ax1.xaxis.set_ticks_position('bottom')
# 刻度线只显示在 y 轴 右侧。
ax1.yaxis.set_ticks_position('left')
# 显示label 里面设置的图例
ax1.legend(title="类别",
           fontsize=16,
           title_fontsize=15,
           bbox_to_anchor=(1.01, 0.7))
# 设置 X轴刻度
ax1.set_xticks(customers_index)
# 设置 X轴刻度标签
ax1.set_xticklabels(season)
# 设置 X 轴标签，字体大小
ax1.xaxis.set_tick_params(labelsize=12)
# 设置 X轴标签
# Y 轴
ax1.yaxis.set_tick_params(which="both", labelsize=10)
ax1.set_ylabel('人数')
ax1.set_title('各季节下骑行总人数')
ax2 = fig.add_subplot(2, 1, 2)
ax2.bar(customers_index, average_season_data['count'] / average_season_data['num'], width=width, align='center',
        color='gray',label='all')

# 设置 X轴刻度
ax2.set_xticks(customers_index)
# 设置 X轴刻度标签
ax2.set_xticklabels(season)
ax2.xaxis.set_tick_params(labelsize=12)
# 设置 X轴标签
ax2.set_xlabel('季节', fontsize=15)
# Y 轴
ax2.yaxis.set_tick_params(which="both", labelsize=10)
ax2.set_ylabel('人数')
ax2.set_title('每个季节平均骑行总人数')
ax1.legend(title="类别",
           fontsize=16,
           title_fontsize=15,
           bbox_to_anchor=(0.1, 1.2))
plt.show()
