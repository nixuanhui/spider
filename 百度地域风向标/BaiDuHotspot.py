# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 14:23:31 2018

@author: theo
"""

import requests
import re
import pymysql.cursors
import time
import redis
def spider(url,data):
    content=[]
    flag=0
    while(flag<5):
        try:
            
            
            headers = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
            
            result = requests.post(url, data=data,headers=headers)
            content=re.findall('"keyword":"(.*?)"',result.text)
            
            if content:
                return content
        except Exception as err:
            print('出现异常\n休眠5秒')
            time.sleep(5)
            flag+=1

    
    
def insert(data_city,content):
    insert_sql="insert into hot_word(city,city_number,hot_word,rank,create_time) values "
    for i in range(len(content)):
        content[i]=content[i].encode('utf-8').decode('unicode_escape')
        insert_sql=insert_sql+"('"+str(data_city[1])+"',"+str(data_city[0])+",'"+content[i]+"','"+str(i+1)+"','"+str(int(time.time()))+"'),"
    
    insert_sql=insert_sql[:-1]
    try:
        connection=pymysql.connect(**config)
        with connection.cursor() as cursor:
            cursor.execute(insert_sql)
        connection.commit()
    except Exception as err:
        print(insert_sql)
        raise(err)
    finally :
        connection.close()
        
        
config = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'root',
          'password':'root',
          'db':'spider',
    
          }

cities_number=[('0', '全国'), ('928', '安徽'), ('934', '澳门'), ('911', '北京'), ('904', '重庆'), ('909', '福建'), ('913', '广东'), ('925', '甘肃'), ('912', '广西'), ('902', '贵州'), ('920', '河北'), ('921', '黑龙江'), ('927', '河南'), ('908', '湖南'), ('906', '湖北'), ('930', '海南'), ('922', '吉林'), ('916', '江苏'), ('903', '江西'), ('907', '辽宁'), ('905', '内蒙古'), ('919', '宁夏'), ('918', '青海'), ('910', '上海'), ('914', '四川'), ('901', '山东'), ('929', '山西'), ('924', '陕西'), ('923', '天津'), ('931', '台湾'), ('932', '西藏'), ('933', '香港'), ('926', '新疆'), ('915', '云南'), ('917', '浙江')]


url = 'http://top.baidu.com/region/singlelist'
data = {'boardid': '341', 'divids[]': '0'}
erro_flag=[]  #数据缺失省市


#爬取数据
for i in cities_number:
    print('====================开始爬取'+i[1]+'热点数据====================')
    data['divids[]']=i[0]
    content=spider(url,data)
    if content:
        print('爬取完成，进行插入操作')
        try:
            insert(i,content)
        except Exception as err:
            print(err)
            print('出现异常，终止程序')
            break
        print('插入完成')
    else:
        print('无数据')
        erro_flag.append(i)
        if len(erro_flag)>5:
            print('网站异常，停止爬取')
            break
    print('休眠5秒')
    time.sleep(5)
#补充爬取
if erro_flag:
    for i in erro_flag:
        print('====================开始爬取'+i[1]+'热点数据====================')
        data['divids[]']=i[0]
        content=spider(url,data)
        if content:
            print('爬取完成，进行插入操作')
            try:
                insert(i,content)
            except Exception as err:
                print(err)
                print('出现异常，终止程序')
                break
            print('插入完成')
        else:
            print('无数据')
            
            if len(erro_flag)>5:
                print('网站异常，停止爬取')
                break
        print('休眠5秒')
        time.sleep(5)
print('爬取完成！！')