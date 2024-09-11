# cn-lottery
Synchronize Chinese lottery data

## 说明

同步民政部彩票公开数据，将xlsx下载到本地，解析xlsx数据到数据库


## 已实现功能

* 读取页面获取周期下载数据路径
* 下载xlsx到本地
* 如果当前下载的文件后缀是xls，先转成xlsx文件
* 读取xlsx各地区彩票销售情况数据
* 整理结构写入数据库留存


## 如何使用

1. 更改env.py的mysql数据库配置

```
touch env.py
```

2. 安装依赖包

```
make install
```

3. 命令行启动同步任务（暂未添加失败重试逻辑，如遇接口异常，重新同步）

```
python3 main.py
```
