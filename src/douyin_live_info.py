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

    # 指定EdgeDriver的路径，如果你已将其添加到PATH，这一步可以省略
    # edge_options.binary_location = r'C:\Path\to\msedgedriver.exe1'

    # 创建WebDriver实例
    driver = webdriver.Edge(options=edge_options)
    driver.implicitly_wait(5)
    try:
        # 打开网页
        driver.get(room_url)

        # 获取网页标题并打印
        print("网页标题是：", driver.title)
        while True:
            elements = driver.find_elements(By.XPATH, "//span[@class='nvmSuSNN']")
            name_img_map = {}

            for element in elements:
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
                    # print(e)

            time.sleep(3)
            print("-------------------")
            for e in name_img_map:
                print(e, name_img_map[e])

            data = {
                "code": "1002",
                "data": name_img_map
            }
            data = json.dumps(data, ensure_ascii=False)
            asyncio.run_coroutine_threadsafe(broadcast1(data),
                                             loop=asyncio.get_event_loop())



    # 这里可以根据需要添加更多的自动化操作，如查找元素、点击等

    finally:
        # 完成后记得关闭浏览器窗口
        driver.quit()
