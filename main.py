# -- coding: utf-8 --**
import logging
import sys
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
    logging.basicConfig(level=logging.ERROR)
    init_global()
    dy_live.parseLiveRoomUrl(room_url)


if __name__ == "__main__":
    # program_args = sys.argv
    program_args = (0, "https://live.douyin.com/250844044426")

    loop = asyncio.new_event_loop()
    threading.Thread(target=local_server.start_server, args=(loop,)).start()
    threading.Thread(target=start_get_dy_user, args=(program_args[1],loop)).start()

    barrage(program_args, loop)
