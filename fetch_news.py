# -*- encoding: utf-8 -*-
# Written by Zibo

import urllib2
from bs4 import BeautifulSoup
import cPickle
import time
from datetime import datetime
import csv

def save_news_url():
    news_url_list = []

    for i in range(1, 100):
        url = 'http://roll.mil.news.sina.com.cn/col/zgjq/index_' + str(i) + '.shtml'
        contents = urllib2.urlopen(url)
        contents = contents.read()
        soup = BeautifulSoup(contents)
        div = soup.body.div.find_all('div')[6].div.find_all('div')[2]
        for ul in div.find_all('ul'):
            for li in ul.find_all('li'):
                news_url_list.append(li.a['href'])
    
    print news_url_list
    cPickle.dump(news_url_list, open('data/news_url_list.pkl', 'wb'))

def get_news(url):
    contents = urllib2.urlopen(url)
    contents = contents.read()
    soup = BeautifulSoup(contents)
    div = soup.body.select('.main_content')[0]
    news_title = div.select('#main_title')[0].string
    news_time = div.select('#page-tools')[0].find_all('span')[1].string
    news_time = time.mktime(time.strptime(news_time, unicode("%Y年%m月%d日 %H:%M", "utf8")))
    news_time = datetime.fromtimestamp(news_time) 
    news_content = div.select('#wrapOuter')[0].select('.content_wrappr_left')[0].select('#artibody')[0]
    news_content = news_content.find_all('p', recursive=True)
    news_content = ''.join([i.string for i in news_content if i.string != None])
    return news_title, news_time, news_content

if __name__ == '__main__':
    #save_news_url()
    news_url_list = cPickle.load(open('data/news_url_list.pkl'))
    with open('data/news.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(('news url', 'news title', 'news time', 'news content'))
        for url in news_url_list:
            print 'Fatching ', url
            try:
                news_title, news_time, news_content = get_news(url)
                writer.writerow([url, news_title.encode("utf8"), str(news_time), news_content.encode("utf8")])
            except:
                print 'Can not fatch '
