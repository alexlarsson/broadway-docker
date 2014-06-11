#!/usr/bin/gjs
const Gtk = imports.gi.Gtk;
const Gdk = imports.gi.Gdk;
const GLib = imports.gi.GLib;
const Gio = imports.gi.Gio;
const Lang = imports.lang;

// Initialize the gtk
Gtk.init(null, 0);

let screen = Gdk.Screen.get_default();
let window = new Gtk.Window ({type : Gtk.WindowType.POPUP});

// Set the window title
window.title = "Panel";
window.connect ("destroy", function(){Gtk.main_quit()});

window.set_default_size(screen.get_width(),-1);

var box = new Gtk.Box ({orientation: Gtk.Orientation.HORIZONTAL, spacing: 10});

Gio.DesktopAppInfo.set_desktop_env("GNOME");

let apps = Gio.AppInfo.get_all();

for (let i in apps) {
    let app = apps[i];

    if (app.should_show()) {
        var image = new Gtk.Image({gicon: app.get_icon()});
        var button = new Gtk.Button({label: app.get_display_name(), image: image, always_show_image: true});

        box.add(button);
        button.app = app;
        button.connect("clicked",
                       Lang.bind(button, function(button) {
                                     let app = button.app;
                                     try {
                                         let context = button.get_display().get_app_launch_context();
                                         app.launch([], context);
                                     } catch(err) {
                                         print(err);
                                     }
                                 }));
    }
}

let scroll = new Gtk.ScrolledWindow({ vexpand: true });

scroll.add(box);
window.add(scroll);

scroll.show_all();

window.show();

Gtk.main();
