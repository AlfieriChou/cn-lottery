# X轴和Y轴都动态更新
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import matplotlib
from matplotlib import font_manager

from mysql import connection

font_manager.fontManager.addfont('font/SimHei.ttf')
matplotlib.rc('font', family='SimHei')

def get_series_data_list(area_name):
  with connection.cursor() as cursor:
    # 查询并打印结果以验证数据插入成功
    cursor.execute(
      'SELECT area_name, series, series_timestamp, fl_month_sale FROM lottery WHERE area_name = %s order by series_timestamp desc limit 134',
      (area_name),
    )

    data_list = cursor.fetchall()
    data_list.reverse()
    dict_list = []
    total = 0
    for row in data_list:
      date = datetime.fromtimestamp(row['series_timestamp'])
      total += float(format(row['fl_month_sale'] / 10000, '.2f'))
      dict_list.append(
        {
          'name': row['area_name'],
          'date': date,
          'value': total,
        }
      )

    return dict_list


fig = plt.figure(figsize=(32, 18))
ax = fig.add_subplot(111)

area_name_1 = '广东'
area_name_2 = '浙江'
dict_list_1 = get_series_data_list(area_name_1)
dict_list_2 = get_series_data_list(area_name_2)

# 创建日期数据
x_data = []
y1_data = []
y2_data = []
for dict_info in dict_list_1:
  x_data.append(dict_info['date'])
  y1_data.append(dict_info['value'])
for dict_info in dict_list_2:
  y2_data.append(dict_info['value'])

# 初始化画布
fig, ax = plt.subplots()

plt.rcParams['axes.unicode_minus'] = False

# 窗口宽度设定，表示显示固定天数
window_width = timedelta(days=200)  # 显示50天的区间

# 初始化两条空线条对象
line1, = ax.plot([], [], label=area_name_1, color='b')
line2, = ax.plot([], [], label=area_name_2, color='r')

# 设置日期格式的x轴
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # 显示格式为年月日
ax.xaxis.set_major_locator(mdates.AutoDateLocator())  # 自动设置日期刻度

# 设置图例
ax.legend()

# 初始化函数，清空线条数据
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    ax.set_xlim(x_data[0], x_data[0] + window_width)  # 设置初始的x轴范围
    return line1, line2

# 更新函数，每次调用会更新曲线的数据，并动态调整x轴和y轴
def update(frame):
    # 截取到当前帧的 x 和 y 数据
    line1.set_data(x_data[:frame], y1_data[:frame])
    line2.set_data(x_data[:frame], y2_data[:frame])
    
    # 动态调整x轴的范围，使其随着frame滑动
    current_x_max = x_data[frame]
    current_x_min = current_x_max - window_width
    
    # 更新 x 轴的显示范围
    ax.set_xlim(current_x_min, current_x_max)
    
    # 实时更新x轴的刻度
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # 格式化日期
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())  # 自动调整刻度
    fig.autofmt_xdate()  # 自动旋转日期标签避免重叠
    
    # 动态更新y轴的范围，但先确保数据不为空
    if frame > 0:
        y_data_combined = np.concatenate([y1_data[:frame], y2_data[:frame]])  # 获取当前帧的所有y值
        y_min, y_max = np.min(y_data_combined), np.max(y_data_combined)  # 计算最小和最大值
        padding = 0.1 * (y_max - y_min)  # 设置10%的padding避免图线贴边
        ax.set_ylim(y_min - padding, y_max + padding)  # 动态更新y轴范围
    
    return line1, line2

# 创建动画，interval 设置每帧之间的间隔时间（毫秒）
ani = FuncAnimation(fig, update, frames=len(x_data), init_func=init, blit=True, interval=300)

# 显示动画
ani.save(filename='video/test.mp4', writer='ffmpeg')

