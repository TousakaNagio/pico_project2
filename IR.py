from machine import Pin, PWM
import utime

class IRs:
    def __init__(self, pin1 = 11, pin2 = 12, pin3 = 13, pin4 = 14, pin5 = 15):
        self.sensor1 = Pin(pin1, Pin.IN, Pin.PULL_DOWN)
        self.sensor2 = Pin(pin2, Pin.IN, Pin.PULL_DOWN)
        self.sensor3 = Pin(pin3, Pin.IN, Pin.PULL_DOWN)
        self.sensor4 = Pin(pin4, Pin.IN, Pin.PULL_DOWN)
        self.sensor5 = Pin(pin5, Pin.IN, Pin.PULL_DOWN)
        
        self.sensors = []
        self.sensors.append(self.sensor1)
        self.sensors.append(self.sensor2)
        self.sensors.append(self.sensor3)
        self.sensors.append(self.sensor4)
        self.sensors.append(self.sensor5)
        
    def test(self):
        value = []
        for i in self.sensors:
            value.append(i.value())
        print(value)
        utime.sleep(0.1)
        pass
    
    def values(self):
        value = []
        for i in self.sensors:
            value.append(i.value())
        return value
#         return self.value
    
def orient(front, back):
    pass
    

# 
# def main():
#     #switch = Pin(0, Pin.IN, Pin.PULL_DOWN)
#     #sensor = Pin(15, Pin.IN, Pin.PULL_DOWN)
# #     test = IRs()
# #     test = IRs(pin1 = 21, pin2 = 20, pin3 = 19, pin4 = 18, pin5 = 17)
#     test = IRs(pin1 = 14, pin2 = 13, pin3 = 12, pin4 = 11, pin5 = 10)
#     
#     while True:
#         print(test.values())
#         #print(sensor.value())
#         utime.sleep(0.05)
#         
# main()