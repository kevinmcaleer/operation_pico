# Music test
# @Author: Kevin McAleer
# @Date: 2025-01-11

from music import MusicPlayer
from tunes import TUNES

# Example usage
m = MusicPlayer(pin=machine.Pin(15))
m.set_tempo(bpm=120)
m.play(TUNES["dadadadum"])
m.stop()