import sys

import gi
from gi.repository import Gtk, Adw

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")


class MainWindow(Gtk.ApplicationWindow):
    def on_check_toggled(self, check):
        if check.get_active():
            self.button.set_label("Goodbye!")
        else:
            self.button.set_label("Hello!")

    def on_switch_state_set(self, switch, state):
        print(f"The switch state is {state} ({'on' if state else 'off'})")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(600, 250)
        self.set_title("MyApp")

        self.main_box = Gtk.Box(
            margin_top=10,
            margin_bottom=10,
            margin_start=10,
            margin_end=10,
            orientation=Gtk.Orientation.HORIZONTAL,
        )
        self.left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.button = Gtk.Button(label="Hello!")
        self.check = Gtk.CheckButton(label="Or goodbye?")
        self.switch_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        self.switch = Gtk.Switch(active=True)
        self.switch_label = Gtk.Label(label="A switch")

        self.switch.connect("state-set", self.on_switch_state_set)
        self.check.connect("toggled", self.on_check_toggled)

        self.set_child(self.main_box)
        self.main_box.append(self.left_box)
        self.main_box.append(self.right_box)
        self.left_box.append(self.button)
        self.left_box.append(self.check)
        self.left_box.append(self.switch_box)
        self.switch_box.append(self.switch)
        self.switch_box.append(self.switch_label)


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.win = None
        self.connect("activate", self.on_activate)

    def on_activate(self, application):
        self.win = MainWindow(application=application)
        self.win.present()


app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)
