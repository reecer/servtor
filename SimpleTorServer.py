import threading, sys, os
import urllib2
import stem.process, stem.util
from stem.util import conf

CONTROL_PORT = 9051

class Server(threading.Thread):
	def __init__(self):
		print 'inited'
		self.config = None
		self.process = None
		self.controller = None


	def startTor(self, port):
		"""Assumed port is int."""
		if self.test_localhost(port):
			print 'Server running at localhost:%d'% port
			tor_config = {
				"HiddenServiceDir" : "/home/reece/dev/soc2013/tor/onion/.tor_hs/",
				"HiddenServicePort": "80 127.0.0.1:%d" % port,
				'ControlPort': str(CONTROL_PORT),
				"ORPort" : "9001"
			}
			sys.stdout.write("Starting tor...")
			self.process = stem.process.launch_tor_with_config(config=tor_config)#, completion_percent=100)
			sys.stdout.write("done\n\n")
		else: # no localhost server running
			print "No localhost server is running on port %d" % port

	def startTor_with_config(self, path="/home/reece/dev/soc2013/tor/torrc"):
		self.config = conf.get_config("servertor")
		self.config = config.load(path)

		sys.stdout.write("Starting tor...")
		stem.process.launch_tor(torrc_path=path)#, completion_percent=100)
		sys.stdout.write("done\n\n")
		print config._contents


	def stopTor(self):
		"""
	  	Stops the tor instance spawned by this module.
	  	"""
		tor_pid = stem.util.system.get_pid_by_port(CONTROL_PORT)
		if tor_pid:
			os.kill(tor_pid, signal.SIGTERM)
			print "tor instance %d terminated"
		else: print "no tor instance found"
	def test_localhost(self, port):
		"""Returns true if localhost is running on given port"""
		try: urllib2.urlopen("http://127.0.0.1:%d" % port)
		except Exception as e: 
			print e
			return False
		return True



if __name__ == "__main__":
	s = Server()
	s.startTor(8080)