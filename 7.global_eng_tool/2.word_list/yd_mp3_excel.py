#! -*- coding:utf-8 -*-


import datetime
import re
import os
import time
from bs4 import BeautifulSoup
import xlrd
from xlrd import xldate_as_tuple


import requests
from lxml import etree
from requests.exceptions import RequestException
from lxml import etree
# def call_page(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.text
#         return None
#     except RequestException:
#         return None
#
# def read_xlrd(excelFile):
#     data = xlrd.open_workbook(excelFile)
#     table = data.sheet_by_index(0)
#     dataFile = []
#     for rowNum in range(table.nrows):
#         dataFile.append(table.row_values(rowNum))
#     return dataFile
#
#
# def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
#     file = open(filename,'a')
#     for i in range(len(data)):
#         s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
#         s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
#         file.write(s)
#     file.close()
#     print("保存文件成功")
#
# if __name__ == '__main__':
#     lpath = os.getcwd()
#     excelFile = '{0}/mp_english.xlsx'.format(lpath)
#     full_items = read_xlrd(excelFile=excelFile)
#     for single_name in full_items:
#         print(single_name)
#         url = 'https://www.youdao.com/w/{0}/#keyfrom=dict2.top'.format(single_name[0])
#         html = call_page(url)
#         selector = etree.HTML(html)
#         mp3_c = selector.xpath('//*[@id="phrsListTab"]/h2/div/span[2]/a/@data-rel')
#         # word_info = selector.xpath('//*[@id="phrsListTab"]/div[2]')
#
#         # 解析HTML
#         soup = BeautifulSoup(html, 'html.parser')
#         # 找到trans-container div
#         trans_container = soup.find('div', class_='trans-container')
#         # 提取所有<li>标签的内容
#         li_items = [li.get_text(strip=True) for li in trans_container.find_all('li')]
#
#
#         try:
#             big_list = []
#             if len(mp3_c) != 0:
#                 for item in mp3_c:
#                     big_list.append('https://dict.youdao.com/dictvoice?audio={0}'.format(item))
#
#             for mp3_url in big_list:
#                 res = requests.get(mp3_url)
#                 time.sleep(2)
#                 music = res.content
#                 word_info = li_items[0]
#                 with open(r'{0}/{1}.mp3'.format(lpath,word_info), 'ab') as file:  # 保存到本地的文件名
#                     file.write(res.content)
#                     file.flush()
#                     time.sleep(0.3)
#         except:
#
#             pass
#

# ! -*- coding:utf-8 -*-

import datetime
import re
import os
import time
from bs4 import BeautifulSoup
import xlrd
from xlrd import xldate_as_tuple
import requests
from requests.exceptions import RequestException


def call_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def read_xlrd(excelFile):
    data = xlrd.open_workbook(excelFile)
    table = data.sheet_by_index(0)
    dataFile = []
    for rowNum in range(table.nrows):
        dataFile.append(table.row_values(rowNum))
    return dataFile


def text_save(filename, data):
    file = open(filename, 'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[', '').replace(']', '')
        s = s.replace("'", '').replace(',', '') + '\n'
        file.write(s)
    file.close()
    print("保存文件成功")


if __name__ == '__main__':
    lpath = os.getcwd()
    # 创建mps文件夹（如果不存在）
    mp3_folder = os.path.join(lpath, 'mps')
    if not os.path.exists(mp3_folder):
        os.makedirs(mp3_folder)
        print(f"已创建文件夹: {mp3_folder}")

    excelFile = '{0}\words.xlsx'.format(lpath)
    full_items = read_xlrd(excelFile=excelFile)

    for single_name in full_items:
        print(f"处理单词: {single_name[0]}")
        url = 'https://www.youdao.com/w/{0}/#keyfrom=dict2.top'.format(single_name[0])
        html = call_page(url)

        if not html:
            print(f"无法获取 {single_name[0]} 的页面内容")
            continue

        selector = etree.HTML(html)
        mp3_c = selector.xpath('//*[@id="phrsListTab"]/h2/div/span[2]/a/@data-rel')

        # 解析词性解释
        soup = BeautifulSoup(html, 'html.parser')
        trans_container = soup.find('div', class_='trans-container')
        li_items = []
        if trans_container:
            li_items = [li.get_text(strip=True) for li in trans_container.find_all('li')]
        else:
            print(f"未找到 {single_name[0]} 的词性解释")

        try:
            big_list = []
            if mp3_c:
                for item in mp3_c:
                    big_list.append('https://dict.youdao.com/dictvoice?audio={0}'.format(item))

            for index, mp3_url in enumerate(big_list):
                res = requests.get(mp3_url)
                time.sleep(2)  # 稍微减少等待时间
                word = mp3_url.split("=")[-2].split("&")[0]
                word_info = li_items[0][:40]

                # 使用单词名称作为文件名，避免使用解释中的特殊字符
                filename = f"{word}-{word_info}_{index}.mp3"
                filepath = os.path.join(mp3_folder, filename)

                with open(filepath, 'wb') as file:
                    file.write(res.content)
                print(f"已保存: {filename}")

        except Exception as e:
            print(f"处理 {single_name[0]} 时出错: {str(e)}")

