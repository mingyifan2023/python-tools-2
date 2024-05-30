
# 前提得点击：开始出题
# 1 .先截图
# 2. 点击答案之后，再截图
# 3 再去点击翻页




#! -*- coding:utf-8 -*-
import datetime
import time

import pymysql
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By


from tqdm import tqdm
import time

# 使用tqdm展示进度条
for i in tqdm(range(1, 1200)):
    # 模拟一些处理时间
    time.sleep(0.01)


driver = webdriver.Chrome()
# 把find_elements 改为　find_element
def get_first_page():

    url = 'https://www.sg-siken.com/sgkakomon.php'
    driver.get(url)
    time.sleep(3)
    driver.find_element(By.XPATH,'//*[@id="configform"]/div[2]/button').click()
    time.sleep(3)
    # 截取整个页面的屏幕截图
    driver.save_screenshot("sg-img-first.png")
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="showAnswerBtn"]').click()
    time.sleep(1)
    driver.save_screenshot("sg-img-second.png")


def print_progress_percentage(current, total):
    percentage = (current / total) * 100

    # 根据进度选择颜色
    if percentage < 30:
        color_code = '\033[91m'  # 红色
    elif percentage < 60:
        color_code = '\033[93m'  # 黄色
    else:
        color_code = '\033[92m'  # 绿色

    # 输出带颜色的进度信息
    print(f"{color_code}Progress: {percentage:.2f}%\033[0m")

# 把首页和翻页处理？

def next_page():
    for i in range(1,1200):  # selenium 循环翻页成功！
        print_progress_percentage(i, 1200)
        driver.find_element(By.XPATH,'//*[@id="configform"]/div[1]/button[1]').click()
        time.sleep(1)
        # 截取整个页面的屏幕截图
        driver.save_screenshot("sg-img-{0}-1.png".format(str(i)))
        time.sleep(3)
        driver.find_element(By.XPATH, '//*[@id="showAnswerBtn"]').click()
        time.sleep(1)
        driver.save_screenshot("sg-img-{0}-2.png".format(str(i)))
        time.sleep(3)














if __name__ == '__main__':
        html = get_first_page()
        time.sleep(1)

        while True:
            next_page()




