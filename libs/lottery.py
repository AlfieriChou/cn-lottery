from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import re
import pyexcel as p

from libs.html import get_html
from libs.area import area_dict, area_list
from libs.md5 import md5

base_url = 'https://zhs.mof.gov.cn'


def Not_none(n):
  if n != None:
    return n


def get_title_exp_time(link_title):
  time = list(
    filter(
      Not_none,
      [
        re.search(r'\d{4}年\d{1}月', link_title),
        re.search(r'\d{4}年\d{2}月', link_title),
        re.search(r'\d{4}年第\d{1}期', link_title),
      ],
    )
  )[0]
  return time


def get_lottery_list_url(page):
  lottery_url = base_url + '/zonghexinxi/'
  if page > 0:
    lottery_url = base_url + '/zonghexinxi/index_' + str(page) + '.htm'
  return lottery_url


def download_lottery_by_page(page):
  download_dict = {}
  lottery_url = get_lottery_list_url(page - 1)
  soup = BeautifulSoup(get_html(lottery_url), 'html.parser')
  ul_list = soup.find_all('ul', class_='liBox')
  for ul in ul_list:
    li_list = ul.find_all('li')
    for li in li_list:
      a = li.a
      href = a.get('href')
      title = a.get('title').encode('iso-8859-1').decode('UTF-8')
      if '彩票销售情况' not in title:
        continue
      time = get_title_exp_time(title)
      series = time.group()
      # 2017年3月的数据结构不同，td->ol->a
      if '2017年3月份全国彩票销售情况' in title:
        soup = BeautifulSoup(get_html(href), 'html.parser')
        ol = soup.find_all('ol')[0]
        download_a = ol.a
        download_href = download_a.get('href')
        download_url = 'https://www.mof.gov.cn/gp/xxgkml/zhs/201704/P020170419592005376814.xlsx'
        print(href, title, download_url)
        download_path = 'xlsx/' + download_href[2:]
        urllib.request.urlretrieve(download_url, download_path)
        download_dict[series] = download_path
        continue
      soup = BeautifulSoup(
        get_html(base_url + '/zonghexinxi/' + href[2:]), 'html.parser'
      )
      span = soup.find(id='appendix1')
      if span is None:
        continue
      download_a = span.a
      download_href = download_a.get('href')
      download_url = (
        base_url + '/zonghexinxi/' + href[2:8] + '/' + download_href[2:]
      )
      print(href, title, download_url)
      download_path = 'xlsx/' + download_href[2:]
      urllib.request.urlretrieve(download_url, download_path)
      download_dict[series] = download_path

  return download_dict


def read_lottery_xlsx(series, xlsx_path):
  list = []
  # 暂不支持解析xls文件
  if xlsx_path.endswith('.xls') is True:
    p.save_book_as(file_name=xlsx_path, dest_file_name=xlsx_path + 'x')
  dfs = pd.read_excel(xlsx_path, sheet_name=None)
  for sheet_name, value in dfs.items():
    if '各地区彩票销售情况' in sheet_name or 'Sheet3' in sheet_name:
      for index, row in value.iterrows():
        lottery_list = row.to_list()
        if series in ['2021年4月', '2021年3月', '2021年2月']:
          lottery_list.insert(2, 0)
          lottery_list.insert(4, 0)
          lottery_list.insert(6, 0)
          lottery_list.insert(8, 0)
          lottery_list.insert(10, 0)
          lottery_list.insert(12, 0)
        if lottery_list[0] not in area_list:
          continue
        area_code = area_dict[lottery_list[0]]
        lottery_list.insert(0, area_code)
        lottery_list.insert(0, series)
        id = series + area_code
        encode_id = md5(id)
        lottery_list.insert(0, encode_id)
        print(xlsx_path, index, lottery_list)
        list.append(lottery_list)

  return list


def write_lottery_list_to_db(series, list, connection):
  try:
    with connection.cursor() as cursor:
      # 创建表（如果尚未存在）
      cursor.execute("""
      CREATE TABLE IF NOT EXISTS lottery (
        id VARCHAR(64) PRIMARY KEY,
        series VARCHAR(64) NOT NULL,
        area_code VARCHAR(32) NOT NULL,
        area_name VARCHAR(32) NOT NULL,
        fl_month_sale DECIMAL(10, 3) NOT NULL,
        fl_month_on_year_growth_rate DECIMAL(10, 3) NOT NULL,
        fl_year_sale DECIMAL(10, 3) NOT NULL,
        fl_year_on_year_growth_rate DECIMAL(10, 3) NOT NULL,
        sport_month_sale DECIMAL(10, 3) NOT NULL,
        sport_month_on_year_growth_rate DECIMAL(10, 3) NOT NULL,
        sport_year_sale DECIMAL(10, 3) NOT NULL,
        sport_year_on_year_growth_rate DECIMAL(10, 3) NOT NULL,
        total_month_sale DECIMAL(10, 3) NOT NULL,
        total_month_on_year_growth_rate DECIMAL(10, 3) NOT NULL,
        total_year_sale DECIMAL(10, 3) NOT NULL,
        total_year_on_year_growth_rate DECIMAL(10, 3) NOT NULL,
        INDEX idx_id (id),
        INDEX idx_series (series),
        INDEX idx_area_code (area_code),
        INDEX idx_area_name (area_name),
        INDEX idx_fl_month_sale (fl_month_sale),
        INDEX idx_fl_month_on_year_growth_rate (fl_month_on_year_growth_rate),
        INDEX idx_fl_year_sale (fl_year_sale),
        INDEX idx_fl_year_on_year_growth_rate (fl_year_on_year_growth_rate),
        INDEX idx_sport_month_sale (sport_month_sale),
        INDEX idx_sport_month_on_year_growth_rate (sport_month_on_year_growth_rate),
        INDEX idx_sport_year_sale (sport_year_sale),
        INDEX idx_sport_year_on_year_growth_rate (sport_year_on_year_growth_rate),
        INDEX idx_total_month_sale (total_month_sale),
        INDEX idx_total_month_on_year_growth_rate (total_month_on_year_growth_rate),
        INDEX idx_total_year_sale (total_year_sale),
        INDEX idx_total_year_on_year_growth_rate (total_year_on_year_growth_rate)
      )
      """)

      # 插入数据
      # 构建INSERT语句
      insert_query = """
        INSERT IGNORE INTO lottery (
          id,
          series,
          area_code,
          area_name,
          fl_month_sale,
          fl_month_on_year_growth_rate,
          fl_year_sale,
          fl_year_on_year_growth_rate,
          sport_month_sale,
          sport_month_on_year_growth_rate,
          sport_year_sale,
          sport_year_on_year_growth_rate,
          total_month_sale,
          total_month_on_year_growth_rate,
          total_year_sale,
          total_year_on_year_growth_rate
        ) VALUES (
          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
      """

      # 构建并执行多个插入语句
      for row in list:
        # 执行INSERT语句
        cursor.execute(insert_query, row)

      connection.commit()

  finally:
    print('write lottery list done: ', series)
