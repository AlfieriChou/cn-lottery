from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import re

from libs.html import get_html
from libs.area import area_dict, area_list

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
  lottery_url = get_lottery_list_url(page)
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
      series_name = time.group()
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
        download_dict[series_name] = download_path
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
      download_dict[series_name] = download_path

  return download_dict

def read_lottery_xlsx(series_name, xlsx_path):
  list = []
  # 暂不支持解析xls文件
  if xlsx_path.endswith('.xls') is True:
    return list
  dfs = pd.read_excel(xlsx_path, sheet_name=None)
  for sheet_name, value in dfs.items():
    if '各地区彩票销售情况' in sheet_name or 'Sheet3' in sheet_name:
      for index, row in value.iterrows():
        lottery_list = row.to_list()
        if lottery_list[0] not in area_list:
          continue
        lottery_list.insert(0, area_dict[lottery_list[0]])
        lottery_list.insert(0, series_name)
        print(xlsx_path, index, lottery_list)
        list.append(lottery_list)

  return list
