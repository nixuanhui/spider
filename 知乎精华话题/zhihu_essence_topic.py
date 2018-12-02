# -*- coding: utf-8 -*-
# @Time    : 2018/11/30 14:52
# @Author  : theo

import scrapy
from zhihutopic.items import ZhihutopicItem
import re
import json
import logging
'''
借助scrapy爬取知乎精华话题
'''


class zhihuspider(scrapy.Spider):
    handle_httpstatus_list = [429, 403]
    name = 'Zhihu_essence_Spider'
    get_item=0          #统计正常爬取信息
    drop_item=0         #统计不正常爬取信息
    def start_requests(self):
        #获取话题id
        with open(r'E:\hui_code\work_space\topic_id.txt','r') as tmp:
            data=tmp.read()
            topic_id=re.findall('([0-9]*?)\n',data)

        topic_id=[str(i) for i in topic_id]
        for i in topic_id:
            for times in range(4):
                url='https://www.zhihu.com/api/v4/topics/' + str(i) + '/feeds/essence?&limit=10&offset='+str(15*times)
                yield scrapy.Request(url=url,callback=self.parse,meta={'topic_id':str(i)},priority=2)

    def parse(self, response):
        try:
            item = ZhihutopicItem()
            text = json.loads(response.text)
            if "data" not in text and "paging" in text:
                text=text['paging']
            for i in range(len(text["data"])):

                    item['topic_url'] = 'https://www.zhihu.com/topic/' + response.meta['topic_id']

                    item['title'] = text["data"][i]["target"]["question"]["title"]
                    if re.findall('[a-zA-Z]', str(item['title'])):  # 匹配英文字符成功则舍弃
                        continue
                    item['comment_num'] = text["data"][i]["target"]["comment_count"]
                    item['zlike'] = text["data"][i]["target"]["voteup_count"]
                    item['create_time'] = text["data"][i]["target"]["created_time"]
                    item['detail_url'] = 'https://www.zhihu.com/question/' + str(
                        text["data"][i]["target"]["question"]["id"])
                    item['typeid'] = 0
                    item['topic_id'] = response.meta['topic_id']
                    if item['title'] != '':

                        yield item
                        self.get_item = self.get_item + 1
        except:
            print(text)
            self.drop_item = self.drop_item + 1

    def close(self, spider, reason):
        logging.info('捕获到的item数为' + str(self.get_item))
        logging.info('关键信息缺失的item数为' + str(self.drop_item))
