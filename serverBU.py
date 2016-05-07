
import tornado.ioloop
import tornado.web
import tornado.websocket

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)

# we gonna store clients in dictionary..
clients = dict()


def pythonToHtml(python):
	htmlComplete = "<!DOCTYPE html>"
	x=0
	for i in python:
		
		module = __import__(i)
		#import i as module
		print (module.html())
		#htmlComplete += module.html()
		print (htmlComplete,"hi")
		x+=1
		
		
class IndexHandler(tornado.web.RequestHandler):
	#@tornado.web.asynchronous
	def get(self):
		pythonQ = ['html1',]
		pythonToHtml(pythonQ[:])
		self.render('index.html')
        
		
class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self, *args):
		print (self.get_argument("I_D", True))
		
	def on_message(self, message):
		ID = self.get_argument("I_D", True)
		print (ID)
		print ("Client ",ID ,"received a message : ", message)
        #print ("Client %s received a message : %s") % (self.get_argument("I_D", True), message)

	def on_close(self):
		if self.get_argument("I_D", True) in clients:
			del clients[self.get_argument("I_D", True)]

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/WS', WebSocketHandler),
])

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()