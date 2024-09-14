import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
from matplotlib import font_manager
import datetime

from mysql import connection

font_manager.fontManager.addfont('font/SimHei.ttf')
matplotlib.rc('font', family='SimHei')
china = gpd.read_file('geo/china_v1.json')
area_list = [
  '北京',
  '天津',
  '河北',
  '山西',
  '内蒙古',
  '辽宁',
  '吉林',
  '黑龙江',
  '上海',
  '江苏',
  '浙江',
  '安徽',
  '福建',
  '江西',
  '山东',
  '河南',
  '湖北',
  '湖南',
  '广东',
  '广西',
  '海南',
  '重庆',
  '四川',
  '贵州',
  '云南',
  '西藏',
  '陕西',
  '甘肃',
  '青海',
  '宁夏',
  '新疆',
  '台湾省',
  '香港特别行政区',
  '澳门特别行政区',
]
provinces = area_list
dates = []

def get_area_data_list(area_name):
  with connection.cursor() as cursor:
    # 查询并打印结果以验证数据插入成功
    cursor.execute(
      'SELECT area_name, series, series_timestamp, fl_month_sale FROM lottery WHERE area_name = %s order by series_timestamp desc limit 132',
      (area_name),
    )
    data_list = cursor.fetchall()
    if len(data_list) == 0:
      return []
    data_list.reverse()
    dict_list = []
    for row in data_list:
      date = datetime.datetime.fromtimestamp(row['series_timestamp'])
      date_str = date.strftime('%Y年%m月')
      if date_str not in dates:
        dates.append(date_str)
      dict_list.append(
        {
          'name': row['area_name'],
          'group': row['area_name'],
          'date': date_str,
          'value': float(format(row['fl_month_sale'] / 10000, '.2f')),
        }
      )

    return dict_list


dict_list = []
for area_name in area_list:
  if area_name in ['台湾省', '香港特别行政区', '澳门特别行政区']:
    dict_list_1 = []
    for date in dates:
      dict_list_1.append(
        {
          'name': area_name,
          'group': area_name,
          'date': date,
          'value': 0
        }
      )
    dict_list += dict_list_1
    continue
  dict_list += get_area_data_list(area_name)
df0 = pd.DataFrame.from_dict(dict_list)
connection.close()

china_w_needed_provinces = china[china.name.isin(provinces)]

df = pd.DataFrame(
  {
    'date': df0['date'].tolist(),
    'province': df0['name'].tolist(),
    'value': df0['value'].tolist(),
  }
)

fig, ax = plt.subplots(figsize=(16, 9))
fontsize = 8

ims = []
t = []
dates = df['date'].unique()
vmin, vmax = df['value'].min(), df['value'].max()


def update_fig(i):
  if len(ims) > 0:
    del ims[0]
  geos = china_w_needed_provinces['geometry']
  value = df[df['date'] == dates[i]]['value'].tolist()
  print(geos, value)
  artist = gpd.plotting._plot_polygon_collection(ax, geos, value, cmap='Reds')
  ims.append(artist)
  # ax.text(20, 45, 'Date:\n{}'.format(dates[i]), fontsize=fontsize, horizontalalignment='center')
  for lon, lat, province in zip(
    china_w_needed_provinces.lon,
    china_w_needed_provinces.lat,
    china_w_needed_provinces.name,
  ):
    ax.text(lon, lat, province, fontsize=fontsize)
  ax.set_title('福利彩票月销售数据 {} - {} 单位：（亿元）'.format(dates[0], dates[i]))
  ax.set_axis_off()
  fig = ax.get_figure()
  cax = fig.add_axes([0.9, 0.1, 0.03, 0.8])
  sm = plt.cm.ScalarMappable(
    cmap='Reds', norm=plt.Normalize(vmin=vmin, vmax=vmax)
  )
  # fake up the array of the scalar mappable. Urgh...
  sm._A = []
  fig.colorbar(sm, cax=cax)
  return ims


anim = FuncAnimation(
  fig,
  update_fig,
  interval=1000,
  repeat_delay=300,
  frames=len(df['date'].unique()),
)

# plt.show()
anim.save(filename='video/map_animation.mp4', writer='ffmpeg')

