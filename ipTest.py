#encoding=utf8
import requests

f = open("G://ip.txt",'r')
lines = f.readlines()
proxys = []
for i in range(0,len(lines)):
    ip = lines[i]
    proxy = 'http:\\' + ip
    proxies = {'proxy': proxy}
    proxys.append(proxies)

url = 'https://www.baidu.com'

for pro in proxys:
    try :
        s = requests.get(url,proxies = pro)
        print (s)
    except Exception as e:
        print (e)
