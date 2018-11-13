# -*- coding=utf-8 -*-
from Crypto.Cipher import AES
import base64
import requests
import json
import codecs
import time
import random
import pymongo
# 头部信息
headers = {
    'Host':"music.163.com",
    'Accept-Language':"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    'Accept-Encoding':"gzip, deflate",
    'Content-Type':"application/x-www-form-urlencoded",
    'Cookie':"_iuqxldmzr_=32; _ntes_nnid=6c1af3c48436cb3b97668169a40c4c24,1516256211288; _ntes_nuid=6c1af3c48436cb3b97668169a40c4c24; __e_=1516452634349; _ngd_tid=Q1LYOdhTTdXuKbqGpMZDXbk%2Bnx%2FmydJ%2B; vjuids=207a50dc2.16223c3d070.0.0ecf709f68465; vjlast=1521018458.1521018458.30; vinfo_n_f_l_n3=8074f322f646afa4.1.0.1521018458252.0.1521018458733; __utma=187553192.1069457778.1521018460.1521018460.1521018460.1; __utmz=187553192.1521018460.1.1.utmcsr=open.163.com|utmccn=(referral)|utmcmd=referral|utmcct=/ted/; __oc_uuid=25ddd590-2767-11e8-a334-8f549e33ca10; P_INFO=m13798244225@163.com|1522166215|0|urs|00&99|gud&1521987264&urs#gud&440300#10#0#0|137225&1|urs|13798244225@163.com; JSESSIONID-WYYY=HcOEyaYI%2FCyb5FpgbI%2Fgaoe%5Cyibk2wrz219gBkflJffRpBxHcYt0xwFdP%2F3faJYKJEHCqgzTr9v7row4nPZ9diVI6ZE5T8t3%2BFN%2B5vh1fCxBD0cw%2FmGfVERBP1CaUdITjPbYy2Ga9woFGmEg%5CjR%2By2VUeYx0q%2FbKI62yGOCf4pYEFdVy%3A1522203991410; __utma=94650624.303187165.1516256212.1522138804.1522202192.5; __utmc=94650624; __utmz=94650624.1522202192.5.5.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmb=94650624.4.10.1522202192",
    'Connection':"keep-alive",
    'Referer':'http://music.163.com/',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
}
# 设置代理服务器
proxies= {


            'http': 'http://120.92.88.202:10000',
            #'http':'http://118.114.77.47:8080',

        }

# offset的取值为:(评论页数-1)*20,total第一页为true，其余页为false
# first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}' # 第一个参数
second_param = b"010001" # 第二个参数
# 第三个参数
third_param = b"00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
# 第四个参数
forth_param = b"0CoJUm6Qyw8W8jud"

# 获取参数
def get_params(page): # page为传入页数
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    if(page == 1): # 如果为第一页
        first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
        h_encText = AES_encrypt(first_param, first_key, iv)
    else:
        offset = str((page-1)*20)
        first_param = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' %(offset,'false')
        h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText

# 获取 encSecKey
def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


# 解密过程
def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    encrypt_text = str(encrypt_text, encoding="utf-8")
    return encrypt_text

# 获得评论json数据
def get_json(url, params, encSecKey):
    data = {
         "params": params,
         "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data,proxies=proxies)
    return response.content
def get_ip():
    ip=random

# 抓取热门评论，返回热评列表
def get_hot_comments(url):
    hot_comments_list = []
    hot_comments_list.append(u"用户ID 用户昵称 用户头像地址 评论时间 点赞总数 评论内容\n")
    params = get_params(1) # 第一页
    encSecKey = get_encSecKey()
    json_text = get_json(url,params,encSecKey)
    json_dict = json.loads(json_text.decoding('utf-8'))
    hot_comments = json_dict['hotComments'] # 热门评论
    print("共有%d条热门评论!" % len(hot_comments))
    for item in hot_comments:
            comment = item['content'] # 评论内容
            likedCount = item['likedCount'] # 点赞总数
            comment_time = item['time'] # 评论时间(时间戳)
            userID = item['user']['userID'] # 评论者id
            nickname = item['user']['nickname'] # 昵称
            avatarUrl = item['user']['avatarUrl'] # 头像地址
            comment_info = userID + " " + nickname + " " + avatarUrl + " " + comment_time + " " + likedCount + " " + comment + u"\n"
            hot_comments_list.append(comment_info)
    return hot_comments_list

# 抓取某一首歌的全部评论
def get_all_comments(url):
    all_comments_list = [] # 存放所有评论
    #all_comments_list.append(u"用户ID 用户昵称 用户头像地址 评论时间 点赞总数 评论内容\n") # 头部信息
    params = get_params(1)
    encSecKey = get_encSecKey()
    json_text = get_json(url,params,encSecKey)
    json_dict = json.loads(json_text.decode('utf-8'))
    comments_num = int(json_dict['total'])
    if(comments_num % 20 == 0):
        page = comments_num / 20
    else:
        page = int(comments_num / 20) + 1
    print("共有%d页评论!" % page)
    for i in range(page):  # 逐页抓取
        params = get_params(i+1)
        encSecKey = get_encSecKey()
        json_text = get_json(url,params,encSecKey)
        json_dict = json.loads(json_text.decode('utf-8'))
        if i == 0:
            print("共有%d条评论!" % comments_num) # 全部评论总数
        for item in json_dict['comments']:
            comment = item['content'] # 评论内容
            likedCount = item['likedCount'] # 点赞总数
            comment_time = item['time'] # 评论时间(时间戳)
            userID = item['user']['userId'] # 评论者id
            nickname = item['user']['nickname'] # 昵称
            #avatarUrl = item['user']['avatarUrl'] # 头像地址
            #comment_info = str(userID) + u" " + nickname + u" " + str(avatarUrl) + u" " + str(comment_time) + u" " + str(likedCount) + u" " + comment + u"\n"
            
            result={
                'comment':str(comment),
                'likedCount':str(likedCount),
                'comment_time':str(comment_time), 
                'userID':str(userID),
                'nickname':str(nickname),
            }
            all_comments_list.append(result)
        print("第%d页抓取完毕!" % (i+1))
    return all_comments_list


# 将评论写入文本文件
def save_to_Mongo(list,song_name):
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client.Wangyiyun
        collection=db[song_name]
        collection.insert_many(list)
        

if __name__ == "__main__":
    start_time = time.time() # 开始时间
    url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_547973104/?csrf_token="
    song_name = u"zheyangdeni"
    all_comments_list = get_all_comments(url)
    save_to_Mongo(all_comments_list,song_name)                                                                                                                                                                                                                                                                                       
    end_time = time.time() #结束时间
    print("程序耗时%f秒." % (end_time - start_time))

