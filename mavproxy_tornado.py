#!/usr/bin/python

import threading 
import tornado.web
import tornado.websocket
import tornado.ioloop
import time
import Queue
import json
import os

server_state = None

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("lib/web_ui/index.html")
 
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        global server_State
        server_state.ws_count += 1
        server_state.websockets.append(self)
        print(server_state.ws_count)
        '''
        while True:
            if not server_state.to_client.empty():
                msg = server_state.to_client.get()
                try:
                    self.write_message(msg.to_dict())
                except:
                    # handle hard-to-convert messages
                    pass
        '''

    def on_message(self, message):
        self.write_message(u"Server echoed: " + message)

    def on_close(self):
        global server_state
        server_state.ws_count -= 1
        server_state.websockets.remove(self)
        print(server_state.ws_count)

    def send_mavlink(self, msg):
        try:
            self.write_message(msg.to_dict())
        except:
            # handle hard-to-convert messages
            pass


class ServerState():
    def __init__(self, _port):
        self.port = _port
        self.from_client = Queue.Queue(maxsize=0)
        self.to_client = Queue.Queue(maxsize=0)
        self.server_thread = None
        self.ws_count = 0
        self.websockets = [] 
        self.application = None

    def decode_mavlink(self, msg):
        result = dict()
        for field in msg._fieldnames:
            result[field] = msg.__dict__

root = os.path.dirname(__file__)
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/websocket", WebSocketHandler),], static_path=os.path.join(root, 'lib/web_ui')
)

def server_thread():
    # start server in separate thread (to maintain mavproxy function if needed)
    global application
    global server_state
    server_state.application = application
    server_state.application.listen(server_state.port)
    tornado.ioloop.IOLoop.instance().start()

def start_server(_server_state):
    global server_state
    server_state = _server_state
    server_state.server_thread = threading.Thread(target=server_thread)
    server_state.server_thread.daemon = True
    server_state.server_thread.start()

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

