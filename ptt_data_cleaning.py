
#%%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 讀取raw data
current_path = os.getcwd()
df = pd.read_csv(os.path.join(current_path, 'PTT_Gossiping_data.csv'))
# print(df.info())

# 將'date'欄位拆分成'month'和'day'兩個欄位
df[['month', 'day']] = df['date'].str.split('/', expand=True)
# 刪除原始的'date'欄位
df = df.drop(columns=['date'])
# 將日期字符串轉換為數值型態
df['month'] = pd.to_numeric(df['month'])
df['day'] = pd.to_numeric(df['day'])
# print(df.info())
# print(df[['month', 'day']])

# 'pop'欄位的所有NaN值替換為0
df['pop'] = df['pop'].fillna(0)
# 'pop'欄位轉換為數值型態
df['pop'] = df['pop'].replace('爆', 100)
df['pop'] = df['pop'].replace('XX', -100)
df['pop'] = df['pop'].replace(r'X(\d+)', r'-\1', regex=True)
df['pop'] = df['pop'].astype(int)
# print(df.info())

# 月份資料處理
month_1_data = df[df['month'] == 1]
month_2_data = df[df['month'] == 2]
month_3_data = df[df['month'] == 3]
month_4_data = df[df['month'] == 4]
month_5_data = df[df['month'] == 5]

# 一月1號的文章
month_1_day_num = 2
month_1_1_data = month_1_data[month_1_data['day'] == month_1_day_num]
print(month_1_1_data)
category_news_month_1_1_data = len(month_1_1_data[month_1_1_data['category'] == '[新聞]'])
print(category_news_month_1_1_data)


# 迴圈month_1_data資料中day欄位1到31份文章中類別篇數
total_1_category_count = []
month_1_day_num = 32
add_news_result = 0
add_gossip_result = 0
add_ask_result = 0
for i in range (1,month_1_day_num):
    # print(i)
    
    day_data = month_1_data[month_1_data['day'] == i]

    category_news_month_1_1_data = len(day_data[day_data['category'] == '[新聞]'])
    add_news_result += category_news_month_1_1_data
    # print(add_news_result)
    
    category_gossip_month_1_1_data = len(day_data[day_data['category'] == '[爆卦]'])
    add_gossip_result += category_gossip_month_1_1_data

    category_ask_month_1_1_data = len(day_data[day_data['category'] == '[問卦]'])
    add_ask_result += category_ask_month_1_1_data

    total_1_category_count.append([add_news_result, add_gossip_result, add_ask_result])

# print(total_1_category_count)
    


# 個月文章數
num_rows_month_1 = len(month_1_data)
print(num_rows_month_1)
num_rows_month_2 = len(month_2_data)
print(num_rows_month_2)
num_rows_month_3 = len(month_3_data)
print(num_rows_month_3)
num_rows_month_4 = len(month_4_data)
print(num_rows_month_4)
num_rows_month_5 = len(month_5_data)
print(num_rows_month_5)

# 文章分類資料
category_news_month_1_data = len(month_1_data[df['category'] == '[新聞]'])
category_gossip_month_1_data = len(month_1_data[df['category'] == '[爆卦]'])
category_ask_month_1_data = len(month_1_data[df['category'] == '[問卦]'])
# print(category_news_month_1_data)

category_news_month_2_data = len(month_2_data[df['category'] == '[新聞]'])
category_gossip_month_2_data = len(month_2_data[df['category'] == '[爆卦]'])
category_ask_month_2_data = len(month_2_data[df['category'] == '[問卦]'])

category_news_month_3_data = len(month_3_data[df['category'] == '[新聞]'])
category_gossip_month_3_data = len(month_3_data[df['category'] == '[爆卦]'])
category_ask_month_3_data = len(month_3_data[df['category'] == '[問卦]'])

category_news_month_4_data = len(month_4_data[df['category'] == '[新聞]'])
category_gossip_month_4_data = len(month_4_data[df['category'] == '[爆卦]'])
category_ask_month_4_data = len(month_4_data[df['category'] == '[問卦]'])

category_news_month_5_data = len(month_5_data[df['category'] == '[新聞]'])
category_gossip_month_5_data = len(month_5_data[df['category'] == '[爆卦]'])
category_ask_month_5_data = len(month_5_data[df['category'] == '[問卦]'])


#%%
#### 一月PTT文章類型分佈 ####

import matplotlib.pyplot as plt
import os


plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

category_type = ['新聞', '爆卦', '問卦']
category_count = [category_news_month_1_data, category_gossip_month_1_data, category_ask_month_1_data]

fig = plt.figure(figsize=(8,5))

plt.xlim(-1,3)
plt.plot(category_type, category_count, marker = 'o', linestyle = '--')

plt.xlabel('文章類別', color = 'red')
plt.ylabel('文章數量（篇）', color = 'red')
plt.tick_params(axis='x', width=5, rotation=45)
plt.title('PTT八卦版 一月文章類別分布', color = 'red')
plt.show()

# 儲存路徑為static資料夾
static_dir = os.path.join('..', 'static/')
plt.savefig(static_dir+'ptt_jan_category_type.png')

#%%
#### 一月每日分布 ####

import matplotlib.pyplot as plt
import matplotlib.animation as animation



# 創建畫布(寬8, 高5)
fig, ax = plt.subplots(figsize=(8,5))


def update(num):
    category_type = ['新聞', '爆卦', '問卦']
    
    ax.clear()
    
    ax.bar(category_type, total_1_category_count[num % len(total_1_category_count)])
    ax.set_title('PTT八卦版 1月文章類別分布', color = 'red')

    ax.set_xlabel('文章類別', color = 'red')
    ax.set_ylabel('文章數量（篇）', color = 'red')
    ax.set_title(f'PTT八卦版 1月 / {num+1}日 文章類別分布', color = 'red')

    # 設定 x 軸的文字刻度間距為 5 個單位
    ax.tick_params(axis='x', width=5, rotation=0)
    # 設定 x 軸的刻度間距為 1
    ax.set_xlim(-1,3)
    # 設定 y 軸的範圍
    ax.set_ylim(0, 35000)
    # 設定 y 軸的刻度間距為 5000
    ax.set_yticks(np.arange(0, 35000, 5000))
    plt.rcParams["font.family"] = 'Arial Unicode MS'
    plt.show()
    
ani = animation.FuncAnimation(fig, update, frames=range(31), repeat=True)

# 儲存路徑為static資料夾
static_dir = os.path.join('..', 'static/')
ani.save(static_dir+'ppt_jan_days_category_type.gif', writer='imagemagick', fps=1/0.2)


#%%
####  一至五月PTT文章類型分佈 ####
    
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# 創建畫布(寬8, 高5)
fig, ax = plt.subplots(figsize=(8,5))


def update(num):
    
    category_type = ['新聞', '爆卦', '問卦']
    category_count_1 = [category_news_month_1_data, category_gossip_month_1_data, category_ask_month_1_data]
    category_count_2 = [category_news_month_2_data, category_gossip_month_2_data, category_ask_month_2_data]
    category_count_3 = [category_news_month_3_data, category_gossip_month_3_data, category_ask_month_3_data]
    category_count_4 = [category_news_month_4_data, category_gossip_month_4_data, category_ask_month_4_data]
    category_count_5 = [category_news_month_5_data, category_gossip_month_5_data, category_ask_month_5_data]
    category_count_list = [category_count_1, category_count_2, category_count_3, category_count_4, category_count_5]
    # print(category_count_list)


    ax.clear()
    ax.bar(category_type, category_count_list[num % len(category_count_list)])
    ax.set_title('PTT八卦版 2024-1月到5月文章類別分布', color = 'red')

    ax.set_xlabel('文章類別', color = 'red')
    ax.set_ylabel('文章數量（篇）', color = 'red')
    ax.set_title(f'PTT八卦版 2024-{num+1}月文章類別分布', color = 'red')

    # 設定 x 軸的文字刻度間距為 5 個單位
    ax.tick_params(axis='x', width=5, rotation=0)
    # 設定 x 軸的刻度間距為 1
    ax.set_xlim(-1,3)
    # 設定 y 軸的範圍
    ax.set_ylim(0, 40000)
    # 設定 y 軸的刻度間距為 5000
    ax.set_yticks(np.arange(0, 40000, 5000))
    plt.rcParams["font.family"] = 'Arial Unicode MS'
    plt.show()

ani = animation.FuncAnimation(fig, update, frames=range(5), repeat=True)

# 儲存路徑為static資料夾
static_dir = os.path.join('..', 'static/')
ani.save(static_dir+'ppt_jan_may_category_type.gif', writer='imagemagick', fps=1/1)



#%%
#### 熱門關鍵字 ####

import pandas as pd
import os
import matplotlib.pyplot as plt

current_path = os.getcwd()
print(current_path)

with (open(current_path+'/PTT_words_count.csv', 'r', encoding='utf-8')) as f:
    PTT_words_count = pd.read_csv(f)
    print(list(PTT_words_count['Counts']))
    

# 排序欄位Counts從大到小
sort_counts = PTT_words_count.sort_values(by='Counts', ascending=False)
print(sort_counts)

list_words = (list(sort_counts['Word'][0:10]))
list_counts = (list(sort_counts['Counts'][0:10]))
plt.figure(figsize=(9,5))

# print(labels)
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
plt.rcParams["font.family"] = 'Arial Unicode MS'
plt.show()

# 儲存路徑為static資料夾
static_dir = os.path.join('..', 'static/')
plt.savefig(static_dir+'ptt_gossping_keyword_search.png')

# %%
#### 1至5月文章數的熱力圖表 ####

import seaborn as sns
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# 讀取raw data
current_path = os.getcwd()
# print(current_path)


df = pd.read_csv(current_path+'/PTT_Gossiping_data.csv')
print(df)

df[['month', 'day']] = df['date'].str.split('/', expand=True)
expand_date = df.drop('date', axis=1)
print(expand_date)


# date_vs_article =  df.groupby(["month", "day"]).size().reset_index(name='article count').sort_values(by='article count', ascending=False)
date_vs_article =  df.groupby(["month", "day"]).size().reset_index(name='article count')
# date_top10 = date_vs_article.head(10)
print(date_vs_article)

month_1 = date_vs_article[date_vs_article['month'] == '1']
month_1_list = list(month_1['article count'])
while True:
    if len(month_1_list) < 31:
        month_1_list.append(0)
    else:
        break
print(len(month_1_list))

month_2 = date_vs_article[date_vs_article['month'] == '2']
month_2_list = list(month_2['article count'])
while True:
    if len(month_2_list) < 31:
        month_2_list.append(0)
    else:
        break
# print(len(month_2_list))

month_3 = date_vs_article[date_vs_article['month'] == '3']
month_3_list = list(month_3['article count'])
while True:
    if len(month_3_list) < 31:
        month_3_list.append(0)
    else:
        break
# print(len(month_3_list))

month_4 = date_vs_article[date_vs_article['month'] == '4']
month_4_list = list(month_4['article count'])
while True:
    if len(month_4_list) < 31:
        month_4_list.append(0)
    else:
        break
# print(len(month_4_list))

month_5 = date_vs_article[date_vs_article['month'] == '5']
# print(month_5)
month_5_list = list(month_5['article count'])
while True:
    if len(month_5_list) < 31:
        month_5_list.append(0)
    else:
        break
# print(len(month_5_list))


list_total_article = [month_1_list, month_2_list, month_3_list, month_4_list, month_5_list]
# print(list_2d)
plt.figure(figsize=(8,2))


sns.heatmap(list_total_article, 
            xticklabels=('1','2','3','4','5','6','7','8','9','10',
                         '11','12','13','14','15','16','17','18','19','20',
                         '21','22','23','24','25','26','27','28','29','30','31'), 
            yticklabels=('1月','2月','3月','4月','5月'),
            cmap='coolwarm', 
            linewidths='0.5',
            cbar_kws={'orientation':'horizontal'})

plt.yticks(rotation=0)
plt.rcParams["font.family"] = 'Arial Unicode MS'
plt.show()

# 儲存路徑為static資料夾
# static_dir = os.path.join('..', 'static/')
# plt.savefig(static_dir+'ptt_gossping_heatmap.png')
# %%

#### 一月每日分布 ####

import matplotlib.pyplot as plt
import matplotlib.animation as animation



# 創建畫布(寬8, 高5)
fig, ax = plt.subplots(figsize=(8,5))

# 迴圈month_1_data資料中day欄位1到31份文章中類別篇數
total_1_category_count = []
month_1_day_num = 32
add_news_result = 0
add_gossip_result = 0
add_ask_result = 0
for i in range (1,month_1_day_num):
    # print(i)
    
    day_data = month_1_data[month_1_data['day'] == i]

    category_news_month_1_1_data = len(day_data[day_data['category'] == '[新聞]'])
    add_news_result += category_news_month_1_1_data
    # print(add_news_result)
    
    category_gossip_month_1_1_data = len(day_data[day_data['category'] == '[爆卦]'])
    add_gossip_result += category_gossip_month_1_1_data

    category_ask_month_1_1_data = len(day_data[day_data['category'] == '[問卦]'])
    add_ask_result += category_ask_month_1_1_data

    total_1_category_count.append([add_news_result, add_gossip_result, add_ask_result])


category_type = ['新聞', '爆卦', '問卦']

ax.clear()

ax.bar(category_type, total_1_category_count[31 % len(total_1_category_count)])
ax.set_title('PTT八卦版 1月文章類別分布', color = 'red')

ax.set_xlabel('文章類別', color = 'red')
ax.set_ylabel('文章數量（篇）', color = 'red')
ax.set_title(f'PTT八卦版 1月 / {31+1}日 文章類別分布', color = 'red')

# 設定 x 軸的文字刻度間距為 5 個單位
ax.tick_params(axis='x', width=5, rotation=0)
# 設定 x 軸的刻度間距為 1
ax.set_xlim(-1,3)
# 設定 y 軸的範圍
ax.set_ylim(0, 35000)
# 設定 y 軸的刻度間距為 5000
ax.set_yticks(np.arange(0, 35000, 5000))
plt.rcParams["font.family"] = 'Arial Unicode MS'
plt.show()



ani = animation.FuncAnimation(fig, frames, repeat=True)

# 儲存路徑為static資料夾
# static_dir = os.path.join('..', 'static/')
# ani.save(static_dir+'ppt_jan_days_category_type.gif', writer='imagemagick', fps=1/0.2)
ani.save('ppt_jan_days_category_type.gif', writer='imagemagick', fps=1/0.2)
# %%
