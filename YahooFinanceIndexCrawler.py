import requests
from bs4 import BeautifulSoup
import time
import csv

def get_timeStamp(start_time, end_time):
    return str(int(time.mktime(time.strptime(start_time, "%m/%d/%Y")))), str(int(time.mktime(time.strptime(end_time, "%m/%d/%Y"))))

index_list = ["^NDX", "^GSPC"]

Start_date = '1/1/2018'
End_date = '5/31/2019'

for name in index_list:
    print("Crawling: "+name)
    start, end = get_timeStamp(Start_date, End_date)
    url = 'https://query1.finance.yahoo.com/v7/finance/download/'+name+'?period1='+start+'&period2='+end+'&interval=1d&events=history&crumb=NvISvesKcFr'
    response = requests.post(url, headers = None, timeout = 5, proxies = None)
    data = str(response.content,"utf-8").strip().split('\n')
    out = open('Data/Index_Data/'+name+'.csv','a', newline='')
    csv_write = csv.writer(out,dialect='excel')
    for r in data:
        csv_write.writerow(r.split(','))
    out.close()
    print("Success!")