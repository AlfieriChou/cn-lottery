import time

from libs.lottery import download_lottery_by_page, read_lottery_xlsx

total_page = 29
page = 1

while page < total_page:
  download_dict = download_lottery_by_page(page)
  print('[DOWNLOAD-LIST]: ', page, download_dict)
  for series_name, xlsx_path in download_dict.items():
    print('[READ-LIST]: ', series_name, xlsx_path)
    read_lottery_xlsx(series_name, xlsx_path)
    time.sleep(1)
  time.sleep(5)
  page += 1
