import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
from matplotlib import font_manager
import pandas as pd

from mysql import connection

font_manager.fontManager.addfont('font/SimHei.ttf')
matplotlib.rc('font', family='SimHei')


def get_series_data_list(series):
  with connection.cursor() as cursor:
    # 查询并打印结果以验证数据插入成功
    cursor.execute(
      'SELECT area_name, area_code, fl_month_sale FROM lottery WHERE series = %s order by fl_month_sale desc',
      (series),
    )

    data_list = cursor.fetchall()
    data_list.reverse()
    dict_list = []
    total = 0
    for row in data_list:
      dict_list.append(
        {
          'name': row['area_name'],
          'value': float(format(row['fl_month_sale'] / 10000, '.2f')),
        }
      )

    return dict_list


series_dict_list = get_series_data_list('2024年7月')
connection.close()

fig, ax = plt.subplots()
# # 创建一个数组，表示数据集
data = []
# 创建一个字符串的列表，表示数据集的标签
x = []

# 创建一个空列表，用于存储图形对象
artists = []
# 创建一个包含5个颜色值的列表，用于绘制图形
colors = ['tab:blue', 'tab:red', 'tab:green', 'tab:purple', 'tab:orange']

for series_dict in series_dict_list:
  # 随机生成一个与data形状相同的数组，并将其加到data中
  data.append(series_dict['value'])
  x.append(series_dict['name'])
  # 创建一个水平条形图，并设置颜色
  container = ax.barh(x, data, color=colors)
  # 设置x轴范围
  ax.set_xlim(0, 20)
  # 将创建的图形对象添加到列表中
  artists.append(container)

# 创建一个ArtistAnimation对象，指定图形窗口和图形对象列表以及动画间隔时间
ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=500)
plt.show()
