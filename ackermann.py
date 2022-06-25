from servo2 import Servo2
import utime
import math

class Ackermann:
    def __init__(self, pin_left = 1, pin_right = 2, left_zero = 95, right_zero = 95):
        
        self.left = Servo2(pin = pin_left, zero = left_zero)
        self.right = Servo2(pin = pin_right, zero = right_zero)
        self.left.zero()
        self.right.zero()
        
        self.K = 140
        self.L = 220
        
    def zero(self):
        self.left.zero()
        self.right.zero()
    
    def test_mode(self):
        while True:
            ang = int(input("Input angle: "))
            if ang == 0:
                self.zero()
            elif ang > 0:
                self.turn_left(ang)
            else:
                self.turn_right(-ang)
            
        pass
    
    def turn(self, ang = 0):
        if ang == 0:
            pass
        elif ang > 0:
            self.turn_right(ang)
        else:
            self.turn_left(-ang)
    
    def turn_left(self, beta = 0):
        if beta == 0:
            self.zero()
        else:
            alpha = math.degrees(math.atan(1 / (1 / math.tan(math.radians(beta)) - self.K / self.L)))
            self.left.left(add = alpha)
            self.right.left(add = beta)
    
    def turn_right(self, beta = 0):
        if beta == 0:
            self.zero()
        else:
            alpha = math.degrees(math.atan(1 / (1 / math.tan(math.radians(beta)) - self.K / self.L)))
            self.left.right(add = beta)
            self.right.right(add = alpha)
    
    def brake(self):
        self.left.right(add = 45)
        self.right.left(add = 45)

# arc = Ackermann(pin_left = 27, pin_right = 26, left_zero = 93, right_zero = 90) #front
# arc = Ackermann(pin_left = 15, pin_right = 1, left_zero = 100, right_zero = 97) #back
# arc.zero()
# arc.brake()
# utime.sleep(2)
# arc.zero()
# arc.test_mode()

# left = Servo2(pin = 0)
# right = Servo2(pin = 1)
# left.zero()
# right.zero()
        