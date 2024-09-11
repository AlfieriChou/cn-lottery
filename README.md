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
