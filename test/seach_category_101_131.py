import my_sql_db
import csv
import matplotlib.pyplot as plt
import os
import matplotlib.pyplot as plt
from collections import Counter

#### 一月PTT文章類型分佈 ####

def get_category_101_131():
    conn, cursor = my_sql_db.connect_db()

    try:
        # 使用資料庫
        cursor.execute("USE PTT_raw_data")

        # 讀取資料
        cursor.execute("SELECT Category FROM PTT_Gossiping_data WHERE Date BETWEEN 101 AND 131")
        result = cursor.fetchall()

        data_list = []
        for row in result:
            data_list.append(row[0])

        return data_list

    finally:
        cursor.close()
        conn.close()

def plot_category_distribution(categories):
    # print(categories)

    # 限制只計算 [問卦], [新聞], [爆卦] 這三種類別的數量
    filtered_categories = []
    for category in categories:
        if category in ['[問卦]', '[新聞]', '[爆卦]']:
            filtered_categories.append(category)
    # print(filtered_categories)
    # 計算每個類別的數量
    category_counts = Counter(filtered_categories)
    print(category_counts)

    # 定義感興趣的類別標籤
    labels = ['[問卦]', '[新聞]', '[爆卦]']
    print(labels)
    # 獲取每個標籤的對應數量，若標籤不存在則設置為0
    values = []
    for label in labels:
        values.append(category_counts.get(label, 0))
    print(values)

    
    # 繪製柱狀圖
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color=['blue', 'orange', 'green'])
    plt.xlabel('文章類別')
    plt.ylabel('文章數量（篇）')
    plt.title('PTT八卦版 一月文章類別分布')
    plt.show()
    plt.savefig('test/ptt_jan_category_type.png')


# 獲取數據
categories = get_category_101_131()
# 繪製圖表
plot_category_distribution(categories)