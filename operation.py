# Operation Pico game
# @Author: Kevin McAleer
# @Date: 2025-01-11

from machine import Pin
from time import sleep
from music import MusicPlayer
from tunes import TUNES

nose = Pin(0, Pin.OUT)
# buzzer = Pin(15, Pin.OUT)
contact = Pin(1, Pin.IN, Pin.PULL_UP)

nose.value(1)
# buzzer.value(1)
sleep(0.5)
nose.value(0)
# buzzer.value(1)
sleep(0.5)

# TUNES = {
#     "dadadadum": [
#         "R4:2", "G4:1", "G4:1", "G4:1", "Eb4:8", "R4:2", "F4:1", "F4:1",
#         "F4:1", "D4:8",
#     ],
#     "entertainer": [
#         "D4:1", "D#:1", "E4:1", "C5:2", "E4:1",
#         "C5:2", "E4:1", "C5:3", "C4:1", "D4:1",
#         "D#:1", "E4:1", "C4:1", "D4:1", "E4:2", "B4:1", "D5:2",
#         "C4:4",
#     ],
# }

music = MusicPlayer(pin=Pin(15))
music.set_volume(1)
# Play "Happy Birthday" tune
music.set_tempo(bpm=120)

music.play(TUNES["dadadadum"])
music.stop()


def check_probe():
    while True:
        if contact.value() == 0:  # Pin reads LOW when connected to GND
            print("Probe connected to GND!")
        else:
            print("Probe not connected.")
        
        sleep(0.25)  # Check every 500ms

# while True:
#     # Run the probe check
#     check_probe()