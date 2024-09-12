import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.animation import FuncAnimation
import matplotlib.patches as mpatches
import matplotlib
from matplotlib import font_manager
import datetime

from mysql import connection

font_manager.fontManager.addfont('font/SimHei.ttf')
matplotlib.rc('font', family='SimHei')


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
      total += float(format(row['fl_month_sale'] / 100, '.2f'))
      dict_list.append(
        {
          'name': row['area_name'],
          'group': row['area_name'],
          'year': date.strftime('%Y%m'),
          'value': total,
        }
      )

    return dict_list

js_area_list = get_area_data_list('江苏')
sd_area_list = get_area_data_list('山东')
gd_area_list = get_area_data_list('广东')
zj_area_list = get_area_data_list('浙江')
fj_area_list = get_area_data_list('福建')
dict_list = js_area_list + sd_area_list + gd_area_list + zj_area_list + fj_area_list
df = pd.DataFrame.from_dict(dict_list)
connection.close()


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
def draw_barchart(year):
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
    ax.text(value - dx, i, name, size=12, weight=600, ha='right', va='bottom')
    ax.text(
      value - dx,
      i - 0.25,
      group_name[name],
      size=10,
      color='#333333',
      ha='right',
      va='baseline',
    )
    # 地区名
    ax.text(value + dx, i, f'{value:,.0f}', size=12, ha='left', va='center')

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
    size=12,
    color='#777777',
  )
  # 添加图例
  handles = []
  for name, color in group_color.items():
    patch = mpatches.Patch(color=color, label=name)
    handles.append(patch)
  ax.legend(
    handles=handles,
    fontsize=12,
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
    f'东南沿海五省福利彩票11年销售数据统计',
    transform=ax.transAxes,
    size=24,
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
    bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'),
  )
  plt.box(False)


# 创建绘图所需的figure和axes
fig, ax = plt.subplots(figsize=(12, 8))
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示汉字
plt.rcParams['axes.unicode_minus'] = False

year_list = list(set(df.year))
year_list.sort()
start_year = min(year_list)
end_year = max(year_list)

# 设置最多显示城市数量
max_range = 5

# 获取数据中的最小年份和最大年份，并进行校验
min_year, max_year = min(set(df.year)), max(set(df.year))
assert min_year <= start_year, f'end_year cannot be lower than {min_year}'
assert end_year <= max_year, f'end_year cannot be higher  than {max_year}'

# 创建动画对象，调用draw_barchart函数进行绘制
ani = FuncAnimation(
  fig,
  draw_barchart,
  frames=year_list,
  repeat_delay=1000,
  interval=200,
)
fig.subplots_adjust(left=0.04, right=0.94, bottom=0.05)

# 显示图形
# plt.show()
ani.save(filename="video/east_south_animation.mp4", writer="ffmpeg")

# ffmpeg -i video.mp4 -i audio.wav -map 0:v -map 1:a -c:v copy -shortest output.mp4
