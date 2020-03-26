
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
from server.localData import DataProcessor
from server.dateManager import DateManager
import json

import cgi

PORT_NUMBER = 8282

dataProcessor = DataProcessor()
dateManager = DateManager()

class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path = "/index.html"
		try:
			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			elif self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			elif self.path.endswith(".png"):
				mimetype='image/png'
				sendReply = True
			elif self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			elif self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			elif self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True
			elif self.path.endswith(".eot"):
				mimetype = 'application/vnd.ms-fontobject'
				sendReply = True
			elif self.path.endswith(".otf"):
				mimetype = 'application/font-sfnt'
				sendReply = True
			elif self.path.endswith(".svg"):
				mimetype = 'image/svg+xml'
				sendReply = True
			elif self.path.endswith(".ttf"):
				mimetype = 'application/font-sfnt'
				sendReply = True
			elif self.path.endswith(".woff"):
				mimetype = 'application/font-woff'
				sendReply = True
			elif self.path.endswith(".woff2"):
				mimetype = 'application/font-woff2'
				sendReply = True
			elif self.path.endswith(".ico"):
				mimetype = 'image/x-icon'
				sendReply = True
			elif self.path == '/time':
				sendReply = False
				d = dateManager.getDate()
				d['price'] = dataProcessor.getPrice()
				self.send_response(200)
				self.send_header('Content-type', 'application/json')
				self.end_headers()
				self.wfile.write(json.dumps(d))
			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + "/client" + self.path)
				self.send_response(200)
				self.send_header('Content-type', mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	#Handler for the POST requests
	def do_POST(self):
		try:
			if self.path == '/submit':
				contentType = self.headers.getheader("Content-type")
				ctype, pdict = cgi.parse_header(contentType)
				length = int(self.headers.getheader('content-length'))
				data = self.rfile.read(length)

				if ctype == "application/json":
					d = json.loads(data)
					re = dataProcessor.processData(d)
					self.send_response(200)
					self.send_header('Content-type', 'application/json')
					self.end_headers()
					try:
						self.wfile.write(json.dumps(re))
					except:
						self.wfile.write('no data')
			else:
				self.send_error(404, "No data found.")
		except Exception as inst:
			self.send_error(404, "No data found.")
			


if __name__ == "__main__":
	try:
		#Create a web server and define the handler to manage the
		#incoming request
		server = HTTPServer(('', PORT_NUMBER), myHandler)
		print 'Started httpserver on port ' , PORT_NUMBER
		
		#Wait forever for incoming htto requests
		server.serve_forever()

	except KeyboardInterrupt:
		print '^C received, shutting down the web server'
		server.socket.close()




	
