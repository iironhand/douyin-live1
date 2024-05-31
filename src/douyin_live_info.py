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
    # 指定EdgeDriver的路径，如果你已将其添加到PATH，这一步可以省略
    # edge_options.binary_location = r'C:\Path\to\msedgedriver.exe1'

    # 创建WebDriver实例
    driver = webdriver.Edge(options=edge_options)
    driver.implicitly_wait(5)
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
                    pass

            for e in name_img_map:
                print("\r", e, name_img_map[e], end='')
            time.sleep(1)

            data = {
                "code": "1002",
                "data": name_img_map
            }
            data = json.dumps(data, ensure_ascii=False)
            asyncio.run_coroutine_threadsafe(broadcast1(data),
                                             loop=asyncio.get_event_loop())

    finally:
        driver.quit()
