# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 15:47:43 2018

@author: theo
"""

#代码功能：批量下载指定搜狗词库（例如搜狗娱乐类词库），转化并保存成txt格式到本地电脑
#代码运行需要借助了代理ip，相关代码已剔除
#下载其他词库需要手动更改链接，同时修改本地保存地址


from multiprocessing import Pool
import requests
from scel_to_txt import scel_parser
from lxml import etree

import time
import random



#获取随机请求头
def rand_headers():
    USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]
    headers={}
    headers['User-Agent']=random.choice(USER_AGENTS)
    return headers


#获取每页词表的下载连接
def get_data_url(url):
   
    flag=0
    while(flag<5):
        try:
            
            
            html_tmp=requests.get(url,headers=rand_headers(),timeout=10)
            html = etree.HTML(html_tmp.text)
            result = html.xpath('//div[@class="dict_dl_btn"]/a/@href')
            if result:
                return result
            else:
                print('数据为空，休眠5秒')
                # print(html_tmp.text)
                time.sleep(4)
        except Exception as err:
            print('爬取出现异常\n休眠5秒')
            time.sleep(5)
            flag+=1

#下载词表，并转格式为txt
def get_data(url,i):
    flag=0
    while(flag<5):
        try:
            
            result=requests.get(url,headers=rand_headers(),timeout=10)
            with open(r'E:\hui_code\work_space\test'+str(i)+'.txt','w') as tmp:
                tmp.write('\n'.join(scel_parser.parse(result.content)))#得到的内容是scelgeshi,借助scel_parser解析scel格式成txt格式
            break
        except Exception as err:
            print('出现异常\n休眠5秒')
            time.sleep(5)
            flag+=1

#爬虫主程序
def spider_run(i):
    url = 'https://pinyin.sogou.com/dict/cate/index/403/default/' #娱乐类词库链接
    print('========================开始爬取第' + str(i) + '页内容========================')
    url = url + str(i)
    data_urls = get_data_url(url)
    time.sleep(3)
    flag = 0
    if data_urls:

        for j in data_urls:
            print('开始爬取第' + str(i) + '页第' + str(flag) + '条内容')
            get_data(j,i)

            flag += 1




if __name__=='__main__':
    po=Pool(5) #定义一个进程池，最大进程数3

    for i in range(1,99):
        po.apply_async(spider_run,(i,))

    print("----start----")
    po.close() #关闭进程池，关闭后po不再接收新的请求
    po.join() #等待po中所有子进程执行完成，必须放在close语句之后
    print("-----end-----")