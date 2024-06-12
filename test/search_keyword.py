import pandas as pd
import csv
import my_sql_db
import matplotlib.pyplot as plt
import seaborn as sns


def get_search_keyword(input_keyword):
    conn, cursor = my_sql_db.connect_db()

    try:
        # 使用資料庫
        cursor.execute("USE PTT_raw_data")

        # 讀取資料
        query = f"""SELECT *
                FROM PTT_Gossiping_data
                WHERE Title LIKE '%{input_keyword}%';"""
        cursor.execute(query)
        result = cursor.fetchall()


        with open('test/temp_search_keyword.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'Pop', 'Author'])

            # 資料寫入個別欄位
            for row in result:
                writer.writerow([row[2], row[3], row[4]])

    except Exception as e:
        print("Error: ", e)

    finally:
        my_sql_db.close_db(conn, cursor)
        print("Database connection closed")

def get_search_keyword_result():
    df = pd.read_csv('test/temp_search_keyword.csv')

    print(df)

    sorted_data = df.sort_values(by='Pop', ascending=False)

    # 選擇Title和Pop欄位
    print(sorted_data[['Title', 'Pop']].head(20))

    # 繪製長條圖
    plt.rcParams["font.family"] = 'Arial Unicode MS'
    plt.figure(figsize=(12, 8))
    sns.countplot(y='Title', data=df)
    plt.title('搜尋關鍵字的文章')
    plt.show()

input_keyword = str(input("請輸入關鍵字: "))
get_search_keyword(input_keyword)
get_search_keyword_result()