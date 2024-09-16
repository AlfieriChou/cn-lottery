# X轴动态更新
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# 创建日期数据
start_date = datetime(2024, 1, 1)
x_data = [start_date + timedelta(days=i) for i in range(500)]  # 生成500天的日期
y1_data = np.sin(np.linspace(0, 10 * np.pi, len(x_data)))
y2_data = np.cos(np.linspace(0, 10 * np.pi, len(x_data)))

# 初始化画布
fig, ax = plt.subplots()
ax.set_ylim(-1.5, 1.5)

# 窗口宽度设定，表示显示固定天数
window_width = timedelta(days=50)  # 显示50天的区间

# 初始化两条空线条对象
line1, = ax.plot([], [], label="sin(x)", color='b')
line2, = ax.plot([], [], label="cos(x)", color='r')

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

# 更新函数，每次调用会更新曲线的数据，并动态调整x轴
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
    
    return line1, line2

# 创建动画，interval 设置每帧之间的间隔时间（毫秒）
ani = FuncAnimation(fig, update, frames=len(x_data), init_func=init, blit=True, interval=50)

# 显示动画
# plt.show()
ani.save(filename='video/test.mp4', writer='ffmpeg')

