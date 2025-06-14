#! -*- coding:utf-8 -*-

import os
import time
import re
import xlrd
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def read_xlrd(excelFile):
    """读取Excel文件中的单词列表"""
    data = xlrd.open_workbook(excelFile)
    table = data.sheet_by_index(0)
    dataFile = []
    for rowNum in range(table.nrows):
        # 只取第一列（单词列）
        word = table.row_values(rowNum)[0]
        if isinstance(word, str) and word.strip():
            dataFile.append(word.strip())
    return dataFile


def sanitize_filename(filename):
    """移除文件名中的非法字符"""
    return re.sub(r'[\\/*?:"<>|]', "", filename)


def download_mp3(url, filepath):
    """下载MP3文件"""
    try:
        res = requests.get(url)
        res.raise_for_status()  # 检查HTTP错误

        with open(filepath, 'wb') as file:
            file.write(res.content)
        return True
    except Exception as e:
        print(f"下载失败: {str(e)}")
        return False


def create_progress_bar(progress, total, length=50):
    """创建进度条"""
    percent = progress / total
    filled_length = int(length * percent)
    bar = '█' * filled_length + '-' * (length - filled_length)
    return f"[{bar}] {percent:.1%}"


if __name__ == '__main__':
    # 设置当前工作目录
    lpath = os.getcwd()

    # 创建mps文件夹（如果不存在）
    mp3_folder = os.path.join(lpath, 'mps')
    if not os.path.exists(mp3_folder):
        os.makedirs(mp3_folder)
        print(f"已创建文件夹: {mp3_folder}")

    # 读取单词列表
    excelFile = os.path.join(lpath, 'words.xlsx')
    word_list = read_xlrd(excelFile=excelFile)
    total_words = len(word_list)

    if total_words == 0:
        print("未找到任何单词，请检查Excel文件")
        exit()

    print(f"共找到 {total_words} 个单词")

    # 设置Edge浏览器选项
    edge_options = Options()
    # edge_options.add_argument('--headless')  # 无头模式，不显示浏览器窗口
    edge_options.add_argument('--disable-gpu')
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')
    edge_options.add_argument('--log-level=3')  # 减少日志输出

    # 初始化Edge WebDriver
    driver = webdriver.Edge(options=edge_options)
    wait = WebDriverWait(driver, 10)  # 设置显式等待时间

    # 创建下载日志
    log_file = os.path.join(lpath, 'download_log.txt')
    with open(log_file, 'w', encoding='utf-8') as log:
        log.write("有道词典单词MP3下载日志\n")
        log.write(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"单词总数: {total_words}\n\n")

    success_count = 0
    failed_words = []

    print("开始处理单词...")
    print(create_progress_bar(0, total_words))

    # 处理每个单词
    for i, word in enumerate(word_list):
        word = word.strip()
        if not word:
            continue

        log_entry = f"\n单词: {word}\n"
        status = "成功"

        try:
            # 构造URL
            url = f'https://www.youdao.com/w/{word}/#keyfrom=dict2.top'
            log_entry += f"URL: {url}\n"

            # 使用Edge访问页面
            driver.get(url)

            # 等待主要内容加载完成
            wait.until(
                EC.presence_of_element_located((By.ID, "phrsListTab"))
            )

            # 获取发音链接
            try:
                # 尝试美式发音
                try:
                    audio_element = driver.find_element(
                        By.CSS_SELECTOR,
                        "#phrsListTab > h2 > div > span.pronounce > a:nth-child(2)"
                    )
                    audio_url = audio_element.get_attribute("data-rel")
                    log_entry += "使用美式发音\n"
                except NoSuchElementException:
                    # 尝试英式发音
                    audio_element = driver.find_element(
                        By.CSS_SELECTOR,
                        "#phrsListTab > h2 > div > span.pronounce > a:nth-child(1)"
                    )
                    audio_url = audio_element.get_attribute("data-rel")
                    log_entry += "使用英式发音\n"

                mp3_url = f'https://dict.youdao.com/dictvoice?audio={audio_url}'
                log_entry += f"MP3 URL: {mp3_url}\n"
            except NoSuchElementException:
                log_entry += "未找到发音链接\n"
                mp3_url = None
                status = "失败"

            # 获取词性解释
            try:
                trans_container = driver.find_element(By.CLASS_NAME, "trans-container")
                li_items = [li.text.strip() for li in trans_container.find_elements(By.TAG_NAME, "li")]
                word_info = li_items[0] if li_items else word
                log_entry += f"词性解释: {word_info}\n"
            except NoSuchElementException:
                log_entry += "未找到词性解释\n"
                word_info = word

            # 下载MP3
            if mp3_url:
                # 清理文件名
                clean_word_info = sanitize_filename(word_info[:40])
                filename = f"{word}-{clean_word_info}.mp3"
                filepath = os.path.join(mp3_folder, filename)

                # 下载文件
                if download_mp3(mp3_url, filepath):
                    log_entry += f"已保存: {filename}\n"
                    success_count += 1
                else:
                    log_entry += "MP3下载失败\n"
                    status = "失败"
            else:
                log_entry += "跳过下载，无有效的MP3链接\n"
                status = "失败"

        except TimeoutException:
            log_entry += "页面加载超时\n"
            status = "失败"
        except Exception as e:
            log_entry += f"处理时出错: {str(e)}\n"
            status = "失败"

        # 更新日志
        log_entry += f"状态: {status}\n"
        with open(log_file, 'a', encoding='utf-8') as log:
            log.write(log_entry)

        # 更新进度条
        print(f"\r{create_progress_bar(i + 1, total_words)}", end="")

        # 记录失败单词
        if status == "失败":
            failed_words.append(word)

        time.sleep(1)  # 每个单词间隔1秒

    # 关闭浏览器
    driver.quit()

    # 写入最终结果
    with open(log_file, 'a', encoding='utf-8') as log:
        log.write("\n\n===== 最终结果 =====\n")
        log.write(f"成功下载: {success_count}/{total_words}\n")
        log.write(f"失败单词: {len(failed_words)}\n")
        if failed_words:
            log.write("失败的单词列表:\n")
            for word in failed_words:
                log.write(f"- {word}\n")

    # 打印最终结果
    print("\n\n===== 处理完成 =====")
    print(f"成功下载: {success_count}/{total_words}")
    print(f"失败单词: {len(failed_words)}")
    if failed_words:
        print("失败的单词列表:")
        for word in failed_words:
            print(f"- {word}")

    print(f"\n详细日志请查看: {log_file}")
    print(f"MP3文件保存在: {mp3_folder}")

