import json
import time

import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions

from local_server import broadcast1


def start_get_dy_user(room_url, _loop):
    asyncio.set_event_loop(_loop)

    # 设置Edge的选项，这里可以根据需要调整，比如开启无头模式等
    edge_options = EdgeOptions()
    edge_options.add_argument("user-data-dir=c://path.txt")
    # edge_options.add_argument('--enable-chrome-browser-cloud-management')
    # 指定EdgeDriver的路径，如果你已将其添加到PATH，这一步可以省略
    # edge_options.binary_location = r'.\msedgedriver.exe'
    # 添加禁用GPU加速的参数
    edge_options.add_argument('--disable-gpu')

    # 如果你还需要禁用硬件加速的其他方面，可以加上以下参数
    edge_options.add_argument('--disable-software-rasterizer')
    edge_options.add_argument('--disable-webgl')
    edge_options.add_argument('--no-sandbox')  # 这个参数也可以帮助在某些受限环境中运行

    # 创建WebDriver实例
    driver = webdriver.Edge(options=edge_options)
    driver.implicitly_wait(5)
    last_map = {}
    try:
        # 打开网页
        driver.get(room_url)

        while True:
            elements = driver.find_elements(By.XPATH, "//span[@class='nvmSuSNN']")
            if len(elements) == 1:
                print("\r", "等待连线..", end='')
                time.sleep(1)
                continue

            name_img_map = {}
            for element in elements[1:]:
                try:
                    element.click()
                    # 连线用户弹窗box
                    img_element = driver.find_element(By.XPATH, "//div[@class='QFivDeia']//img[1]")
                    name_element = driver.find_element(By.XPATH, "//div[@class='PS25Q1lw']")
                    img_src = img_element.get_attribute("src")
                    img_src = img_src.replace('100x100', '1080x1080')

                    name_img_map[name_element.text] = img_src
                    time.sleep(1)

                    element.click()
                except Exception as e:
                    print(e)
                    # driver.refresh()
                    break

            for e in name_img_map:
                print("\r", e, name_img_map[e], end='')
            time.sleep(10)

            if last_map != name_img_map:
                data = {
                    "code": "1002",
                    "data": name_img_map
                }
                data = json.dumps(data, ensure_ascii=False)
                asyncio.run_coroutine_threadsafe(broadcast1(data), loop=asyncio.get_event_loop())
                last_map = name_img_map



    finally:
        driver.quit()
