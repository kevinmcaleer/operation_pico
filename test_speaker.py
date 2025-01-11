# @Author: Kevin McAleer
# @Date: 2025-01-11

from machine import PWM, Pin

# Check PWM capability of GPIO15
pwm = PWM(Pin(15))
pwm.freq(1000)
pwm.duty_u16(32768)
print("PWM initialized on GPIO15 with 1 kHz frequency and 50% duty cycle.")
