import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

def on_activate(application):
    win = Gtk.ApplicationWindow(application=application)
    win.present()

app = Gtk.Application()
app.connect('activate', on_activate)

app.run(None)