#!/usr/bin/python
 
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
            self.write_message(mpstate.status.last_heartbeat)
            time.sleep(1)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/websocket", WebSocketHandler),
])


def init(_mpstate):
    '''initialise module'''
    global mpstate
    global application
    mpstate = _mpstate
    print("Test server initialized.")
    application.listen(8888)
    tornado.ioLoop.IOLoop.instance().start()

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

