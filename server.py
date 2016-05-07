#!/usr/bin/python3
import time
import tornado.ioloop
import tornado.web
import tornado.websocket
import os
import sys
import mysql.connector as sql
import importlib as rl
import json
import random
import string
from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)

# we gonna store clients in dictionary..
clients = dict()
commandsL = ["r","e","l"]


def checkusr(usr, pas):
	con = sql.connect(host='localhost',user='fserver',password='easypass')
	cur = con.cursor()
	cur.execute("SELECT password FROM fserver.users WHERE name = '{0}'".format(usr))
	data = cur.fetchall ()
	print(cur.rowcount)
	for row in data :
		if row[0] == pas:
			return True
		print(row[0])
	con.close ()

def LtJS(list):
	lst = []
	for pn in list:
		d = {}
		d['mpn']=pn[0]
		d['Fdt']=pn[1]
		lst.append(d)
	return json.dumps(lst, separators=(',',':'))

class commands():
	def r(self, message):
		print("omg")
		os.execv('server.py', sys.argv)
		print ("done")
		return "done"
	def e(self, message):
		self.write_message("{0} was your message".format(message))
	def l(self, message):
		fls = []
		f = os.listdir("html/")
		i=0
		for a in f:
			st = os.stat("html/"+a)
			print(st.st_mtime)
			fls.append([a,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime))])
			i=i+1
		files = LtJS(fls)
		print(files)
		self.write_message("1:1")
		self.write_message("{0}".format(files))

def randomgen(N):
	R = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(N))
	return (R)
	
def pythonToHtml(python, self,body,css,JS):
	htmlComplete = "<!DOCTYPE html>"
	x=0
	ID=self.get_argument("I_D", True)
	for i in python:
		print(i)
		if i in sys.modules:
			module = rl.reload( sys.modules[i] )
		else:
			module = __import__(i)
		#print(module)		
		htmlComplete += module.html(body,css,JS)
	f = "{}.html".format(str(ID))
	print (ID,"hi")
	file = open(f,"w")
	file.write(htmlComplete)
	file.close()
	return f
		
class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("usr")
		
class IndexHandler(tornado.web.RequestHandler):
	def get_current_user(self):
                return self.get_secure_cookie("usr")
	@tornado.web.authenticated
	def get(self):
		SU = ["jaap"]
		name = tornado.escape.xhtml_escape(self.current_user)
		self.write("Hello, " + name)
		pythonQ = ['basepage',]
		base = ['ap']
		if name in SU:
			base = ['console','AP']
		css = []
		JS = ['JQ','console']
		f = pythonToHtml(pythonQ[:],self,base, css,JS)
		#print(open(f).read())
		self.render(f)
		
class loginHandler(BaseHandler):
	def get(self):
		pythonQ = ['basepage',]
		css = ['login.css',]
		base = ['loginB']
		JS = ['JQ','login']
		f = pythonToHtml(pythonQ[:],self,base, css,JS)
		#print(open(f).read())
		self.render(f)
	
	def post(self):
		print("A LOGIN OMG")
		name = self.get_argument("name", default=None, strip=False)
		pas = self.get_argument("pass", default=None, strip=False)
		print(name)
		print(pas)
		userOn = checkusr(name, pas)
		if userOn == True:
			print("logedin")
			self.set_secure_cookie("usr", name)
			login_response = {
				'error': False,
				'text': "you sucesfully loged in"
			}
		else:
			login_response = {
                                'error': True,
                                'text': "you r name and password do not mach our database"
                        }
		self.write(login_response)

class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def get_current_user(self):
                return self.get_secure_cookie("usr")


	@tornado.web.authenticated
	def open(self, *args):
		name = self.get_argument("I_D", True)
		if name != "undefined":
			print (name)
			print("hi")
		else:
			self.write_message("0")
			id = randomgen(40)
			self.write_message(id)
			print(id)
		
	def on_message(self, message):
		
		global commands
		ID = self.get_argument("I_D", True)
		print ("received a message from client ",ID , ": ", message)
		if message in commandsL:
			getattr(commands,message)(self,message)
		else:
			self.write_message("{0}, is not in my list".format(message))
		

	def on_close(self):
		
		if self.get_argument("I_D", True) in clients:
			del clients[self.get_argument("I_D", True)]

			
			
settings = {
	"cookie_secret": "dsnfkljdsnkfljndd;mflkdjsf",
	"login_url": "/login",
	"debug":"True",
	"xsrf_cookies": True,
}
app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/WS', WebSocketHandler),
    (r'/login', loginHandler),
], **settings)

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
