import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager
import numpy as np

from mysql import connection

# 设置matplotlib后台执行
matplotlib.use('agg')
font_manager.fontManager.addfont('font/SimHei.ttf')
matplotlib.rc('font', family='SimHei')

def generate_line_chart(area_name):
  filepath = 'img/line_' + area_name + '.png'
  try:
    with connection.cursor() as cursor:
      # 查询并打印结果以验证数据插入成功
      cursor.execute("SELECT area_name, series, fl_month_sale FROM lottery WHERE area_name = %s order by series asc limit 24", (area_name))

      x = []
      y = []
      for row in cursor.fetchall():
        x.append(row['series'])
        y.append(row['fl_month_sale'])

      plt.figure(figsize=(14, 6))  # 设置画布大小
      
      x = np.array(x)
      y = np.array(y)

      plt.figure(figsize=(14, 6))  # 设置画布大小
      plt.title('彩票趋势_' + area_name)  # 折线图标题
      plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示汉字
      plt.rcParams['axes.unicode_minus'] = False
      plt.xlabel('时间')  # x轴标题
      plt.ylabel('值')  # y轴标题
      plt.plot(
        x, y, marker='o', markersize=3
      )  # 绘制折线图，添加数据点，设置点的大小
      for a, b in zip(x, y):
        plt.text(
          a, b, b, ha='center', va='bottom', fontsize=10
        )  # 设置数据标签位置及大小
      # plt.legend(['最高价'])  # 设置折线名称
      plt.savefig(filepath, dpi=300)  # save the figure to file
      plt.close()

  finally:
    print('matplotlib bar image done: ', area_name)


generate_line_chart('北京')
connection.close()
