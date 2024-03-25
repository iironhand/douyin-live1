from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from twisted.internet import reactor

clients = []


class MyServerProtocol(WebSocketServerProtocol):

    def __init__(self):
        super().__init__()
        self.is_connected = True

    def onConnect(self, request):
        clients.append(self)
        print("Client connecting: {}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {} bytes".format(len(payload)))
        else:
            print("Text message received: {}".format(payload.decode("utf8")))
        # 发送回接收到的消息
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))
        self.is_connected = False
        clients.remove(self)


# 启动WebSocket服务器
def start_server():
    # 创建WebSocket服务器工厂
    factory = WebSocketServerFactory("ws://localhost:8888")
    factory.protocol = MyServerProtocol

    # 使用Twisted的reactor来运行WebSocket服务器
    reactor.listenTCP(8888, factory)
    reactor.run()


# 广播
def broadcast(message: str):
    if len(clients) == 0:
        return

    if message is None:
        print(message)
    bb = message.encode()
    for conn in clients:
        # if conn.is_connected:
        #     conn.sendMessage(bb, False)
        conn.sendMessage(bb, False)
