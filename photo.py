from machine import Pin
import time, utime
import math

class Photo:
    def __init__(self, pin = 2):
        
        self.light_in_pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        self.wheel_d = 60
        self.hole = 20
        self.distance = 0
        self.is_light = 0
        self.delta_d = 0
    
    def count_distance(self):
        
        start_time = time.time()
        
        if self.light_in_pin.value() == 0 and self.is_light == 0:
            self.delta_d = (math.pi) * self.wheel_d / self.hole
            self.distance += self.delta_d
            time1 = time.time()
            self.is_light = 1
        elif self.light_in_pin.value() == 1 and self.is_light == 1:
            self.is_light = 0
        
        return self.distance
    
    
    def zero(self):
        self.distance = 0

# photo = Photo(pin = 9)
# while True:
#     d = photo.count_distance()
#     utime.sleep(0.005)
#     print(d)
#     if d >= 100:
#         break
# print('fuck you')