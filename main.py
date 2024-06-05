# -- coding: utf-8 --**
import logging
import sys
import threading

import asyncio

import local_server
from src import dy_live
from src.douyin_live_info import start_get_dy_user
from src.utils.common import init_global


def barrage(room_url, mloop):
    asyncio.set_event_loop(mloop)
    logging.basicConfig(level=logging.ERROR)
    init_global()
    dy_live.parseLiveRoomUrl(room_url)


if __name__ == "__main__":
    args = sys.argv

    room_url = args[1]
    open_avatar_thread = args[2]

    if not args[1].startswith(r"https://live.douyin.com/"):
        print("请输入正确的房间地址")
        exit(0)

    # program_args = (0, "https://live.douyin.com/250844044426")

    loop = asyncio.new_event_loop()
    threading.Thread(target=local_server.start_server, args=(loop,)).start()

    if open_avatar_thread == "true":
        threading.Thread(target=start_get_dy_user, args=(room_url, loop)).start()

    barrage(room_url, loop)
