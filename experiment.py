# -*- encoding: utf-8 -*-
# Written by Zibo

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import pandas as pd
import jieba
import jieba.analyse
import time
from datetime import datetime
from nltk.probability import FreqDist
import nltk
from gensim import corpora, models
from sklearn.cluster import KMeans
import numpy as np

stop_words = ' '.join(open('data/stop_word.txt').readlines()).encode('utf8').split()
N_TOPICS = 8

# 输入表达时间的字符串，输出第几周
def cal_week(time_str):
    news_time = time.mktime(time.strptime(time_str, unicode("%Y-%m-%d %H:%M:%S", "utf8")))
    news_time = datetime.fromtimestamp(news_time) 
    init_time = datetime(2017, 4, 24, 0, 0, 0)
    return (news_time - init_time).days / 7

# 分词和去除停用词
def split_and_cut_stop_word(s):
    remain_words = []
    words = jieba.cut(str(s))
    for i in words:
        if i not in stop_words: # 不在停用词列表中的词才保留
            remain_words.append(i)
    return  ' '.join(remain_words).encode('utf8')

# 预处理
def preprocessing(news_csv_path):
    output_csv_path = 'data/news_processed.csv'
    df = pd.read_csv(news_csv_path, sep='\t') # DataFrame
    news_cut = df['news content'].apply(split_and_cut_stop_word) # 对每一条新闻的news content域使用分词和去除停用词函数
    df['news cut'] = news_cut
    news_week = df['news time'].apply(cal_week) # 对每一条新闻的news time域计算具体是第几周
    df['news week'] = news_week
    df = df.sort_values(by='news week') # 按周序排列新闻
    df.to_csv(output_csv_path, index=False, sep='\t')

# 统计分析
def statistic_analysis(csv_path):
    output_csv_path = 'data/most_frequent_words.csv'
    column_names = ['week', 'top1 frequent word', '1 frequency', 'top2 frequent word', '2 frequency', 'top3 frequent word', '3 frequency', 'top4 frequent word', '4 frequency', 'top5 frequent word', '5 frequency', 'top6 frequent word', '6 frequency', 'top7 frequent word', '7 frequency', 'top8 frequent word', '8 frequency', 'top9 frequent word', '9 frequency', 'top10 frequent word', '10 frequency']
    df_week_words = pd.DataFrame(columns=column_names)
    df = pd.read_csv(csv_path, sep='\t') # DataFrame
    news_per_week = {} # 字典结构：{第1周:[新闻1, 新闻2, ...], 第2周:[新闻1, 新闻2, ...], ...}
    for row_index, row in df.iterrows(): # 遍历统计csv，统计每周的新闻
        if row['news week'] not in news_per_week:
            news_per_week[row['news week']] = [row['news cut']]
        else:
            news_per_week[row['news week']].append(row['news cut'])
    for week in news_per_week:
        fdist = FreqDist()
        word_list = ' '.join(news_per_week[week]).split()
        for word in word_list: # 统计每周新闻的词频
            fdist[word] += 1
        freq_list = sorted(fdist.items(), key=lambda i:i[1], reverse=True) # 词频从高到低排序
        l = [week]
        for i in range(10):
            l.append(freq_list[i][0]) # 记录下高频词
            l.append(freq_list[i][1] * 1.0 / len(word_list)) # 记录下高频词的词频
        df_week_words = df_week_words.append(pd.DataFrame([l], columns=column_names))
    df_week_words.to_csv(output_csv_path, index=False, sep='\t')

# 话题检测
def topic_detection(csv_path):
    df = pd.read_csv(csv_path, sep='\t') # DataFrame
    words = []
    for row_index, row in df.iterrows():
        words.append(row['news cut'].split())
    dic = corpora.Dictionary(words) # 使用所有词汇构造词典
    corpus = [dic.doc2bow(text) for text in words] # 构造语料库
    lda = models.LdaModel(corpus, id2word=dic, num_topics=N_TOPICS) # 训练LDA模型的N个话题
    ldaOut=lda.print_topics(N_TOPICS)
    column_names = ['topic id','keyword1','keyword2','keyword3','keyword4','keyword5','keyword6','keyword7','keyword8','keyword9','keyword10'] # 每个话题有10个关键字
    df_topic_keywords = pd.DataFrame(columns=column_names)
    for i in range(N_TOPICS):
        l = [ldaOut[i][0], ldaOut[i][1].split('"')[1], ldaOut[i][1].split('"')[3], ldaOut[i][1].split('"')[5], ldaOut[i][1].split('"')[7], ldaOut[i][1].split('"')[9], ldaOut[i][1].split('"')[11], ldaOut[i][1].split('"')[13], ldaOut[i][1].split('"')[15], ldaOut[i][1].split('"')[17], ldaOut[i][1].split('"')[19]]
        df_topic_keywords = df_topic_keywords.append(pd.DataFrame([l], columns=column_names)) # 添加一行话题关键字
    df_topic_keywords.to_csv('data/topic_keywords.csv', index=False, sep='\t') # 保存话题关键字
    corpus_lda = lda[corpus]
    column_names = ['topic0','topic1','topic2','topic3','topic4','topic5','topic6','topic7']
    df_news_topic = pd.DataFrame(columns=column_names)
    for doc in corpus_lda: # 对语料库中的每一篇文档
        l = [0] * N_TOPICS
        for i in doc: # 获取文档为每个话题的概率
            l[i[0]] = i[1] 
        df_news_topic = df_news_topic.append(pd.DataFrame([l], columns=column_names))
    week = pd.read_csv(csv_path, sep='\t')['news week'].values
    print week
    week = np.array([week])
    week = np.transpose(week)
    df_news_topic['news week'] = week
    print df_news_topic
    df_news_topic.to_csv('data/news_topic.csv', index=False, sep='\t')

# 聚类分析
def cluster_analysis(csv_path):
    df = pd.read_csv(csv_path, sep='\t') # DataFrame
    X = df.values
    kmeans = KMeans(n_clusters=8, random_state=0).fit(X) # 训练K means聚类模型
    l = np.array([kmeans.labels_]) # 将每条新闻的标签组成一个向量
    l = np.transpose(l) # 转化成列向量
    df = pd.read_csv('data/news_processed.csv', sep='\t')
    df['label'] = l
    df = df.sort_values(by='label') # 排列新闻
    df.to_csv('data/news_cluster.csv', index=False, sep='\t')


if __name__ == '__main__':
    #preprocessing('data/news.csv')
    #statistic_analysis('data/news_processed.csv')
    topic_detection('data/news_processed.csv')
    #cluster_analysis('data/news_topic.csv')
