from libs.lottery import download_lottery_by_page

total_page = 29
page = 1

while page < total_page:
  download_lottery_by_page(page)
  page += 1
