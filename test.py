from selenium import webdriver
import os
import requests
from main import Crawl
headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Referer": "https://kyfw.12306.cn/otn/leftTicket/init",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0"
    }

r = requests.get(url="https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2018-02-10&leftTicketDTO."
                     "from_station=SZQ&leftTicketDTO.to_station=ZZF&purpose_codes=ADULT", headers=headers, verify=False)
r.encoding = "utf-8"
date = "2018-02-11"
from_station = "SZQ"
to_station = "ZZF"
human_type = "ADULT"
train_number = "K4426"
seat = "无座"


mission = Crawl(date, from_station, to_station, human_type, train_number, seat)
mission.open_browser()

print(r.text)
