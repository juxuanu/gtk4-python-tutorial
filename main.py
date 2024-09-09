import os
import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, Gdk, GLib, Gio  # noqa: E402

from gridmodel import File

css_provider = Gtk.CssProvider()
css_provider.load_from_path("style.css")
Gtk.StyleContext.add_provider_for_display(
    Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


class MainWindow(Gtk.ApplicationWindow):
    def show_open_dialog(self, button):
        f = Gtk.FileFilter()
        f.set_name("Image files")
        f.add_mime_type("image/png")
        f.add_mime_type("image/jpeg")
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(f)
        self.open_dialog.set_filters(filters)
        self.open_dialog.set_default_filter(f)
        self.open_dialog.open(self, None, self.open_dialog_callback)

    def open_dialog_callback(self, dialog: Gtk.FileDialog, result):
        try:
            file = dialog.open_finish(result)
            if file is not None:
                print(f"File path is {file.get_path()}")
                # ...
        except GLib.Error as error:
            print(f"Error opening the file: {error.message}")

    def on_check_toggled(self, check: Gtk.CheckButton):
        if check.get_active():
            self.button.set_label("Goodbye!")
        else:
            self.button.set_label("Hello!")

    def on_switch_state_set(self, switch, state):
        print(f"The switch state is {state} ({'on' if state else 'off'})")

    def on_slider_value_changed(self, slider):
        print(f"The slider value is {slider.get_value()}")

    def show_about(self, action, param):
        self.about.set_visible(True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(600, 250)
        self.set_title("MyApp")
        GLib.set_application_name("My App")
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)
        self.open_file_button = Gtk.Button(
            tooltip_text="Open",
            icon_name="org.example.example-symbolic",
        )
        self.open_file_button.connect("clicked", self.show_open_dialog)
        self.about = Adw.AboutWindow(
            transient_for=self,
            application_name="My App",
            version="0.0.1",
            developer_name="Ícar Nin Solana",
            license_type=Gtk.License.GPL_3_0,
            comments="Just an example, move along",
            website="https://icarns.xyz",
            issue_url="https://lmao.com",
            translator_credits="None",
            copyright="© 2024 Ícar Nin Solana",
            developers=["Ícar Nin Solana"],
            application_icon="org.example.example",
        )
        self.popover = Gtk.PopoverMenu()

        action_something = Gio.SimpleAction.new("something", None)
        action_something.connect(
            "activate", lambda signal, param: print("Something happened")
        )
        self.add_action(action_something)
        action_about = Gio.SimpleAction.new("about", None)
        action_about.connect("activate", self.show_about)
        self.add_action(action_about)

        menu = Gio.Menu.new()
        menu.append("Do something", "win.something")
        menu.append("About", "win.about")
        self.popover.set_menu_model(menu)
        self.hamburger = Gtk.MenuButton()
        self.hamburger.set_popover(self.popover)
        self.hamburger.set_icon_name("open-menu-symbolic")

        self.header.pack_start(self.open_file_button)
        self.header.pack_end(self.hamburger)

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
        self.slider = Gtk.Scale(digits=0, draw_value=True)
        self.slider.set_range(0, 10)
        self.slider.set_value(5)
        self.open_dialog = Gtk.FileDialog.new()
        self.open_dialog.set_title("Select a file")
        self.grid = Gtk.GridView()
        self.list_store = Gio.ListStore()
        for f in os.listdir("."):
            print(f, type(f))
            self.list_store.append(File(f))
        self.grid.set_model(Gtk.SingleSelection(model=self.list_store))
        factory = Gtk.SignalListItemFactory()
        factory.connect(
            "setup",
            lambda _, item: item.set_child(
                Gtk.Label(halign=Gtk.Align.START, selectable=False)
            ),
        )
        factory.connect(
            "bind", lambda _, item: item.get_child().set_label(item.get_item().name)
        )

        self.switch.connect("state-set", self.on_switch_state_set)
        self.check.connect("toggled", self.on_check_toggled)
        self.slider.connect("value-changed", self.on_slider_value_changed)

        self.set_child(self.main_box)
        self.main_box.append(self.left_box)
        self.main_box.append(self.right_box)
        self.left_box.append(self.button)
        self.left_box.append(self.check)
        self.left_box.append(self.switch_box)
        self.left_box.append(self.slider)
        self.switch_box.append(self.switch)
        self.switch_box.append(self.switch_label)
        self.right_box.append(self.grid)


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
