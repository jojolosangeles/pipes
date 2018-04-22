from websocket_server import WebsocketServer

port2socket = {}

def makeWebsocketServer(port):
    server = port2socket.get(port)
    if server == None:
        server = WebsocketServer(port)
        port2socket[port] = server
    return port2socket[port]

class WebsocketInChannel:
    def __init__(self, port):
        self.port = port

    def message_received(self, client, server, message):
        self.line_processor(message)

    def receive(self, line_processor):
        self.line_processor = line_processor
        server = makeWebsocketServer(self.port)
        server.set_fn_message_received(self.message_received)
        server.run_forever()

class WebsocketOutChannel:
    def __init__(self, port):
        self.server = makeWebsocketServer(port)

    def send(self, message):
        self.server.send_message_to_all(message)