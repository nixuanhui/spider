#encoding=utf8
import requests

f = open("G:\\iGit\\ip.txt",'r')
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
        if str(s)=='<Response [200]>':
            print("OK")

    except Exception as e:
        print (e)
