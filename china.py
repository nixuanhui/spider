from bs4 import BeautifulSoup
import requests
import re
import xlwt
import datetime
import time
import random
import threading
def findCity(url):#获取市级或区级信息
    Target = url;
    Target0 = "http://www.xzqy.net/"
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
    ip=getip()
    rep = requests.get(url=Target,headers=headers,proxies=ip)
    text = rep.text;
    soup = BeautifulSoup(text, "html5lib")
    city = str(soup.find_all('td', class_="parent")).split('<a')
    pattern = re.compile('"./(.*htm)"')
    pattern1 = re.compile('>(.*)</a>')
    del city[0]#去除无用信息


    cityUrl = [];
    cityName = [];
    for i in range(len(city)):
        cityU = Target0 + pattern.findall(city[i])[0]
        name = pattern1.findall(city[i])[0]  # 市或区名
        cityUrl.append(cityU)
        cityName.append(name)
    return [cityUrl, cityName]


def getMessage(url):#获取街道信息
    Target = url

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
    ip = getip()
    rep = requests.get(url=Target, headers=headers, proxies=ip)
    text = rep.text;
    soup = BeautifulSoup(text, "html5lib")
    city = str(soup.find_all('td', class_="parent")).split('<a')

    pattern1 = re.compile('>(.*)</a>')
    del city[0]

    message = []
    for i in range(len(city)):
        target2 = pattern1.findall(city[i])[0]  # 省名
        message.append(target2)
    return message
def getip():#随机获取可用ip
    f = open("G://ip.txt", 'r')
    lines = f.readlines()
    proxys = []
    for i in range(0, len(lines)):
        ip = lines[i]
        proxy = 'http:\\' + ip
        proxies = {'proxy': proxy}
        proxys.append(proxies)
    pro=random.choice(proxys);
    f.close()
    return pro

def province(url,Pname):#以省为单位保存数据

    city = [];
    name = [];
    [city, name] = findCity(url)
    wrd = xlwt.Workbook()
    sheet = wrd.add_sheet(Pname)
    CityRow = 0;
    row = 0;
    print("即将爬取"+Pname+"数据*************************************")
    for i in range(len(name)):
        sheet.write(CityRow, 0, name[i])

        [countryU, CountryName] = findCity(city[i])
        print("爬取" + name[i] + "数据中")

        for j in range(len(CountryName)):
            sheet.write(row, 1, CountryName[j])
            message = getMessage(countryU[j])
            print('正在爬取' + CountryName[j] + "数据")

            sss="、".join(message)
            sheet.write(row,2,sss)
            print(CountryName[j] + "数据写入完成")
            row = row + 1;
        print(name[i] + "数据写入完成")
        CityRow = CityRow + len(CountryName);
    wrd.save("G://"+Pname+".xls")
    print("爬取完成")

Target="http://www.xzqy.net/"
headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
ip = getip()
rep = requests.get(url=Target, headers=headers, proxies=ip)

text=rep.text;
soup=BeautifulSoup(text, "html5lib")
province0=str(soup.find_all('div',class_="navi")).split('</a>')#得到各省名及网址
pattern = re.compile('./(.*)"')
pattern1=re.compile('>(.*)')
del province0[0]
del province0[0]
del province0[-1]
for i in range(0,len(province0)):
    target1=Target+pattern.findall(province0[i])[0]
    target2=pattern1.findall(province0[i])[0]#省名
    province(target1,target2)


