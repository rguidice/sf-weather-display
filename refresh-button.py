#!/usr/bin/env python3
from gpiozero import Button
import subprocess
import signal
import os

os.environ['DISPLAY'] = ':0'
os.environ['XAUTHORITY'] = os.path.expanduser('~/.Xauthority')

button = Button(17, pull_up=True)

def refresh():
    window = subprocess.check_output(['xdotool', 'getactivewindow']).strip()
    subprocess.run(['xdotool', 'key', '--window', window, 'ctrl+r'])

button.when_pressed = refresh
signal.pause()
