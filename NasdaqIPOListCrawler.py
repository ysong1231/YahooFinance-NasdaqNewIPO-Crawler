import requests
from bs4 import BeautifulSoup
import time
import easygui

def generate_url(url, years, months):
    rst = []
    for y in years:
        for m in months:
            rst.append(url+y+'-'+m)
    return rst

def get_html(url, headers = None, timeout = 5, proxies = None):
    try:
        response = requests.post(url, headers = headers, timeout = timeout, proxies = proxies)
        if response.status_code == 200:
            return response.content
    except:
        for i in range(1, 10):
            print ('Request Timeout, retry time '+str(i)+'...')
            try:
                response = requests.post(url, headers = headers, timeout = timeout)
                if response.status_code == 200:
                    return response.content
            except:
                continue
    return -1

def get_info(html):
    soup = BeautifulSoup(html,'html.parser')
    records = soup.find('tbody').find_all('tr')
    rst = []
    for record in records:
        td = record.find_all('td')
        rcd = []
        for tr in td:
            rcd.append(tr.text)
        rst.append(rcd)
    return rst

base_url = "https://www.nasdaq.com/markets/ipos/activity.aspx?tab=pricings&month="
years = ['2018']
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
url_list = generate_url(base_url, years, months)

f = open('Data/IPO_list.txt', 'a')
while url_list != []:
    url = url_list.pop(-1)
    
    response = get_html(url)  
    if response == -1:
        print('Woops, something wrong... Current URL: '+ url)
        url_list.append(url)
        print(str(len(url_list))+' Pieces left!')
        easygui.msgbox("Woops, something wrong...", title="Woops!", ok_button="OK") 
        f.close()
        break
    
    print('Analyzing html...')
    rst = get_info(response)
    
    for r in rst:
        f.write('\t'.join(r)+'\n')
f.close()
