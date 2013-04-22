#!/usr/bin/python
import gtk, gobject
import hidden_service


class MyWindow(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)
		self.set_size_request(200,100)
		self.switch = gtk.Button("Start")
		self.switch.connect("clicked", self.switchClicked)

		self.portLabel = gtk.Label("localhost port :")
		self.portEntry = gtk.Entry()
		self.portEntry.set_text("8080")
		self.portEntry.set_width_chars(6)
		self.statbar = gtk.Statusbar()
		self.status_id = self.statbar.get_context_id("main") # for setting status

		box = gtk.HBox()
		box.pack_start(self.portLabel)
		box.pack_start(self.portEntry)

		outmost = gtk.VBox()
		outmost.pack_start(box)
		outmost.pack_start(self.switch)
		outmost.pack_end(self.statbar)

		self.add(outmost)

		self.connect("delete-event", self.quitzies)
		self.service = hidden_service.TorConnection(self)
		self.status("Ready.")
		self.show_all()

	def status(self,status):
		msg = str(status)
		self.statbar.push(self.status_id, msg)

	def quitzies(self, a, b):
		self.turn_off()
		gtk.main_quit()

	def switchClicked(self, widget):
		"""
		When the switch is activated, this callback will either connect or disconnect 
		the tor connection.
		"""
		if widget.get_label() == "Start": 
			self.turn_on()
		else: 
			self.turn_off()

	def turn_on(self):
		self.switch.set_label("Stop")
		self.status("Starting...")
		port = int(self.portEntry.get_text())
		self.service.start(int(port))

	def turn_off(self):
		self.switch.set_label("Start")
		self.status("Stopping...")
		self.service.stop()


# gobject.threads_init()
win = MyWindow()
gtk.main()