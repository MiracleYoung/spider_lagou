#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/1 下午9:56
# @Author  : MiracleYoung
# @File    : app.py



import time
import xlsxwriter
import datetime
import requests
import random


def get_page(url, pn, kd):
    tag = 'true' if pn == 1 else 'false'
    headers = {
        'Host': 'www.lagou.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Connection': 'keep-alive',
        # 'Content-Type': 'application / x - www - form - urlencoded;charset = UTF - 8',
        'Referer': 'https://www.lagou.com/jobs/list_{}?labelWords=&fromSearch=true&suginput='.format(kd),
        # 'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://www.lagou.com'
    }

    data = {
        'first': tag,
        'pn': pn,
        'kd': kd
    }
    page = requests.post(url, data=data, headers=headers).json()
    return page


def get_info(page, tag):
    page_json = page['content']['positionResult']['result']
    page_result = [num for num in range(15)]
    # 一个页面 15个岗位
    for i in range(15):
        page_result[i] = []
        for page_tag in tag:
            page_result[i].append(page_json[i].get(page_tag))
        page_result[i][8] = ','.join(page_result[i][8])
    return page_result


def read_max_page(page):
    max_page_num = page['content']['pageSize']
    if max_page_num > 30:
        max_page_num = 30
    return max_page_num


def save_excel(fin_result, tag_name, file_name):
    book = xlsxwriter.Workbook('./{}.xls'.format(file_name))
    tmp = book.add_worksheet()
    row_num = len(fin_result)
    for i in range(1, row_num):
        if i == 1:
            tag_pos = 'A{}'.format(i)
            tmp.write_row(tag_pos, tag_name)
        else:
            con_pos = 'A{}'.format(i)
            content = fin_result[i - 1]  # -1是因为被表格的表头所占
            tmp.write_row(con_pos, content)
    book.close()


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    url = r'https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false'
    tag = ['companyFullName', 'district', 'positionName', 'workYear', 'salary', 'financeStage', 'companySize',
           'industryField', 'companyLabelList']
    tag_name = ['公司名称', '地区', '职位名称', '工作年限', '工资', '公司资质', '公司规模', '所属类别', '福利']

    print('即将进行抓取'.center(50, '*'))
    keyword = input('请输入您要搜索的职位信息：')
    fin_result = []
    # max_page_num = read_max_page(get_page(url, 1, keyword))
    max_page_num = 4
    for page_num in range(1, max_page_num):
        print('正在下载第{}页内容'.format(page_num).center(50, '*'))
        page = get_page(url, page_num, keyword)
        page_result = get_info(page, tag)
        fin_result.extend(page_result)
        time.sleep(random.randint(1, 5))
    file_name = input('抓去完成，输入文件名保存：')
    save_excel(fin_result, tag_name, file_name)
    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds
    print('共用时：{} s'.format(time))
