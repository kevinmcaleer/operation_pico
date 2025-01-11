import machine
import time

# Configure a PWM pin (adjust GPIO number as needed)
buzzer = machine.PWM(machine.Pin(15))  # GPIO 15, for example

def play_tone(frequency, duration):
    if frequency == 0:  # Rest note
        buzzer.duty_u16(0)
    else:
        buzzer.freq(frequency)
        buzzer.duty_u16(32768)  # 50% duty cycle
    time.sleep(duration)
    buzzer.duty_u16(0)  # Turn off sound
    time.sleep(0.05)    # Short pause between notes

# Notes and durations for the famous section of The Entertainer
# Format: (frequency in Hz, duration in seconds)
melody = [
    # First phrase
    (659, 0.3), (784, 0.3), (880, 0.3), (659, 0.3), (784, 0.3), (880, 0.3),
    (587, 0.3), (659, 0.3), (698, 0.3), (587, 0.3), (659, 0.3), (698, 0.3),
    (523, 0.3), (587, 0.3), (622, 0.3), (494, 0.3), (523, 0.3), (587, 0.5), (0, 0.2),

    # Second phrase
    (440, 0.3), (494, 0.3), (523, 0.3), (440, 0.3), (494, 0.3), (523, 0.3),
    (392, 0.3), (440, 0.3), (494, 0.3), (392, 0.3), (440, 0.3), (494, 0.3),
    (349, 0.3), (392, 0.3), (440, 0.3), (330, 0.3), (349, 0.3), (392, 0.5), (0, 0.2),
]

# Play the melody
for note in melody:
    frequency, duration = note
    play_tone(frequency, duration)

buzzer.deinit()  # Clean up PWM
