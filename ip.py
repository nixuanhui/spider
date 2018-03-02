from bs4 import BeautifulSoup
import requests
import random
import lxml
def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list

if __name__ == '__main__':
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    ip_list = get_ip_list(url, headers=headers)
    #proxies = get_random_ip(ip_list)
    file=open('G://ip.txt','w+')
    urlTest="https://www.baidu.com"
    for i in range(len(ip_list)):
      ip= 'http:\\' + ip_list[i];
      proxies = {'proxy': ip}
      try:                                  #检测ip是否可用
          ss = requests.get(urlTest, proxies=proxies)
          if str(ss) == '<Response [200]>':
              str1 = ip_list[i] + "\n"
              file.write(str1);

      except Exception as e:
          print (e)

      
    file.close()
    print(ip_list)

