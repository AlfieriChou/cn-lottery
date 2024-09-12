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

def generate_bar(series):
  filepath = 'img/bar_' + series + '.png'
  try:
    with connection.cursor() as cursor:
      # 查询并打印结果以验证数据插入成功
      cursor.execute("SELECT area_name, area_code, fl_month_sale FROM lottery WHERE series = %s order by fl_month_sale desc", (series))

      x = []
      y = []
      for row in cursor.fetchall():
        x.append(row['area_name'])
        y.append(row['fl_month_sale'])

      plt.figure(figsize=(14, 6))  # 设置画布大小

      plt.title('彩票销售排名_' + series)  # 折线图标题
      plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示汉字
      plt.rcParams['axes.unicode_minus'] = False

      plt.xlabel('省市')  # x轴标题
      plt.ylabel('值')  # y轴标题
      
      x = np.array(x)
      y = np.array(y)

      plt.bar(x, y)

      plt.savefig(filepath, dpi=300)  # save the figure to file
      plt.close()

  finally:
    print('matplotlib bar image done: ', series)


generate_bar('2024年7月')
connection.close()
