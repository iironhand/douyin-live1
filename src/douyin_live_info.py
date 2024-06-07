import json
import time

import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions

from local_server import broadcast1
from src.source import js


def start_get_dy_user(room_url, _loop):
    asyncio.set_event_loop(_loop)

    # 设置Edge的选项，这里可以根据需要调整，比如开启无头模式等
    edge_options = EdgeOptions()
    edge_options.add_argument("user-data-dir=c://browser_data")
    edge_options.add_argument('--disable-gpu')
    # edge_options.add_argument('--headless')
    # 如果你还需要禁用硬件加速的其他方面，可以加上以下参数
    edge_options.add_argument('--disable-software-rasterizer')
    edge_options.add_argument('--disable-webgl')
    edge_options.add_argument('--no-sandbox')  # 这个参数也可以帮助在某些受限环境中运行
    edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    edge_options.add_argument('--disable-blink-features=AutomationControlled')
    edge_options.add_argument('--enable-chrome-browser-cloud-management')

    # 创建WebDriver实例
    driver = webdriver.Edge(options=edge_options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
    driver.implicitly_wait(5)

    try:
        # 打开网页
        driver.get(room_url)

        while True:
            try:
                driver.find_element(By.CLASS_NAME, "_KRdYhzy").click()
                driver.find_element(By.XPATH, "//div[@class='uc-ui-icon-new_close_view']").click()
            except Exception as e:
                pass

            video_boxes = driver.find_elements(By.XPATH, "//div[@class='W4iHfz0m b0KSDAZ9']")

            if len(video_boxes) == 1:
                print("\r", "等待连线..", end='')
                time.sleep(1.5)
                continue

            name_map = {}
            for element in video_boxes:
                try:
                    element.click()
                    time.sleep(1)

                    user_box = driver.find_element(By.XPATH, "//div[@class='QFivDeia']")
                    img_element = user_box.find_element(By.XPATH, ".//img[@class='RlLOO79h']")
                    name_element = driver.find_element(By.XPATH, ".//div[@class='PS25Q1lw']")

                    img_src = img_element.get_attribute("src")
                    img_src = img_src.replace('100x100', '1080x1080')

                    name_map[name_element.text] = img_src

                    video_boxes[0].click()
                except Exception as e:
                    print(e)

                    break

            time.sleep(5)

            if len(name_map) != 0:
                data = {
                    "code": "1002",
                    "data": name_map
                }
                data = json.dumps(data, ensure_ascii=False)
                asyncio.run_coroutine_threadsafe(broadcast1(data), loop=asyncio.get_event_loop())
                last_map = name_map

    finally:
        driver.quit()
