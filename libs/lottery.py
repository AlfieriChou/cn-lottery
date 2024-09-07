from bs4 import BeautifulSoup
from libs.html import get_html
import urllib.request

base_url = 'https://zhs.mof.gov.cn'


def get_lottery_list_url(page):
  lottery_url = base_url + '/zonghexinxi/'
  if page > 0:
    lottery_url = base_url + '/zonghexinxi/index_' + str(page) + '.htm'
  return lottery_url


def download_lottery_by_page(page):
  download_list = []
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
      # 2017年3月的数据结构不同，td->ol->a
      if '2017年3月份全国彩票销售情况' in title:
        soup = BeautifulSoup(get_html(href), 'html.parser')
        ol = soup.find_all('ol')[0]
        download_a = ol.a
        download_href = download_a.get('href')
        download_url = base_url + '/zonghexinxi/201704/' + download_href[2:]
        print(href, title, download_url)
        download_path = 'xlsx/' + download_href[2:]
        urllib.request.urlretrieve(download_url, download_path)
        download_list.append(download_path)
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
      download_list.append(download_path)

  return download_list
