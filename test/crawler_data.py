import requests
import bs4
import pandas as pd
import re
from fake_useragent import UserAgent



base_url = 'https://www.ptt.cc'
sub_url = '/bbs/Gossiping/index.html'
ua = UserAgent()
user_agent = ua.random
my_headers = {'user-agent':user_agent,'cookie': 'over18=1'}
count_date = 0


while True:
    full_url = base_url + sub_url
    response_url = requests.get(full_url, headers = my_headers)
    soup = bs4.BeautifulSoup(response_url.text, 'html.parser')
    ppt_articles = soup.find_all('div', class_='r-ent')

    # 判斷日期是否等於607並跳出迴圈
    if count_date == 608:
        print(count_date)
        print("========DONE======")
        print(full_url)
        break


    # Find the link to the previous page
    prev_link = soup.find('a', string='‹ 上頁')
    if prev_link is None:
        break

    for article in ppt_articles:

        htmal_tag = article.find('div', class_='title').text.strip('')

        # 取得文章標題
        title = htmal_tag.replace('[問卦]', '').replace('[新聞]', '').replace('[爆卦]', '').strip()

        # 取得文章類別
        match = re.search(r'\[.*?\]', htmal_tag)
        if match:
            category = match.group(0)
        else:
            category = 'None'
        
        # 過濾公告或協尋文章
        if '[公告]' in htmal_tag or '[協尋]' in htmal_tag:
            continue

        # 取得回文數
        pop = article.find('div', class_='nrec').text.strip()
        
        # 取得作者ID
        author = article.find('div', class_='author').text.strip()
        
        # 日期字串拆分處理
        date_str = article.find('div', class_='date').text.strip()
        month, day  = date_str.split('/')
        date = int(str(int(month)) + str(int(day[0])) + str(int(day[1])))
        
        # 取得當前index number
        prev_link = soup.find('a', string='‹ 上頁')
        prev_link_url = prev_link['href']
        match = re.search(r'index(\d+)', prev_link_url)
        current_index_num = int(match.group(1)) + 1
        
        # 判斷日期是否需要跳出迴圈
        find_article = soup.find_all('div', class_='r-ent')
        second_article_date = find_article[1]
        date_str = second_article_date.find('div', class_='date').text.strip()
        article_month, article_day = date_str.split('/')
        count_date = int(str(int(article_month)) + str(int(article_day[0])) + str(int(article_day[1])))
        
        if count_date == 608:
            break

        print(f"{title} {pop} {author} {count_date} {current_index_num}")
        
        # 回傳sub_url執行上一頁
        sub_url = prev_link['href']

