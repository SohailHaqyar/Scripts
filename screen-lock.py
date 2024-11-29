#!/usr/bin/env python3
import gi
import sys
import time
import subprocess
import threading
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GLib

class CountdownWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Time Remaining")
        
        # Set window to fullscreen
        self.fullscreen()
        self.set_keep_above(True)
        
        # Make window borderless
        self.set_decorated(False)
        
        # Style the window
        screen = Gdk.Screen.get_default()
        css_provider = Gtk.CssProvider()
        css = """
            window {
                background-color: #000000;
            }
            .time-label {
                color: white;
                font-size: 250px;
                font-weight: bold;
                font-family: "Inter";
            }
            .message-label {
                color: white;
                font-size: 80px;
                font-weight: bold;
                font-family: "Inter";
            }
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        # Create vertical box for layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=50)
        vbox.set_valign(Gtk.Align.CENTER)
        vbox.set_halign(Gtk.Align.CENTER)
        
        # Create labels with style classes
        self.time_label = Gtk.Label()
        self.time_label.get_style_context().add_class("time-label")
        
        self.message_label = Gtk.Label(label="Take a break!")
        self.message_label.get_style_context().add_class("message-label")
        
        # Add labels to box
        vbox.pack_start(self.time_label, True, True, 0)
        vbox.pack_start(self.message_label, True, True, 0)
        
        # Add box to window
        self.add(vbox)
        
        # Initialize countdown
        self.remaining = 60
        self.update_label()
        
        # Start countdown timer
        GLib.timeout_add(1000, self.update_countdown)
        
        # Ensure window stays on top in Hyprland
        self.set_events(Gdk.EventMask.FOCUS_CHANGE_MASK)
        self.connect('focus-out-event', self.on_focus_out)

    def on_focus_out(self, widget, event):
        self.present()
        return True
    
    def update_label(self):
        minutes = self.remaining // 60
        seconds = self.remaining % 60
        self.time_label.set_text(f"{minutes}:{seconds:02d}")
    
    def update_countdown(self):
        if self.remaining > 0:
            self.remaining -= 1
            self.update_label()
            return True
        else:
            self.destroy()
            return False

def check_lock():
    while True:
        # Check if swaylock is running
        result = subprocess.run(['pgrep', 'swaylock'], capture_output=True)
        if result.returncode != 0:
            # If swaylock isn't running, start it
            subprocess.Popen(['swaylock'])
        time.sleep(1)

def main():
    # Start swaylock
    subprocess.Popen(['swaylock'])
    
    # Start lock checker in a separate thread
    lock_thread = threading.Thread(target=check_lock, daemon=True)
    lock_thread.start()
    
    # Create and show countdown window
    win = CountdownWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    
    # Ensure it's focused and on top
    win.present()
    
    Gtk.main()

if __name__ == "__main__":
    main()
