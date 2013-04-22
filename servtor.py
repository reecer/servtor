import threading, sys, os
import urllib2
import stem.process, stem.util
from stem.util import conf
from stem.control import Controller
import shutil, tempfile

import SimpleHTTPServer, BaseHTTPServer
import SocketServer

CONTROL_PORT = 9051

class Server:
	def __init__(self, port=8080, path=""):
		self.port = port
		self.running = False
		self.thread = None
		self.server = None
		# self.set_path(os.getcwd())

	def set_path(self, path):
		self.path = path
		os.chdir(path)

	def start(self,port):
		self.running = True
		handler = SimpleHTTPServer.SimpleHTTPRequestHandler
		self.server = SocketServer.TCPServer(("", self.port), handler)
		self.thread = threading.Thread(target=self.server.serve_forever)
		self.thread.setDaemon(True)
		self.thread.start()

	def stop(self):
		self.running = False
		self.server.shutdown()
		self.thread.join()
		print "Server stopped"

class TorConnection(threading.Thread):
	def __init__(self):
		self.hs_dir = tempfile.mkdtemp(prefix=".tor_hs")
		self.process = None
		self.controller = None
		self.running = False

	def run(self):
		self.running = True
		while self.running:
			pass#sys.stdout.flush()

	def start(self, port=8080):
		"""Assumed port is int."""
		if self.test_localhost(port):
			print 'Server running at localhost:%d'% port
			print "hs_dir = " , self.hs_dir
			tor_config ={
				'ControlPort': [str(CONTROL_PORT)],
			#	'ORPort': ['9001'], 
				'HiddenServiceDir': [str(self.hs_dir)],
				'HiddenServicePort': ['80 127.0.0.1:%d' % port]
			}
			sys.stdout.write("Starting tor...")
			self.process = stem.process.launch_tor_with_config(config=tor_config)#, completion_percent=100)
			sys.stdout.write("tor started!\n\n")
			self.controller = Controller.from_port(port=CONTROL_PORT)
			print self.get_hostname()
		else: # no localhost server running
			print "No localhost server is running on port %s" % port
		return

	def stop(self):
		"""
	  	Stops the tor instance spawned by this module.
	  	"""
	  	if not self.process: return
	  	self.running = False
		self.process.kill()
	  	shutil.rmtree(path=self.hs_dir)
		print "Process stopped"

	def test_localhost(self, port):
		"""Returns true if localhost is running on given port"""
		try: urllib2.urlopen("http://127.0.0.1:%d" % port)
		except Exception as e: 
			print e
			return False
		return True

	def get_hostname(self):
		if(self.hs_dir):
			return open(self.hs_dir + "/hostname", "r").read()


if __name__ == "__main__":
	print "Starting..."
	port = 8080
	s = Server(port)
	s.start()
	print "Started server"

	tconn = TorConnection(port)
	tconn.start()
	print "Started tconn"
