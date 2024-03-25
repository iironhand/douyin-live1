import asyncio
from asyncio.log import logger

import websockets

conns = set()
message_queue = asyncio.Queue()


# 定义处理WebSocket连接的回调函数
async def handle_client(websocket, path):
    conns.add(websocket)
    try:
        async for _ in websocket:
            pass

    except websockets.exceptions.ConnectionClosed as e:
        conns.remove(websocket)


# 启动WebSocket服务器
async def start_server():
    async with websockets.serve(handle_client, "127.0.0.1", 8888):
        print("WebSocket server is listening on :8888")
        await asyncio.Future()  # 阻塞，保持服务器运行


# 广播
async def broadcast1(message):
    if len(conns) == 0:
        return
    # await print("broadcast message:", message)
    for conn in conns:
        await conn.send(message)
