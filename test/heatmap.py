import pandas as pd
import csv
import my_sql_db
import matplotlib.pyplot as plt
import seaborn as sns


def get_pop_count():
    conn, cursor = my_sql_db.connect_db()

    try:
        # 使用資料庫
        cursor.execute("USE PTT_raw_data")

        # 讀取資料
        query = """SELECT Pop, 
                    CAST(FLOOR(Date / 100) AS UNSIGNED) AS month, 
                    CAST(Date % 100 AS UNSIGNED) AS day
                    FROM PTT_Gossiping_data
                    WHERE date BETWEEN 101 AND 531;"""
        cursor.execute(query)
        result = cursor.fetchall()


        with open('test/temp_pop_count_data.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Pop', 'Month', 'Day'])

            # 資料寫入個別欄位
            for row in result:
                writer.writerow([row[0],row[1],row[2]])

    except Exception as e:
        print("Error: ", e)

    finally:
        my_sql_db.close_db(conn, cursor)
        print("Database connection closed")


#### 1至5月文章數的熱力圖表 ####
def get_heatmap_result():

    df = pd.read_csv('test/temp_pop_count_data.csv')
    # print(df)

    # 將資料轉換成適合繪製熱力圖的格式
    heatmap_data = df.pivot_table(index='Month', columns='Day', values='Pop', aggfunc='sum', fill_value=0)

    # 繪製熱力圖
    plt.rcParams["font.family"] = 'Arial Unicode MS'
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data,  fmt="d", cmap='coolwarm')
    plt.title('1至5月文章數的熱力圖表')
    plt.yticks(rotation=0)
    plt.ylabel('單位：月')
    plt.xlabel('單位：日')
    plt.show()


    # # 儲存路徑為static資料夾
    # static_dir = os.path.join('..', 'static/')
    plt.savefig('test/ptt_pop_count_heatmap.png')

# get_pop_count()
get_heatmap_result()