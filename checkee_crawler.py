# -*- coding: utf-8 -*
import urllib2,json
import ssl
import datetime
from bs4 import BeautifulSoup
import lxml.html as lh

def crawl(visaType, month, city, date):
    context = ssl._create_unverified_context()
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    url = ""
    if month < 10:
        url = "https://www.checkee.info/main.php?dispdate=2019-0" + str(month)
    else :
        url = "https://www.checkee.info/main.php?dispdate=2019-" + str(month)
    print("Request to url :" + url)
    print("查询中=============================================================")
    req = urllib2.Request(url, headers = hdr)
    response = urllib2.urlopen(req, context = context)
    # workFile = "checkee-page-" + str(datetime.datetime.now().time())
    soup = BeautifulSoup(response.read().decode('utf-8', 'ignore'), "html.parser")
    t = soup.find_all("table")

    print("在您之前面谈，且仍然Pending的还有：")
    for row in t[6].select("tr"):
        td = row.select("td")
        if(td[2].text == visaType
        and td[4].text == city
        and td[6].text == "Pending"
        and td[7].text < date):
            # print(row)
            print("User ID: " + td[1].text + " | " + "Visa Type: " + td[2].text + " | " + "Interview Date: " + td[7].text + " | " + "Detail Info: " + td[10].a['href'])
def main():
    visaType = raw_input("请输入签证类型(H1/F1/J1/B1): ")
    month = input("您想搜索哪个月份？(输入数字): ")
    city = raw_input("您在哪个城市签证?（BeiJing/GuangZhou/ShangHai/Vancouver）: ")
    date = raw_input("您的面谈日期？（请按照yyyy-mm-dd格式）: ")
    crawl(visaType, month, city, date)

if __name__ == "__main__":
    main()

