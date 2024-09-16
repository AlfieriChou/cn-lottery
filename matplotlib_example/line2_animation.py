from matplotlib.lines import Line2D  # for legend
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
from matplotlib import font_manager
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
      # total += float(format(row['fl_month_sale'] / 10000, '.2f'))
      dict_list.append(
        {
          'name': row['area_name'],
          'date': date.strftime('%Y%m'),
          'value': float(format(row['fl_month_sale'] / 10000, '.2f')),
        }
      )

    return dict_list


fig = plt.figure(figsize=(32, 18))
ax = fig.add_subplot(111)

area_name_1 = '广东'
area_name_2 = '浙江'
dict_list_1 = get_series_data_list(area_name_1)
dict_list_2 = get_series_data_list(area_name_2)

data = pd.DataFrame.from_dict((dict_list_1 + dict_list_2))

print(data)

def animate(i):
  # create a color dict for each name
  cd = dict(zip(data.name.unique(), ['tab:blue', 'tab:orange']))

  # select each name group and plot with a different color
  for name in data.name.unique():
    data_name = data[data.name.eq(name)]

    temp = data_name.iloc[: 1 + int(i)]  # select temp range
    ax.plot(temp['date'], temp['value'], color=cd[name])

  # create custom legend lines
  custom_lines = [
    Line2D([0], [0], color=v, lw=2, label=k) for k, v in cd.items()
  ]

  ax.legend(title='name', handles=custom_lines)


Writer = animation.writers['ffmpeg']

# increase the frame rate
writer = Writer(fps=30, metadata=dict(artist='Me'), bitrate=1800)
fig = plt.figure()
ax = fig.add_subplot()

# frames is the length of the data / 3 because there are 3 name groups
ani = animation.FuncAnimation(
  fig, animate, frames=int(len(data) / 3), repeat=False
)

ani.save('video/test.mp4', writer=writer)
