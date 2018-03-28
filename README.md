# spider
python爬各省市行政规划数据，精确到街道。

### 网易云评论爬虫

- Python3环境下直接运行 wangyiyun.py 文件。
- 出现{'msg': 'Cheating', 'code': -460}报错时：修改header的cookie
- 长时间连接无反应则换用代理ip或直接只用本地ip：
  修改    response = requests.post(url, headers=headers, data=data,proxies=proxies)

  去掉proxies=proxies即可。


