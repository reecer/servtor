import threading, sys
import stem.process, stem.util
import tempfile, shutil, urllib2
import gobject

CONTROL_PORT = 9051

class TorConnection:
	def __init__(self, par):
		self.hs_dir = None # temp dir
		self.process = None
		self.parent = par # parent - for setting statusbar text
		self.port = 8080
		self.thread = None
		self.alive = False

	def status(self, s):
		gobject.idle_add(self.parent.status,s)


	def connect(self):
		tor_config ={
			'ControlPort': [str(CONTROL_PORT)],
		#	'ORPort': ['9001'], 
			'HiddenServiceDir': [str(self.hs_dir)],
			'HiddenServicePort': ['80 127.0.0.1:%d' % self.port]
		}
		self.status("Starting tor...")
		try:
			self.process = stem.process.launch_tor_with_config(config=tor_config)#, completion_percent=100)
		except Exception as e:
			self.status("Unable to start tor.")
			print "\n## ERROR LAUNCHING TOR ##\n", e
			sys.stdout.flush()
		else:
			self.running = True
			onion = self.get_hostname().strip()
			self.status("Tor started!")
			print onion
			# self.controller = Controller.from_port(port=CONTROL_PORT)


	def start(self, port=8080):
		"""Assumed port is int."""
		self.hs_dir = tempfile.mkdtemp(prefix="torhs_")
		self.port = port
		if self.test_localhost(port):
			# self.thread = threading.Thread(target=self.connect)
			# self.thread.start()
			self.connect()
		else:# no localhost server running
			self.status("No localhost server is running on port " + str(port))
			return False
		return True

	def stop(self):
		"""
	  	Stops the tor instance spawned by this module.
	  	"""
	  	if self.running:
		  	self.running = False
		  	if self.thread: self.thread.join()
			if self.process:self.process.kill()
		  	shutil.rmtree(path=self.hs_dir)
		self.status("Stopped.")

	def test_localhost(self, port):
		"""Returns true if localhost is running on given port"""
		self.status("Checking local server...")
		try: urllib2.urlopen("http://127.0.0.1:%d" % port)
		except urllib2.URLError as e:
			return False
		return True

	def get_hostname(self):
		if(self.hs_dir):
			return open(self.hs_dir + "/hostname", "r").read()
