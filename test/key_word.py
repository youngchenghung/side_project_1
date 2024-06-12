import jieba
import jieba.analyse
from collections import Counter
import pandas as pd
import csv
import my_sql_db
import matplotlib.pyplot as plt


def get_all_article_title():
    conn, cursor = my_sql_db.connect_db()

    try:
        # 使用資料庫
        cursor.execute("USE PTT_raw_data")

        # 讀取資料
        cursor.execute("SELECT Title FROM PTT_Gossiping_data WHERE date BETWEEN 101 AND 531")
        result = cursor.fetchall()


        with open('test/temp_title_data.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Title'])

            # 讀取Title欄位資料
            
            for row in result:
                writer.writerow([row[0]])

    except Exception as e:
        print("Error: ", e)

    finally:
        my_sql_db.close_db(conn, cursor)
        print("Database connection closed")



jieba.enable_paddle()
def jieba_conversion():
    # 读取CSV文件
    df = pd.read_csv('test/temp_title_data.csv')  # 请将文件名替换为你的CSV文件名

    # 加载自定义词库和停用字
    # jieba.load_userdict("dict.txt.big")  # 加载预设词库
    jieba.set_dictionary("test/custom_names.txt")  # 加载自定义人名词典
    with open("test/stop_words.txt", "r", encoding="utf-8") as f:  # 读取停用字文件
        stopwords = f.read().splitlines()

    # 假设文本数据在'Title'列中
    texts = df['Title'].tolist()

    # 进行分词
    segmented_texts = []

    # 遍历每个文本，对其进行分词并过滤停用词和单个字的词语，然后连接成字符串，存入segmented_texts中
    for text in texts:
        # 将文本进行分词
        segmented_words = jieba.cut(text, use_paddle=True)
        # 过滤停用词和单个字的词语
        filtered_segmented_words = []
        for word in segmented_words:
            if word not in stopwords and len(word) > 1:  # 过滤停用词和单个字的词语
                filtered_segmented_words.append(word)
        # 将分词后的词语列表连接成字符串，以空格分隔
        segmented_string = ' '.join(filtered_segmented_words)
        # 将连接后的字符串添加到segmented_texts列表中
        segmented_texts.append(segmented_string)

    # 删除只出现一次的词语
    all_words = ' '.join(segmented_texts).split()
    word_counts = Counter(all_words)
    filtered_words = [word for word in all_words if word_counts[word] > 1]

    # 将分词结果添加到数据框中
    df['segmented_content'] = segmented_texts
    # print(df.head())  # 打印前5行数据，检查结果

    # 进行词频统计
    word_counts = Counter(filtered_words)

    # 打印出现次数最多的10个词
    top_10_word_counts = word_counts.most_common(10)
    # print(type(word_counts.most_common(10)))

    # 保存分词结果到新的CSV文件
    df.to_csv('test/segmented_output.csv', index=False)

    return top_10_word_counts



#### 熱門關鍵字 ####
def get_top_10_keyword():

    # 將top_10_word_counts[0]放入list_words
    list_words = []
    list_counts =[]
    top_10_word_counts = jieba_conversion()
    for i in range(10):
        list_words.append(top_10_word_counts[i][0])
        list_counts.append(top_10_word_counts[i][1])
    
    print(list_words)
    print(list_counts)



    # list_words = (list(sort_counts['Word'][0:10]))
    # list_counts = (list(sort_counts['Counts'][0:10]))
    plt.figure(figsize=(9,5))
    plt.rcParams["font.family"] = 'Arial Unicode MS'
    separeted = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
    plt.pie(list_counts,                           # 數值
            labels = list_words,                # 標籤
            autopct = "%1.1f%%",            # 將數值百分比並留到小數點一位
            explode = separeted,            # 設定分隔的區塊位置
            pctdistance = 0.6,              # 數字距圓心的距離
            textprops = {"fontsize" : 12},  # 文字大小
            shadow=True)                    # 設定陰影


    plt.axis('equal')                                          # 使圓餅圖比例相等
    plt.title("Top 10 keyword in PTT", {"fontsize" : 20})  # 設定標題及其文字大小
    plt.legend(loc = "best")                                   # 設定圖例及其位置為最佳
    plt.show()

    # 儲存路徑為static資料夾
    # static_dir = os.path.join('..', 'static/')
    plt.savefig('test/ptt_get_top_10_keyword.jpg')


# get_all_article_title()
# jieba_conversion()
get_top_10_keyword()