# -*- coding: utf-8 -*-
import requests
import os


class GetProvince(object):
    @staticmethod
    def get_all():
        url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9044"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                          "63.0.3239.132"" Safari/537.36"
        }

        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None

    @staticmethod
    def get_province():
        response = GetProvince.get_all().split("=")[1]
        split_data_list = response.split("|")
        split_data_list_total = len(split_data_list)
        tail = 6 - (split_data_list_total % 5) + split_data_list_total
        province_dict = dict()
        for head in range(0, tail, 5):
            try:
                simplified, abbreviation = split_data_list[head+1: head+3]
                province_dict[abbreviation] = simplified
            except ValueError as e:
                pass
                # print(e)
                # print("共{0}条, 当前查询{1}条, 抛出异常, 表示已查询完毕".format(split_data_list_total, head))
        return province_dict

    #  这里将来用数据库替换
    @staticmethod
    def output_province(path, content):
        if path[-1] != os.sep:
            path += "/"
        with open(file=path + "province.txt", mode="w", encoding="utf-8") as wf:
            wf.writelines(content)


if __name__ == '__main__':
    gp = GetProvince()
    content = gp.get_province()
    print(content)
    # gp.output_province(r"C:\Users\Administrator\Desktop", content)
