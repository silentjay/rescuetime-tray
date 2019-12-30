import gi, cairo
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
import signal
import os
from rescuetime_wrapper import get_efficiency
from gi.repository import GObject

APPINDICATOR_ID = 'myappindicator'
CURRPATH = os.path.dirname(os.path.realpath(__file__))

class RescueTray:

    def __init__(self):
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, gtk.STOCK_INFO, appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        pulse = str(get_efficiency())
        print "pulse: %s" % pulse
        self.update_icon(pulse)
        self.old_pulse = pulse
        self.minute_milliseconds = 6000  #number of milliseconds in a minute
        
    def main(self):
        source_id = GObject.timeout_add(self.minute_milliseconds, self.update)
        gtk.main()

    def build_menu(self):
		menu = gtk.Menu()
		item_quit = gtk.MenuItem('Quit')
		item_quit.connect('activate', quit)
		menu.append(item_quit)
		menu.show_all()
		return menu

    def update_icon(self, text):
        icon_width = 20
        fresh_icon = cairo.ImageSurface(cairo.FORMAT_ARGB32, icon_width, 20) #icon  # possibly create_similar
        cr = cairo.Context(fresh_icon)
        cr.set_source_rgba(1,0.6,0,0)
        cr.rectangle(0, 0, icon_width, 20)
        cr.fill()
        cr.select_font_face('Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.move_to(0, 16)
        cr.set_font_size(15)
        if text == 'F' or int(text) < 60:
            cr.set_source_rgba(255, 0, 0, 1) # red
            print "setting icon colour to red"
        else:
            cr.set_source_rgba(0, 128, 0, 1) # green
            print "setting icon colour to green"
        cr.show_text(text)
        fresh_icon.write_to_png(CURRPATH + '/icons/' + text + 'tmp.png')
        self.indicator.set_icon(CURRPATH + '/icons/' + text + 'tmp.png')

    def update(self):
		"""This method is called everytime a tick interval occurs"""

		#Get this hour efficiency
		pulse = str(get_efficiency())
		if pulse == self.old_pulse:
		    print "pulse not changed, skipping tray update"
		    pass
		else:
		    print "updating tray icon"
		    self.old_pulse = pulse
		    self.update_icon(pulse)
		source_id = GObject.timeout_add(self.minute_milliseconds * 10, self.update)
		# return True
	 
    def quit(source):
		gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = RescueTray()
    app.main()
