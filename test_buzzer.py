# Buzzer Test
# @Author: Kevin McAleer
# @Date: 2025-01-11

from time import sleep
#Configure a PWM pin (adjust GPIO number as needed)
buzzer = machine.PWM(machine.Pin(15))  # GPIO 15, for example

def play_tone(frequency, duration):
    buzzer.freq(frequency)
    buzzer.duty_u16(32768)  # 50% duty cycle
    sleep(duration)
    buzzer.duty_u16(0)  # Turn off sound
    sleep(0.05)

# Example melody
play_tone(440, 0.5)  # A4 for 0.5 seconds
play_tone(523, 0.5)  # C5 for 0.5 seconds
play_tone(659, 0.5)  # E5 for 0.5 seconds

buzzer.deinit()  # Clean up PWM