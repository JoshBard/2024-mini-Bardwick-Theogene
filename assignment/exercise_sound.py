#!/usr/bin/env python3
"""
PWM Tone Generator

based on https://www.coderdojotc.org/micropython/sound/04-play-scale/
"""

import machine
import utime

# GP16 is the speaker pin
SPEAKER_PIN = 16

# create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))


def playtone(frequency: float, duration: float) -> None:
    speaker.duty_u16(1000)
    speaker.freq(frequency)
    utime.sleep(duration)


def quiet():
    speaker.duty_u16(0)


freq: float = 30
duration: float = 0.1  # seconds

print("Playing frequency (Hz):")

xprint(freq)
playtone(freq, duration)

freq = 250
print(freq)
playtone(freq, 0.15)

freq = 280
print(freq)
playtone(freq, 0.1)

freq = 320
print(freq)
playtone(freq, 0.2)

freq = 660
print(freq)
playtone(freq, 0.05)

freq = 770
print(freq)
playtone(freq, 0.05)

freq = 880
print(freq)
playtone(freq, 0.05)

freq = 990
print(freq)
playtone(freq, 0.05)

freq = 600
print(freq)
playtone(freq, 0.2)

quiet()
utime.sleep(0.1)

freq = 700
print(freq)
playtone(freq, 0.3)

freq = 800
print(freq)
playtone(freq, 0.2)

freq = 900
print(freq)
playtone(freq, 0.15)

freq = 1000
print(freq)
playtone(freq, 0.05)

freq = 1100
print(freq)
playtone(freq, 0.05)

freq = 1200
print(freq)
playtone(freq, 0.05)

quiet()
utime.sleep(0.2)

freq = 180
print(freq)
playtone(freq, 0.4)

freq = 200
print(freq)
playtone(freq, 0.3)

quiet()
utime.sleep(0.1)

freq = 1100
print(freq)
playtone(freq, 0.05)

freq = 1300
print(freq)
playtone(freq, 0.05)

freq = 1500
print(freq)
playtone(freq, 0.05)

quiet()
utime.sleep(0.3)

freq = 800
print(freq)
playtone(freq, 0.3)

freq = 600
print(freq)
playtone(freq, 0.3)

freq = 400
print(freq)
playtone(freq, 0.3)

freq = 300
print(freq)
playtone(freq, 0.4)

freq = 220
print(freq)
playtone(freq, 0.5)

# Turn off the PWM
quiet()
