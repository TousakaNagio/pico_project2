from machine import Pin, PWM
from utime import sleep
import utime

#setting: 5.5 start: 5.65

class BLDC:
    def __init__(self, pin = 10, freq = 50, step = 20, Min = 5.5*65025/100, Max = 8.5*65025/100): #1040000/2370000
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(freq)
        self.step = step
        
        self.MIN = int(Min)
        self.MAX = int(Max)
        self.turn = (self.MAX - self.MIN)//self.step
        self.duty = self.MIN
        
    
    def test_mode(self):
        while True:
            duty = float(input('Input duty cycle: '))
            self.duty = int(duty*65025/100)
            print(self.duty)
            self.pwm.duty_u16(self.duty)
            utime.sleep(0.1)
            pass
        
    def zero(self):
        self.pwm.duty_u16(self.MIN)
        
    def update(self, duty = 5.5):
        
        self.duty = int(duty*65025/100)
#         print(chrust)
        self.pwm.duty_u16(self.duty)
        utime.sleep(0.005)
        return duty
    
    def climb(self, pitch, accX):
        # 5.85可在斜坡啟動 5.75可在斜坡移動
        # 5.7可在平面啟動
        if pitch >= 3.5 and accX <= -0.7:
            #在平面
            self.duty = 5.7
            
        elif pitch < 3.5 and accX > -0.7:
            #在爬坡
            self.duty = 5.75
            
        else:
            #平均值
            self.duty = 5.7
            
        self.update(self.duty)
        pass
    
    def speed_up(self):
        self.duty += 0.01
        self.update(self.duty)
        pass
    
    def slow_down(self):
        self.duty -= 0.01
        self.update(self.duty)
        pass

# test = BLDC(pin = 16)
# test.test_mode()