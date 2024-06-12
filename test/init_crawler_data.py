import requests
import bs4
import re
from fake_useragent import UserAgent
import pymysql


## 收尋第一篇日期為0101的頁面
def index_start_page():
    base_url = 'https://www.ptt.cc'
    sub_url = '/bbs/Gossiping/index26767.html'
    ua = UserAgent()
    user_agent = ua.random
    my_headers = {'user-agent':user_agent,'cookie': 'over18=1'}
    date = 0

    while True:
        full_url = base_url + sub_url
        response_url = requests.get(full_url, headers = my_headers)
        soup = bs4.BeautifulSoup(response_url.text, 'html.parser')
        ppt_articles = soup.find_all('div', class_='r-ent')

        # 判斷日期是否等於1231並跳出迴圈
        if date == 1231:
            print(date)
            print(full_url)
            print("========DONE======")
            target_url = full_url
            break


        for article in ppt_articles:
            
            # 日期字串拆分處理
            date_str = article.find('div', class_='date').text.strip()
            month, day  = date_str.split('/')
            date = int(str(int(month)) + str(int(day[0])) + str(int(day[1])))
            
            # 取得當前index number
            prevous_link = soup.find('a', string='‹ 上頁')
            prevous_link_url = prevous_link['href']
            match = re.search(r'index(\d+)', prevous_link_url)
            current_index_num = int(match.group(1)) + 1
            
            # 判斷日期是否需要跳出迴圈
            find_article = soup.find_all('div', class_='r-ent')
            second_article_date = find_article[1]
            date_str = second_article_date.find('div', class_='date').text.strip()
            article_month, article_day = date_str.split('/')
            date = int(str(int(article_month)) + str(int(article_day[0])) + str(int(article_day[1])))
            print(date)

            if date == 1231:
                break

            # 回傳sub_url執行下一頁
            sub_url = prevous_link['href']

    return target_url #回傳值給get_raw_data() -> sub_url 


## 爬取資料並寫入資料庫
def get_raw_data():
    try:
        # 連線資料庫
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='11111111',
            port=3306
            )

        cursor = conn.cursor()
        print("Connected to the database")

        # 建立資料庫
        cursor.execute("CREATE DATABASE IF NOT EXISTS PTT_raw_data")
        print("Database created successfully")

        # 使用資料庫
        cursor.execute("USE PTT_raw_data")
        print("Using database PTT_raw_data")

        # 建立資料表
        create_table_query = ("CREATE TABLE IF NOT EXISTS PTT_Gossiping_data ("
                                "ID INT AUTO_INCREMENT PRIMARY KEY,"
                                "Category VARCHAR(10),"
                                "Title VARCHAR(255),"
                                "Pop INT,"
                                "Author VARCHAR(255),"
                                "Date VARCHAR(10),"
                                "Current_page_index INT"
                                ")")
                            

        cursor.execute(create_table_query)
        print("Table created successfully")


        # 取得 target_url 並開始爬取資料
        base_url = 'https://www.ptt.cc'
        sub_url = index_start_page().replace('https://www.ptt.cc', '')
        ua = UserAgent()
        user_agent = ua.random
        my_headers = {'user-agent':user_agent,'cookie': 'over18=1'}
        date = 0


        while True:
            try:
                full_url = base_url + sub_url
                # print(full_url)
                response_url = requests.get(full_url, headers = my_headers)
                soup = bs4.BeautifulSoup(response_url.text, 'html.parser')
                ppt_articles = soup.find_all('div', class_='r-ent')

                # 判斷日期是否等於102並跳出迴圈
                if date == 600:
                    print(date)
                    print("========DONE======")
                    print(full_url)
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

                    # 取得回文數
                    pop = article.find('div', class_='nrec').text.strip()
                    if pop == '爆':
                        pop = 100
                    elif pop == 'XX':
                        pop = -20
                    elif pop.startswith('X'):
                        pop = -int(pop[1:])
                    elif pop == '':
                        pop = 0
                    else:
                        pop = int(pop)
                    
                    # 取得作者ID
                    author = article.find('div', class_='author').text.strip()
                    
                    # 日期字串拆分處理
                    date_str = article.find('div', class_='date').text.strip()
                    if not date_str.replace('/', '').isdigit(): # 檢查data_str不是數字轉0/00
                        month_str = '0'
                    else:
                        month_str, day_str  = date_str.split('/')
                        date = int(str(int(month_str)) + str(int(day_str[0])) + str(int(day_str[1])))
                    
                    # 取得當前index number
                    next_link = soup.find('a', string='下頁 ›')
                    next_link_url = next_link['href']
                    if next_link_url == next_link['href']:
                        match = re.search(r'index(\d+)', next_link_url)
                        current_index_num = int(match.group(1)) + 1
                        sub_url = next_link['href'] #回傳值給sub_url
                    else:
                        # 當next_link_url == None時, 無下一頁可以爬取
                        break

                    # 略過本次迴圈, 過濾公告或協尋文章
                    if '[公告]' in htmal_tag or '[協尋]' in htmal_tag:
                        continue

                    # 略過本次迴圈, 類別是None或標題是空或作者是空
                    if category == 'None' or title == '' or article.find('div', class_='author').text.strip() == '' or month_str == '0':
                        continue

                    # 略過本次迴圈, 日期是1231
                    if date == 1231:
                        continue

                    # 日期是102跳出迴圈
                    if date == 600:
                        break

                    print(f"{title} {pop} {author} {date} {current_index_num}")

                    try:
                        # 寫入資料庫
                        insert_query = ("INSERT INTO PTT_Gossiping_data (Category, Title, Pop, Author, Date, Current_page_index)"
                                "VALUES (%s, %s, %s, %s, %s, %s)")
                        
                        cursor.execute(insert_query, (category, title, pop, author, date, current_index_num))
                        conn.commit()
                        print(f"{current_index_num} Data inserted successfully")

                    except Exception as e:
                        print(f"Error inserting data: {e}")
            
            except Exception as e:
                print(f"Error cawler issue: {e}")
                break


    except Exception as e:
        print(f"Error connecting to the database: {e}")

    finally:
        # 關閉資料庫連線
        cursor.close()
        conn.close()
        print("Database connection closed")


if __name__ == '__main__':
    get_raw_data()
