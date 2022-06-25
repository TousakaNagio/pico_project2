from bldc import BLDC
from machine import Pin, PWM
import utime, time

global fan
fan = BLDC(pin = 16)


# fan.test_mode()
fan.zero()