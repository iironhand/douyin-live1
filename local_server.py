import asyncio

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


def start_server(_loop):
    asyncio.set_event_loop(_loop)
    serve = websockets.serve(handle_client, "127.0.0.1", 8888)
    print("WebSocket server is listening on :8888")
    _loop.run_until_complete(serve)
    _loop.run_forever()


# 广播
async def broadcast1(message):
    if len(conns) == 0:
        return
    for conn in conns:
        await conn.send(message)
