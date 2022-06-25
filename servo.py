from machine import Pin, PWM
from utime import sleep
import utime

class Servo:
    def __init__(self, pin = 15, freq = 50, step = 20):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(freq)
        self.step = step
        
        self.MIN = 1040000
        self.MAX = 1540000#2370000
        self.turn = (self.MAX - self.MIN)//self.step
    
    def update(self, ang):
        val = float(ang)
        val = int(ang/180*(self.MAX-self.MIN) + self.MIN)
        self.pwm.duty_ns(val)
        utime.sleep(0.05)
        
    
    def test_mode(self):
        while True:
            ang = float(input("Input angle: "))
            self.update(ang)
#             for i in range(self.step):
#                 self.pwm.duty_ns(self.MIN + self.turn*i)
#                 utime.sleep(0.05)
#                 
#             for i in range(self.step):
#                 self.pwm.duty_ns(self.MAX - self.turn*i)
#                 utime.sleep(0.05)
                
    def zero(self):
        ang = float(110)
        self.update(ang)
    
    def brake(self, ang = 155):
        ang = float(ang)
        self.update(ang)
        

# test = Servo(pin = 22)
# test.zero()
# utime.sleep(1)
# test.brake()
# utime.sleep(1)
# test.zero()
# test.test_mode()

