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

def generate_pie(series, area_code):
  filepath = 'img/pie_' + series + '_' + area_code + '.png'
  try:
    with connection.cursor() as cursor:
      # 查询并打印结果以验证数据插入成功
      cursor.execute("SELECT series, area_code, area_name, fl_month_sale, sport_month_sale FROM lottery WHERE series = %s and area_code = %s", (series, area_code))

      y = []
      rows = cursor.fetchall()
      row = rows[0]
      y.append(row['fl_month_sale'])
      y.append(row['sport_month_sale'])

      plt.title('彩票销售排名_' + series + '_' + row['area_name'])  # 折线图标题
      plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示汉字
      plt.rcParams['axes.unicode_minus'] = False

      y = np.array(y)
            
      plt.pie(y,
        labels=['福利彩票月销售额','体育彩票月销售额'], # 设置饼图标签
        colors=["#d5695d", "#5d8ca8"], # 设置饼图颜色
        explode=(0.2, 0), # 第一部分突出显示，值越大，距离中心越远
        autopct='%.2f%%', # 格式化输出百分比
      )

      plt.savefig(filepath, dpi=300)  # save the figure to file
      plt.close()

  finally:
    print('matplotlib pie image done: ', series, area_code)


generate_pie('2024年7月', '01')
connection.close()
