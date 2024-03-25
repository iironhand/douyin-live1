import _thread
import asyncio
import logging
import sys

from local_server import start_server
from src import dy_live
from src.utils.common import init_global
from src.utils.http_send import send_start

if __name__ == "__main__":
    _thread.start_new_thread(asyncio.run, (start_server(),))

    args = sys.argv

    if not (len(args) >= 2 and args[1].startswith("https://live.douyin.com/")):
        raise Exception("参数错误")

    # 日志配置
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.ERROR)
    print("记得修改config.py里面的直播地址啊，不然获取不到数据的！")
    # 初始化要做的事情：比如初始化全局变量
    init_global()
    # 推送直播点赞等数据
    send_start()
    # 在config.py配置中修改直播地址: LIVE_ROOM_URL
    dy_live.parseLiveRoomUrl(sys.argv[1])
