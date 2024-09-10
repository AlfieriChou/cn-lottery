import time

from libs.lottery import (
  download_lottery_by_page,
  read_lottery_xlsx,
  write_lottery_list_to_db,
)
from libs.mysql import connection

total_page = 29
page = 1

while page < total_page:
  download_dict = download_lottery_by_page(page)
  print('[DOWNLOAD-LIST]: ', page, download_dict)
  for series, xlsx_path in download_dict.items():
    print('[READ-LIST]: ', series, xlsx_path)
    list = read_lottery_xlsx(series, xlsx_path)
    if len(list) > 0:
      write_lottery_list_to_db(series, list, connection)
    time.sleep(1)
  time.sleep(5)
  page += 1

connection.close()
