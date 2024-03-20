import asyncio
import json

import websockets

conns = set()


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
    async with websockets.serve(handle_client, "localhost", 8888):
        print("WebSocket server is listening on localhost:8888")
        await asyncio.Future()  # 阻塞，保持服务器运行


# 广播
async def broadcast(message):
    if len(conns) == 0:
        return

    err_conn_set = set()

    for conn in conns:
        try:
            await conn.send(json.dumps(message, ensure_ascii=True))
            await asyncio.sleep(0)

        except websockets.exceptions.ConnectionClosed as e:
            err_conn_set.add(conn)
    # 删除无效的链接
    conns.difference_update(err_conn_set)
