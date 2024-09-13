import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
from matplotlib import font_manager
import numpy as np
import datetime

from mysql import connection

font_manager.fontManager.addfont('font/SimHei.ttf')
matplotlib.rc('font', family='SimHei')

def get_series_data_list(area_name):
  with connection.cursor() as cursor:
    # 查询并打印结果以验证数据插入成功
    cursor.execute(
      'SELECT area_name, series, series_timestamp, fl_month_sale FROM lottery WHERE area_name = %s order by series_timestamp desc limit 133',
      (area_name),
    )

    data_list = cursor.fetchall()
    data_list.reverse()
    dict_list = []
    total = 0
    for row in data_list:
      date = datetime.datetime.fromtimestamp(row['series_timestamp'])
      total += float(format(row['fl_month_sale'] / 10000, '.2f'))
      dict_list.append(
        {
          'name': row['area_name'],
          'date': date.strftime('%Y%m'),
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

x =[]
y1 = []
y2 = []

for dict_info in dict_list_1:
  x.append(dict_info['date'])
  y1.append(dict_info['value'])

for dict_info in dict_list_2:
  y2.append(dict_info['value'])

(line1,) = ax.plot([], [], 'b', label=area_name_1)
(line2,) = ax.plot([], [], 'r', label=area_name_2)
ax.legend()
total = len(x)
min_x = min(x)
max_x = max(x)
max_y1 = max(y1)
max_y2 = max(y2)


def update_params(i):
  ax.set_ylim(0, max(max_y1, max_y2) * 1.2)
  ax.set_xlim(min_x, max_x)
  # 同时更新line1和line2参数
  line1.set_data(x[:i], y1[:i])
  line2.set_data(x[:i], y2[:i])
  return line1, line2


ani = FuncAnimation(fig, update_params, total, interval=100, blit=True)

ani.save(filename='video/line_animation.mp4', writer='ffmpeg')
