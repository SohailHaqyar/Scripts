#!/usr/bin/env python3
import gi
import sys
import time
import subprocess
import threading
import random
import os
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GLib

# Doctor Who themed warning messages
WARNING_MESSAGES = [
    "TARDIS systems detecting temporal fatigue! Rest imminent in 30 seconds",
    "Oi! Time Lord decree: mandatory rest period approaching in 30 seconds",
    "Warning: Local reality requires maintenance in 30 seconds",
    "Temporal coordinates indicate break time in 30 seconds. Wibbly wobbly timey wimey!",
    "The Angels have the computer! Look away in 30 seconds... Don't blink!",
]

# Main screen messages
LOCK_MESSAGES = [
    "Time Lord Mandatory Meditation Period. Yep. That's a thing.",
    "TARDIS Maintenance Mode Activated. Start your own maintenance mode dork.",
    "Reality Stabilization in Progress.... Please move thy fez.",
    "Temporal Recalibration Required. Meaning stop whatever you're doing. Please. Or the wee beasties will get you.",
    "Don't Blink. Don't Even Blink. Blink and you're... oh wait, you can blink. Just make sure you're stretching.",
    "Regeneration Break Initiated. No, you can't regenerate. But you can stretch.",
    "One Break a day. Keeps the weeping angels away. I know 25 minutes isn't a day on earth. But it is in some other teeny planet, Right?.",
    "Time Vortex Recharging.... Stretch or something",
    "Daleks Can't Type Passwords. You can. But you know, don't.",
    "Would You Like a Jelly Baby?. I mean, you can't have one. But you can think about it.",
]

# Early unlock messages
EARLY_UNLOCK_MESSAGES = [
    "Time streams not aligned yet",
    "Temporal coordinates still unstable",
    "The TARDIS insists you wait",
    "Even Time Lords need proper breaks",
    "Temporal paradox prevented",
]

def play_tardis_bell():
    try:
        # Use timeout to kill paplay after 5 seconds
        subprocess.Popen(['timeout', '5', 'paplay', os.path.expanduser('~/doctor-who/sound-effects/Cloister_Bell_In_The_TARDIS.mp3')])
    except FileNotFoundError:
        try:
            # Fallback to aplay with timeout
            subprocess.Popen(['timeout', '5', 'aplay', os.path.expanduser('~/doctor-who/sound-effects/Cloister_Bell_In_The_TARDIS.mp3')])
        except FileNotFoundError:
            print("No audio player found")

def create_swaylock_config():
    config_dir = os.path.expanduser("~/.config/swaylock")
    os.makedirs(config_dir, exist_ok=True)
    
    image_path = os.path.expanduser("~/Pictures/supermassive_black_hole-wallpaper-2560x1600.jpg")  # Adjust path to your image
    
    config_path = os.path.join(config_dir, "config")
    config_content = f"""
image={image_path}
scaling=fill
font=Doctor Who
indicator
indicator-radius=200
indicator-thickness=20
ring-color=003B6F
key-hl-color=005BBB
line-color=005BBB
separator-color=00000000
inside-color=00000088
inside-clear-color=00000088
inside-ver-color=00000088
inside-wrong-color=00000088
text-color=FFFFFF
text-clear-color=FFFFFF
text-caps-lock-color=FFFFFF
text-ver-color=FFFFFF
clock
text-wrong-color=FF0000
"""
    with open(config_path, "w") as f:
        f.write(config_content)

def send_notification():
    play_tardis_bell()
    subprocess.run([
        'notify-send',
        'Reminder',
        random.choice(WARNING_MESSAGES),
        '-u', 'critical',
        '-t', '25000'
    ])

class CountdownWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Time Remaining")
        self.is_relocking = False
        
        self.fullscreen()
        self.set_keep_above(True)
        self.set_decorated(False)
        
        screen = Gdk.Screen.get_default()
        css_provider = Gtk.CssProvider()
        css = """
            window {
                background: linear-gradient(rgba(0,59,111,0.95), rgba(0,91,187,0.95));
            }
            .time-label {
                color: #FFFFFF;
                font-size: 50px;
                font-weight: bold;
                text-shadow: 0 0 20px #00FFFF,
                            0 0 30px #00FFFF,
                            0 0 40px #00FFFF;
            }
            .message-label {
                color: #FFFFFF;
                font-size: 40px;
                font-weight: bold;
                text-shadow: 0 0 10px #00FFFF,
                            0 0 20px #00FFFF;
            }
            .warning-label {
                color: #FF3333;
                font-size: 30px;
                font-weight: bold;
                text-shadow: 0 0 10px #FF0000,
                            0 0 20px #FF0000;
            }
            .police-box {
                color: #FFFFFF;
                font-size: 24px;
                font-weight: bold;
            }
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=50)
        vbox.set_valign(Gtk.Align.CENTER)
        vbox.set_halign(Gtk.Align.CENTER)
        
        police_box = Gtk.Label(label="POLICE BOX")
        police_box.get_style_context().add_class("police-box")
        
        self.time_label = Gtk.Label()
        self.time_label.get_style_context().add_class("time-label")
        
        self.message_label = Gtk.Label(label=random.choice(LOCK_MESSAGES))
        self.message_label.get_style_context().add_class("message-label")
        
        self.warning_label = Gtk.Label()
        self.warning_label.get_style_context().add_class("warning-label")
        
        vbox.pack_start(police_box, True, True, 0)
        vbox.pack_start(self.time_label, True, True, 0)
        vbox.pack_start(self.message_label, True, True, 0)
        vbox.pack_start(self.warning_label, True, True, 0)
        
        self.add(vbox)
        
        self.remaining = 30
        self.update_label()
        self.warning_countdown = 0
        self.final_warning_played = False
        
        GLib.timeout_add(1000, self.update_countdown)
        GLib.timeout_add(10000, self.update_message)
        
        self.set_events(Gdk.EventMask.FOCUS_CHANGE_MASK)
        self.connect('focus-out-event', self.on_focus_out)

    def on_focus_out(self, widget, event):
        if self.remaining > 0:
            self.is_relocking = True
            self.warning_countdown = 5
            self.warning_label.set_text(f"{random.choice(EARLY_UNLOCK_MESSAGES)}\nLocking in {self.warning_countdown} seconds...")
            GLib.timeout_add(5000, self.allow_relock)
        self.present()
        return True
    
    def allow_relock(self):
        self.is_relocking = False
        return False

    def update_label(self):
        minutes = self.remaining // 60
        seconds = self.remaining % 60
        self.time_label.set_text(f"{minutes}:{seconds:02d}")
    
    def update_message(self):
        if self.remaining > 0:
            self.message_label.set_text(random.choice(LOCK_MESSAGES))
            return True
        return False
    
    def update_countdown(self):
        if self.warning_countdown > 0:
            self.warning_countdown -= 1
            self.warning_label.set_text(f"{random.choice(EARLY_UNLOCK_MESSAGES)}\nLocking in {self.warning_countdown} seconds...")
            if self.warning_countdown == 0:
                self.warning_label.set_text("")
        
        if self.remaining > 0:
            if self.remaining == 5 and not self.final_warning_played:
                play_tardis_bell()
                self.final_warning_played = True
            
            self.remaining -= 1
            self.update_label()
            return True
        else:
            self.destroy()
            return False

def check_lock(window):
    while True:
        if not window.is_relocking:
            result = subprocess.run(['pgrep', 'swaylock'], capture_output=True)
            if result.returncode != 0:
                subprocess.Popen(['swaylock'])
        time.sleep(5)

def main():
    create_swaylock_config()
    send_notification()
    time.sleep(30)
    subprocess.run(['playerctl', 'pause'])
    start_lock()

def start_lock():
    win = CountdownWindow()
    
    lock_thread = threading.Thread(target=check_lock, args=(win,), daemon=True)
    lock_thread.start()
    
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    win.present()
    
    Gtk.main()

if __name__ == "__main__":
    main()
