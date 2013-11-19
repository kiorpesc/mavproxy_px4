#!/usr/bin/python

import threading 
import tornado.web
import tornado.websocket
import tornado.ioloop
import time

mpstate = None

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("front.html")
 
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def on_message(self, message):
        self.write_message(u"Server echoed: " + message)
    def open(self):
        global mpstate
        while True:
            self.write_message(str(mpstate.status.last_heartbeat))
            time.sleep(1)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/websocket", WebSocketHandler),
])

def server_thread(port, _mpstate):
    # initialise module
    global mpstate
    global application
    mpstate = _mpstate
    print("Test server initialized.")
    # application stuff here?
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()

def start_server(port, _mpstate):
    server = threading.Thread(target=server_thread, args=(port, _mpstate))
    server.daemon = True
    server.start()

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

