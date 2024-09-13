import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.animation import FuncAnimation
import matplotlib.patches as plt_patches
import matplotlib
from matplotlib import font_manager
import datetime

from mysql import connection

font_manager.fontManager.addfont('font/SimHei.ttf')
matplotlib.rc('font', family='SimHei')

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
]


def get_area_data_list(area_name):
  with connection.cursor() as cursor:
    # 查询并打印结果以验证数据插入成功
    cursor.execute(
      'SELECT area_name, series, series_timestamp, fl_month_sale FROM lottery WHERE area_name = %s order by series_timestamp desc limit 132',
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
          'group': row['area_name'],
          'year': date.strftime('%Y%m'),
          'value': total,
        }
      )

    return dict_list


dict_list = []
for area_name in area_list:
  dict_list += get_area_data_list(area_name)
df = pd.DataFrame.from_dict(dict_list)
connection.close()

# 设置最多显示城市数量
max_range = 10
title = '中国福利彩票事业TOP10省市'


# 定义一个函数，用于生成颜色列表
def generate_colors(string_list):
  num_colors = len(string_list)
  # 使用tab10调色板，可以根据需要选择不同的调色板
  colormap = plt.get_cmap('tab10', num_colors)

  colors = []
  for i in range(num_colors):
    color = colormap(i)
    colors.append(color)

  return colors


# 将年份列转换为整数型
df['year'] = df['year'].astype(int)
# 将人口数量列转换为浮点型
df['value'] = df['value'].astype(float)

# 获取城市分组列表
group = list(set(df.group))

# 生成城市分组对应的颜色字典
group_color = dict(zip(group, generate_colors(group)))

# 创建城市名称与分组的字典
group_name = df.set_index('name')['group'].to_dict()


# 定义绘制柱状图的函数
def draw_bar_chart(year):
  # 根据年份筛选数据，并按人口数量进行降序排序，取出最大范围的数据
  df_year = (
    df[df['year'].eq(year)]
    .sort_values(by='value', ascending=True)
    .tail(max_range)
  )

  ax.clear()
  # 绘制水平柱状图，并设置颜色
  ax.barh(
    df_year['name'],
    df_year['value'],
    color=[group_color[group_name[x]] for x in df_year['name']],
  )

  # 在柱状图上方添加文字标签
  dx = df_year['value'].max() / 200
  for i, (value, name) in enumerate(zip(df_year['value'], df_year['name'])):
    # 城市名
    # ax.text(value - dx, i, name, size=32, weight=600, ha='right', va='bottom')
    ax.text(
      value - dx,
      i - 0.25,
      group_name[name],
      size=40,
      color='#333333',
      ha='right',
      va='baseline',
    )
    # 地区名
    ax.text(value + dx, i, f'{value:,.0f}', size=40, ha='left', va='center')

  # 设置其他样式
  ax.text(
    1,
    0.2,
    year,
    transform=ax.transAxes,
    color='#777777',
    size=46,
    ha='right',
    weight=800,
  )
  ax.text(
    0,
    1.06,
    '金额 (亿元)',
    transform=ax.transAxes,
    size=40,
    color='#777777',
  )
  # 添加图例
  handles = []
  for name, color in group_color.items():
    patch = plt_patches.Patch(color=color, label=name)
    handles.append(patch)
  ax.legend(
    handles=handles,
    fontsize=40,
    loc='center',
    bbox_to_anchor=(0.5, -0.03),
    ncol=len(group_color),
    frameon=False,
  )

  # x轴的主要刻度格式化，不保留小数
  ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
  # 将x轴的刻度位置设置在图的顶部
  ax.xaxis.set_ticks_position('top')
  # 设置x轴的刻度颜色为灰色(#777777)，字体大小为16
  ax.tick_params(axis='x', colors='#777777', labelsize=16)
  # 清除y轴的刻度标签
  ax.set_yticks([])
  # 在x轴和y轴上设置0.01的边距
  ax.margins(0, 0.01)
  # 在x轴上绘制主要网格线，线条样式为实线
  ax.grid(which='major', axis='x', linestyle='-')
  # 设置网格线绘制在图像下方
  ax.set_axisbelow(True)

  # 添加绘图信息
  ax.text(
    0,
    1.10,
    f'{title}',
    transform=ax.transAxes,
    size=48,
    weight=600,
    ha='left',
  )

  ax.text(
    1,
    0,
    'Produced by AlfieriChou',
    transform=ax.transAxes,
    ha='right',
    color='#777777',
    size=24,
    bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'),
  )
  plt.box(False)


# 创建绘图所需的figure和axes
fig, ax = plt.subplots(figsize=(32, 18))
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示汉字
plt.rcParams['axes.unicode_minus'] = False

year_list = list(set(df.year))
year_list.sort()
start_year = min(year_list)
end_year = max(year_list)

# 获取数据中的最小年份和最大年份，并进行校验
min_year, max_year = min(set(df.year)), max(set(df.year))
assert min_year <= start_year, f'end_year cannot be lower than {min_year}'
assert end_year <= max_year, f'end_year cannot be higher  than {max_year}'

# 创建动画对象，调用draw_bar_chart函数进行绘制
ani = FuncAnimation(
  fig,
  draw_bar_chart,
  frames=year_list,
  repeat_delay=1000,
  interval=200,
)
fig.subplots_adjust(left=0.04, right=0.94, bottom=0.05)

# 显示图形
# plt.show()
ani.save(filename='video/east_south_animation.mp4', writer='ffmpeg')

# ffmpeg -i music.mp3 music.wav
# ffmpeg -i music.wav -ss 0 -t 37 musicshort.wav
# ffmpeg -i musicshort.wav -i east_south_animation.mp4 output.mp4
