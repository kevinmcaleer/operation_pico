# Operation Pico game
# @Author: Kevin McAleer
# @Date: 2025-01-11

from machine import Pin
from time import sleep
from music import MusicPlayer
from tunes import TUNES

nose = Pin(0, Pin.OUT)
contact = Pin(1, Pin.IN, Pin.PULL_UP)

nose.value(1)
sleep(0.5)
nose.value(0)
sleep(0.5)

music = MusicPlayer(pin=Pin(15))

def check_probe():
    while True:
        if contact.value() == 0:  # Pin reads LOW when connected to GND
#             print("Probe connected to GND!")
            nose.value(1)
            music.play_buzzer(freq=100, duration_ms=500, buzz_rate=50)
            sleep(0.01)
        else:
#             print("Probe not connected.")
            nose.value(0)
            music.stop()
        
        sleep(0.1)  # Check every 500ms


music.play_nintendo_on()
# music.set_volume(50)
# Play "Happy Birthday" tune
music.set_tempo(bpm=120)

music.play(TUNES["power_up"])
music.stop()

while True:
    # Run the probe check
    check_probe()