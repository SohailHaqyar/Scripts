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

# # Doctor Who themed warning messages
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

def play_tardis_sound():
    # Using paplay for PulseAudio or aplay for ALSA
    try:
        # Try PulseAudio first
        subprocess.Popen(['paplay', os.path.expanduser('~/doctor-who/sound-effects/Cloister_Bell_In_The_TARDIS.mp3')])
    except FileNotFoundError:
        try:
            # Try ALSA if PulseAudio not available
            subprocess.Popen(['aplay', os.path.expanduser('~/doctor-who/sound-effects/Cloister_Bell_In_The_TARDIS.mp3')])
        except FileNotFoundError:
            print("No audio player found")

def create_swaylock_config():
    # Create config directory if it doesn't exist
    config_dir = os.path.expanduser("~/.config/swaylock")
    os.makedirs(config_dir, exist_ok=True)
    
    # Use your existing TARDIS image
    image_path = os.path.expanduser("~/doctor-who/space_love.jpg")  # Adjust path to your image
    
    # Create swaylock config
    config_path = os.path.join(config_dir, "config")
    config_content = f"""
image={image_path}
scaling=fill
font=Doctor Who
indicator
clock
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
text-wrong-color=FF0000
"""
    with open(config_path, "w") as f:
        f.write(config_content)

def send_notification():
    # Play TARDIS bell sound with notification
    play_tardis_sound()
    subprocess.run([
        'notify-send',
        '🌀 TARDIS Alert System 🌀',
        random.choice(WARNING_MESSAGES),
        '-u', 'critical',
        '-t', '2500'
    ])

def main():
    # Create swaylock config
    create_swaylock_config()
    
    # Send warning notification with sound
    send_notification()
    
    # Wait 30 seconds
    time.sleep(3)
    # Start the lock screen
    start_lock()

def start_lock():
    class CountdownWindow(Gtk.Window):
        def __init__(self):
            super().__init__(title="Time Remaining")
            
            self.fullscreen()
            self.set_keep_above(True)
            self.set_decorated(False)
            
            # TARDIS/Doctor Who themed CSS
            screen = Gdk.Screen.get_default()
            css_provider = Gtk.CssProvider()
            css = """
                window {
                    background: linear-gradient(rgba(0,59,111,0.95), rgba(0,91,187,0.95));
                }
                .time-label {
                    color: #FFFFFF;
                    font-size: 150px;
                    font-weight: bold;
                    text-shadow: 0 0 20px #00FFFF,
                                0 0 30px #00FFFF,
                                0 0 40px #00FFFF;
                }
                .message-label {
                    color: #FFFFFF;
                    font-size: 80px;
                    font-weight: bold;
                    text-shadow: 0 0 10px #00FFFF,
                                0 0 20px #00FFFF;
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
            
            vbox.pack_start(police_box, True, True, 0)
            vbox.pack_start(self.time_label, True, True, 0)
            vbox.pack_start(self.message_label, True, True, 0)
            
            self.add(vbox)
            
            self.remaining = 60
            self.update_label()
            
            # Play sound at specific intervals
            self.sound_times = {60, 30, 10, 5, 4, 3, 2, 1}
            
            GLib.timeout_add(1000, self.update_countdown)
            GLib.timeout_add(10000, self.update_message)
            
            self.set_events(Gdk.EventMask.FOCUS_CHANGE_MASK)
            self.connect('focus-out-event', self.on_focus_out)

        def on_focus_out(self, widget, event):
            self.present()
            return True
        
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
            if self.remaining > 0:
                # Play sound at specific times
                if self.remaining in self.sound_times:
                    play_tardis_sound()
                
                self.remaining -= 1
                self.update_label()
                return True
            else:
                play_tardis_sound()  # Play sound when finished
                self.destroy()
                return False

    def check_lock():
        while True:
            result = subprocess.run(['pgrep', 'swaylock'], capture_output=True)
            if result.returncode != 0:
                subprocess.Popen(['swaylock'])
            time.sleep(1)

    subprocess.Popen(['swaylock'])
    
    lock_thread = threading.Thread(target=check_lock, daemon=True)
    lock_thread.start()
    
    win = CountdownWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    win.present()
    
    Gtk.main()

if __name__ == "__main__":
    main()
