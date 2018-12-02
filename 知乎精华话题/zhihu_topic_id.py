# -*- coding: utf-8 -*-
# @Time    : 2018/12/2 15:07
# @Author  : theo

import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
'''
本脚本用于爬取知乎话题id
'''

#存储大类网址
lists = ['https://www.zhihu.com/topics#%E7%94%9F%E6%B4%BB%E6%96%B9%E5%BC%8F',
                 'https://www.zhihu.com/topics#%E7%BB%8F%E6%B5%8E%E5%AD%A6',
                 'https://www.zhihu.com/topics#%E8%BF%90%E5%8A%A8',
                 'https://www.zhihu.com/topics#%E4%BA%92%E8%81%94%E7%BD%91',
                 'https://www.zhihu.com/topics#%E8%89%BA%E6%9C%AF',
                 'https://www.zhihu.com/topics#%E9%98%85%E8%AF%BB', 'https://www.zhihu.com/topics#%E7%BE%8E%E9%A3%9F',
                 'https://www.zhihu.com/topics#%E5%8A%A8%E6%BC%AB', 'https://www.zhihu.com/topics#%E6%B1%BD%E8%BD%A6',
                 'https://www.zhihu.com/topics#%E8%B6%B3%E7%90%83', 'https://www.zhihu.com/topics#%E6%95%99%E8%82%B2',
                 'https://www.zhihu.com/topics#%E6%91%84%E5%BD%B1', 'https://www.zhihu.com/topics#%E5%8E%86%E5%8F%B2',
                 'https://www.zhihu.com/topics#%E6%96%87%E5%8C%96', 'https://www.zhihu.com/topics#%E6%97%85%E8%A1%8C',
                 'https://www.zhihu.com/topics#%E8%81%8C%E4%B8%9A%E5%8F%91%E5%B1%95',
                 'https://www.zhihu.com/topics#%E9%87%91%E8%9E%8D',
                 'https://www.zhihu.com/topics#%E6%B8%B8%E6%88%8F', 'https://www.zhihu.com/topics#%E7%AF%AE%E7%90%83',
                 'https://www.zhihu.com/topics#%E7%94%9F%E7%89%A9%E5%AD%A6',
                 'https://www.zhihu.com/topics#%E7%89%A9%E7%90%86%E5%AD%A6',
                 'https://www.zhihu.com/topics#%E5%8C%96%E5%AD%A6', 'https://www.zhihu.com/topics#%E7%A7%91%E6%8A%80',
                 'https://www.zhihu.com/topics#%E4%BD%93%E8%82%B2', 'https://www.zhihu.com/topics#%E5%95%86%E4%B8%9A',
                 'https://www.zhihu.com/topics#%E5%81%A5%E5%BA%B7', 'https://www.zhihu.com/topics#%E5%88%9B%E4%B8%9A',
                 'https://www.zhihu.com/topics#%E8%AE%BE%E8%AE%A1',
                 'https://www.zhihu.com/topics#%E8%87%AA%E7%84%B6%E7%A7%91%E5%AD%A6',
                 'https://www.zhihu.com/topics#%E6%B3%95%E5%BE%8B', 'https://www.zhihu.com/topics#%E7%94%B5%E5%BD%B1',
                 'https://www.zhihu.com/topics#%E9%9F%B3%E4%B9%90', 'https://www.zhihu.com/topics#%E6%8A%95%E8%B5%84']

max = len(lists)
for i in range(max):
    b = int(i)
    print(str(i))
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(chrome_options=chrome_options,)
    # 打开大类网址
    browser.get(lists[b])
    time.sleep(2)

    # 动态加载
    for i in range(10):
        try:
            print('休眠2秒')
            time.sleep(2)
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            a = browser.find_element_by_xpath('//*[@class="zg-btn-white zu-button-more"]')#向下滑动
            a.click()
        except:
            break
    # 获取小类id
    print('获取并保存')
    aaa = re.findall("/topic/(\d+)", browser.page_source, re.S)
    aaa=[str(i) for i in aaa]
    with open('topic_id.txt','a') as tmp:
        tmp.write('\n'.join(aaa))
    print('ok')