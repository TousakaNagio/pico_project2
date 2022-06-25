import math

class Odometry:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.theta = 0
        self.L = 140
        self.l_last = 0
        self.r_last = 0
        
    def update(self, d_left = 0, d_right = 0):
        
        delta_l = d_left - self.l_last
        delta_r = d_right - self.r_last
        self.l_last = d_left
        self.r_last = d_right
        
        d_center = (delta_l + delta_r) / 2
        phi = (delta_r - delta_l) / self.L
#         phi = (delta_l - delta_r) / self.L
#         self.x += d_center * math.cos(self.theta + phi / 2)
#         self.y += d_center * math.sin(self.theta + phi / 2)
        self.x += d_center * math.cos(self.theta)
        self.y += d_center * math.sin(self.theta)
        self.theta += phi
        return self.x, self.y, self.theta
    
    def zero(self):
        self.x = 0
        self.y = 0
        self.theta = 0
        self.l_last = 0
        self.r_last = 0