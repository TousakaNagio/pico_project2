from machine import Pin, PWM
from utime import sleep
import utime

class Servo2:
    def __init__(self, pin = 6, freq = 50, step = 36, zero = 95):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(freq)
        self.step = step
        
        self.MIN = 1350
        self.MAX = 8200
        self.turn = (self.MAX - self.MIN)//self.step
        self.CUR = (self.MIN+self.MAX)//2
        self.ang = zero
        self.zero_ang = zero
        
    
    def test_mode(self):
        while True:
            for i in range(self.step//2):
                self.pwm.duty_u16(self.MIN + self.turn*i)
                utime.sleep(0.05)
                
            for i in range(self.step):
                #self.pwm.duty_u16(self.MAX - self.turn*i)
                utime.sleep(0.05)
                
    def test_mode2(self):
        while True:
            ang = float(input("Input angle: "))
            self.CUR = int(ang/180*(self.MAX-self.MIN) + self.MIN)
            print(self.CUR)
            self.pwm.duty_u16(self.CUR)
            utime.sleep(0.5)
    
    def update(self, ang=95):
        self.ang = float(ang)
        self.CUR = int(self.ang/180*(self.MAX-self.MIN) + self.MIN)
        self.pwm.duty_u16(self.CUR)
    
    def zero(self):
        self.ang = self.zero_ang
        self.update(self.ang)
        utime.sleep(0.005)
    
    def target(self, tar):
        
        print(tar)
        
        if tar < 0:
            self.CUR = self.MIN
            self.pwm.duty_u16(self.CUR)
            utime.sleep(0.005)
        elif (tar > 180):
            self.CUR = self.MAX
            self.pwm.duty_u16(self.CUR)
            utime.sleep(0.005)
        else:
            tar = tar // 5
            print(tar)
            self.CUR = self.MIN + self.turn * tar
            print(self.CUR)
            self.pwm.duty_u16(int(self.CUR))
            utime.sleep(0.005)
            
    def turn_right(self, ang = 25):
        self.ang += ang
        self.update(self.ang)
        utime.sleep(0.001)
        
    def turn_left(self, ang = 25):
        self.ang -= ang
        self.update(self.ang)
        utime.sleep(0.001)
    
    def right(self, add = 15):
        self.ang = self.zero_ang + add
        self.update(self.ang)
        utime.sleep(0.001)
        
    def left(self, add = 15):
        self.ang = self.zero_ang - add
        self.update(self.ang)
        utime.sleep(0.001)
        
    def brake(self, ang = 55):
        self.ang = ang
        self.update(self.ang)
        utime.sleep(0.005)
        
    def release(self, ang = 90):
        self.ang = ang
        self.update(self.ang)
        utime.sleep(0.005)

# test = Servo2(pin = 14)
# test.zero()
# test.test_mode2()
# test.turn_right()
# test.turn_right()
# test.turn_left()
# test.turn_left()
# test.test_mode2()
# left_brake = Servo2(pin = 4)
# left_brake.brake()
# utime.sleep(1)
# left_brake.release()
# left_brake.zero()
# left_brake.test_mode2()
# left_brake.turn_right()
# right_brake = Servo2(pin = 5)
# right_brake.zero()
