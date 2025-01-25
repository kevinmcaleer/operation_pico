# Kev's Music Player
# A simple music player for MicroPython
# @Author: Kevin McAleer
# @Date: 2025-01-11

import time
import machine

# Default configurations
DEFAULT_BPM = 120
DEFAULT_TICKS = 4
DEFAULT_OCTAVE = 4
DEFAULT_DURATION = 4
ARTICULATION_MS = 10  # Gap between notes in milliseconds
DEFAULT_PIN = machine.Pin(15)

class MusicPlayer:
    def __init__(self, pin=DEFAULT_PIN, volume=100):
        self.pin = machine.PWM(pin)
        self.bpm = DEFAULT_BPM
        self.ticks = DEFAULT_TICKS
        self.last_octave = DEFAULT_OCTAVE
        self.last_duration = DEFAULT_DURATION
        self.is_playing = False
        self.volume = volume  # Volume as a percentage (0 to 100)

    def set_tempo(self, bpm=None, ticks=None):
        if bpm:
            self.bpm = bpm
        if ticks:
            self.ticks = ticks

    def get_tempo(self):
        return self.bpm, self.ticks

    def set_volume(self, volume):
        """Set the volume (0 to 100)."""
        if 0 <= volume <= 100:
            self.volume = volume
#             print(f"Volume set to {volume}%")
        else:
            raise ValueError("Volume must be between 0 and 100")

    def _play_frequency(self, freq, duration_ms):
        """Play a frequency for a given duration."""
        if freq == 0:
            self.pin.duty_u16(0)  # Mute if frequency is 0
            return
        
        # Set frequency and adjust duty cycle based on volume
        self.pin.freq(int(freq))
#         duty = int(65535 * (self.volume / 100))  # Scale duty cycle for volume
        duty = (32768)
        self.pin.duty_u16(duty)
        
        # Play the tone for the specified duration
        time.sleep_ms(duration_ms)
        
        # Stop the tone after the duration
        self.pin.duty_u16(0)

    def _note_frequency(self, note, octave):
        note_frequencies = {
            'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
            'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
            'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88,
        }
        base_frequency = note_frequencies.get(note.upper())
        if not base_frequency:
            return None
        return base_frequency * (2 ** (octave - 4))

    def play(self, notes, wait=True, loop=False):
        self.is_playing = True
        while self.is_playing:
            for note in notes:
                if not self.is_playing:
                    break
                if isinstance(note, str):
                    try:
                        note, duration = self._parse_note_string(note)
                        print(f"Parsed note: {note}, Duration: {duration}")
                    except ValueError as e:
                        print(f"Error parsing note: {note}")
                        raise e
                else:
                    raise ValueError(f"Invalid note format for {note}")
                frequency = self._note_frequency(note[0], note[1])
#                 print(f"Frequency: {frequency} Hz, Duration: {duration} beats")
                if frequency:
                    duration_ms = (60000 // self.bpm) * duration // self.ticks
                    self._play_frequency(frequency, duration_ms - ARTICULATION_MS)
                    time.sleep_ms(ARTICULATION_MS)
                else:
                    print(f"Skipping invalid frequency for note: {note}")
            if not loop:
                break
        self.is_playing = False


    def stop(self):
        self.is_playing = False
        self.pin.duty_u16(0)

    def _parse_note_string(self, note_str):
#         print(f"Parsing note string: '{note_str}'")
        if ':' not in note_str:
            raise ValueError("Note string must include duration, e.g., 'C4:4'")
        
        # Split the note and duration
        note_octave, duration = note_str.split(':')
        duration = int(duration)  # Convert duration to integer
        
#         print(f"note_octave: {note_octave}, duration: {duration}")
        
        # Extract the octave
        if len(note_octave) < 2 or not note_octave[-1].isdigit():
            raise ValueError(f"Invalid note format: {note_str}")
        octave = int(note_octave[-1])  # Last character is the octave
        
        # Extract the note
        note = note_octave[:-1]  # All characters except the last are the note
        
        # Validate note
        valid_notes = {"C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "R"}
        if note not in valid_notes:
            raise ValueError(f"Invalid note: {note}")
        
#         print(f"Parsed note: {note}, Octave: {octave}, Duration: {duration}")
        return (note, octave), duration

    def play_nintendo_on(self):
        """Recreate the Nintendo 'On' sound."""
        base_freq = 196  # G3 (Hz)
        higher_freq = 392  # G4 (Hz)

        # Play the first note
        self._play_frequency(base_freq, 300)  # Play G3 for 300 ms

        # Play the second note with fade-out
        duration = 800  # Duration of the fade-out (ms)
        steps = 20  # Number of fade-out steps
        step_duration = duration // steps

        for i in range(steps):
            # Gradually reduce volume
            fade_volume = int(65535 * (1 - i / steps))  # Scale duty cycle
            self.pin.freq(higher_freq)
            self.pin.duty_u16(fade_volume)
            time.sleep_ms(step_duration)

        # Ensure PWM stops after playing
        self.pin.duty_u16(0)

    def play_buzzer(self, freq=440, duration_ms=500, buzz_rate=50):
        """
        Play a buzzer sound.

        :param freq: Frequency of the buzz sound (default: 440 Hz).
        :param duration_ms: Total duration of the buzzing (default: 500 ms).
        :param buzz_rate: On/Off interval of the buzz in milliseconds (default: 50 ms).
        """
        # Calculate the number of buzz cycles
        cycles = duration_ms // (buzz_rate * 2)

        for _ in range(cycles):
            # Turn the sound on
            self._play_frequency(freq, buzz_rate)

            # Turn the sound off (mute)
            self.pin.duty_u16(0)
            time.sleep_ms(buzz_rate)

        # Ensure the PWM stops after buzzing
        self.pin.duty_u16(0)

# Example usage
# music = MusicPlayer(pin=machine.Pin(15))
# music.set_tempo(bpm=120)
# music.play(["C4:4", "D4:4", "E4:4", "F4:4"])
# music.stop()
