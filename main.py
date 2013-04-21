#!/usr/bin/python
from gi.repository import Gtk, GObject
import urllib2
import stem, os

CNTRL_PORT = 7001

class MyWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Hello World")
		self.switch = Gtk.Switch()
		self.switch.connect("notify::active", self.switchClicked)
		self.portLabel = Gtk.Label("localhost port :")

		self.portEntry = Gtk.Entry()
		self.portEntry.set_width_chars(6)


		self.box = Gtk.Box()
		self.box.pack_start(self.portLabel, True, True, 15)
		self.box.pack_start(self.portEntry, True, True, 15)
		self.box.pack_end(self.switch, True, True, 15)
		self.add(self.box)

	def startTor(self, port):
		"""Assumed port is int."""
		if self.test_localhost(port):
			print 'Server running at localhost:%d'% port
			tor_config = {
				"HiddenServiceDir" : ".tor_us",
				"HiddenServicePort": "80 127.0.0.1:%d" % port,
				'ControlPort': str(CNTRL_PORT)
			}
			sys.stdout.write("Starting tor...")
			stem.process.launch_tor_with_config(config = tor_config, completion_percent = 5)
			sys.stdout.write("  done\n\n")
		else: # no localhost server running
			print "No localhost server is running on port %d" % port

	def stopTor(self):
		"""
	  	Stops the tor instance spawned by this module.
	  	"""
		tor_pid = stem.util.system.get_pid_by_port(CONTROL_PORT)
		if tor_pid: os.kill(tor_pid, signal.SIGTERM)

	def test_localhost(self, port):
		"""Returns true if localhost is running on given port"""
		try: 
			urllib2.urlopen("http://127.0.0.1:%d" % port)
		except Exception as e: return False
		return True

	def switchClicked(self, widget, e):
		"""
		When the switch is activated, this callback will either connect or disconnect 
		the tor connection.
		"""
		if widget.get_active():
			print "Connecting"
			port = self.portEntry.get_text()
			if not port: port = 9090
			self.startTor(port)
		else:
			print "Disconnecting"


GObject.threads_init()
win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()