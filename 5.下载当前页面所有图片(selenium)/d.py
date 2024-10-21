import os
import uuid
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager



def selenium_download_img(url):


    # 创建 img 文件夹
    img_folder = 'img'
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    # 初始化 Selenium WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # 访问目标网址
    # url = 'https://veryweb.jp/fashion/731849/'  # 将此替换为你想要爬取的 URL
    driver.get(url)

    # 找到所有图片元素
    images = driver.find_elements(By.TAG_NAME, 'img')

    # 下载图片
    for idx, img in enumerate(images):
        img_url = img.get_attribute('src')

        if img_url:  # 确保 img_url 不为空
            try:
                # 生成唯一的 UUID 文件名
                img_name = str(uuid.uuid4()) + '.jpg'
                img_path = os.path.join(img_folder, img_name)

                # 下载图片
                response = requests.get(img_url)
                if response.status_code == 200:
                    with open(img_path, 'wb') as f:
                        f.write(response.content)
                    print(f'[{idx + 1}/{len(images)}] 下载完成: {img_name}')
                else:
                    print(f'[{idx + 1}/{len(images)}] 下载失败: {img_url}')
            except Exception as e:
                print(f'[{idx + 1}/{len(images)}] 出错: {e}')

    # 关闭浏览器
    driver.quit()


if __name__ == "__main__":
    url = 'https:..'  # 将此替换为你想要爬取的 URL
    selenium_download_img(url)
