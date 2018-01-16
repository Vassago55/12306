# -*- coding: utf-8 -*-
"""
监控类
:params: date  出发日期
:params: from_station  始发站
:params: to_station  到达站
:params: human_type  乘客类型
"""
from json import JSONDecodeError
from time import sleep
from pyquery import PyQuery
from selenium import webdriver
import os
import requests
import json
from GetProvince import GetProvince


class Crawl(object):
    fields_index = {
        3: "车次", 6: "出发地", 7: "目的地", 23: "软卧", 26: "无座", 28: "硬卧", 29: "硬座", 30: "二等座", 31: "一等座", 32: "商务座"
    }
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Referer": "https://kyfw.12306.cn/otn/leftTicket/init",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0"
    }
    # cookies = {
    #     "JSESSIONID": "35EA16A4D9723FF8CC57538C799D3C09", "tk": "neV_LqBf4gbwxRjghfqKqU-N5qh9jyXas6GFfAcgR1R0",
    #     "route": "c5c62a339e7744272a54643b3be5bf64", "BIGipServerotn": "1557725450.50210.0000",
    #     "RAIL_EXPIRATION": "1516293311208", "vRAIL_DEVICEID": "ri49HKkm1b416Juk4OGyeXwekZrfmFTp - oQmO4gCyov - "
    #                                                           "sRVJeWq26waVASpeI96ycMokPo0KGgYCUwBDX7HT1LXZqaQUMlR"
    #                                                           "tm5O - eLSeZQPjwAcdy1WcCu8 - 7tbFD9HXX3m2Fo3AXvG59F"
    #                                                           "tRTJN3z9TKkdKDSOxB",
    #     "_jc_save_fromStation": " % u6DF1 % u5733 % 2CSZQ"
    #     , "_jc_save_toStation": " % u90D1 % u5DDE % 2CZZF"
    #     , "_jc_save_fromDate": "2018 - 02 - 10"
    #     , "_jc_save_toDate": "2018 - 01 - 15"
    #     , "_jc_save_wfdc_flag": "dc",
    #     "BIGipServerpassport": "954728714.50215.0000",
    #     "current_captcha_type": "Z"
    # }
    province_dict = GetProvince.get_province()

    def __init__(self, date, from_station, to_station, human_type, train_number, seat):
        self.date = date
        self.from_station = from_station
        self.to_station = to_station
        self.human_type = human_type
        self.train_number = train_number
        self.seat = {v: k for k, v in self.fields_index.items()}[seat]
        self.url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={date}&" \
              "leftTicketDTO.from_station={from_station}&" \
              "leftTicketDTO.to_station={to_station}&" \
              "purpose_codes={human_type}".format(date=self.date, from_station=self.from_station,
                                                  to_station=self.to_station, human_type=self.human_type)

    def to_crawl(self):
        s = requests.Session()
        print()
        response = s.get(url=self.url, headers=Crawl.headers, verify=False)
        response.encoding = "utf-8"
        if response.status_code == 200:
            try:
                response_json = json.loads(response.text)
            except JSONDecodeError as e:
                print(response.text)
                print(e)
                return None
            return response_json
        else:
            print("返回错误代码:{0}".format(response.status_code))
            print(response.text)
            return None

    def monitor(self):
        content = self.to_crawl()
        # fields_index = [3, 6, 7, 23, 26, 28, 29, 30, 31, 32]
        if content["httpstatus"] == 200:
            for number, item in enumerate(content["data"]["result"]):
                fields = item.split("|")
                if fields[3] == self.train_number and (fields[self.seat] != "" and fields[self.seat] != "无"):
                    print(fields[self.seat])
                    print("{0}次,{1}快!!!!!!!!!!!!!!".format(self.train_number, self.date))
                    self.open_browser()
                    return True

    def open_browser(self):
        # chrome_driver = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        # os.environ["webdriver.chrome.driver"] = chrome_driver
        # PyQuery(self.url)
        browser = webdriver.Chrome()
        # browser.add_cookie(Crawl.cookies)
        browser.get("https://kyfw.12306.cn/otn/leftTicket/init")
        js = "$(\"input[name='leftTicketDTO.train_date']\").removeAttr('readonly')"
        browser.execute_script(js)
        browser.find_element_by_id("fromStationText").click()
        browser.find_element_by_id("fromStationText").send_keys(Crawl.province_dict[self.from_station])
        browser.find_element_by_id("citem_0").click()
        browser.find_element_by_id("toStationText").click()
        browser.find_element_by_id("toStationText").send_keys(Crawl.province_dict[self.to_station])
        browser.find_element_by_id("citem_0").click()
        browser.find_element_by_name("leftTicketDTO.train_date").clear()
        browser.find_element_by_name("leftTicketDTO.train_date").send_keys("2018-02-10")
        browser.find_element_by_id("query_ticket").click()
        sleep(1)
        book_btn_list = browser.find_elements_by_class_name("btn72")
        book_btn = ""
        can_book = browser.find_element_by_id("username")
        print("qian")
        print(can_book)
        for btn in book_btn_list:
            train_code = btn.get_attribute("onclick").split(",")[-3]
            if self.train_number in train_code:
                print("True!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                book_btn = btn
        book_btn.click()
        can_book = browser.find_element_by_id("username")
        print("hou")
        print(can_book)
        sleep(1)
        browser.find_element_by_id("username").send_keys("Rainymood")
        browser.find_element_by_id("password").send_keys("xiaoyue21")

        sleep(1000)
        # print(browser.page_source)


if __name__ == '__main__':
    date = "2018-02-11"
    from_station = "SZQ"
    to_station = "ZZF"
    human_type = "ADULT"
    train_number = "K4426"
    seat = "无座"


    mission = Crawl(date, from_station, to_station, human_type, train_number, seat)
    mission.monitor()
