# -- coding: utf-8 --**
import logging
import threading

import asyncio

import local_server
from src import dy_live
from src.douyin_live_info import start_get_dy_user
from src.utils.common import init_global


def barrage(args, mloop):
    if not (len(args) >= 2 and args[1].startswith("https://live.douyin.com/")):
        raise Exception("参数错误")
    room_url = args[1]

    asyncio.set_event_loop(mloop)
    # 日志配置
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.ERROR)
    # print("记得修改config.py里面的直播地址啊，不然获取不到数据的！")
    # 初始化要做的事情：比如初始化全局变量
    init_global()
    # 推送直播点赞等数据
    # send_start()
    # 在config.py配置中修改直播地址: LIVE_ROOM_URL
    dy_live.parseLiveRoomUrl(room_url)


if __name__ == "__main__":
    # program_args = sys.argv
    # # thread = threading.Thread(target=barrage, args=(args, loop))

    loop = asyncio.new_event_loop()
    program_args = (0, "https://live.douyin.com/529701251426")
    threading.Thread(target=local_server.start_server, args=(loop,)).start()
    threading.Thread(target=start_get_dy_user, args=(program_args[1],loop)).start()

    barrage(program_args, loop)
