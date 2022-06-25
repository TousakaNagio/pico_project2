from IR import IRs
import utime

class PassLine:
    def __init__(self):
        self.queue = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        
        self.state = [0, 0, 0, 0, 0]
    
    def zero(self):
        self.queue = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        self.state = [0, 0, 0, 0, 0]
        
    def update(self, new_IR = [0, 0, 0, 0, 0]):
        temp = self.queue.pop(0)
        self.queue.append(new_IR)
        for i, key in enumerate(new_IR):
            if temp[i] == 1:
                self.state[i] -= 1
            if key == 1:
                self.state[i] += 1
    
    def check(self):
        if sum(self.queue[4]) >= 3:
            return True
        for i in self.state:
            if i == 0:
                return False
        return True
        
# test = IRs(pin1 = 21, pin2 = 20, pin3 = 19, pin4 = 18, pin5 = 17)
# Q = PassLine()
# count = 0
# while True:
#     print(test.values())
#     Q.update(test.values())
#     if Q.check():
#         count += 1
#         Q.zero()
#         utime.sleep(0.5)
#     if count >= 3:
#         break
#     #print(sensor.value())
#     utime.sleep(0.05)
