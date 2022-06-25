import machine
import utime, time
import _thread

from time import sleep
from photo import Photo
from odometry import Odometry
from machine import Pin, PWM
from servo2 import Servo2
from servo import Servo
from bldc import BLDC
from IR import IRs
from ackermann import Ackermann
from tools import *


def init():
    
    global switch
    switch = Pin(0, Pin.IN, Pin.PULL_DOWN)
    
    global fan
    fan = BLDC(pin = 16)
    fan.zero()
    
    global photo
    photo = Photo(pin = 9)
    
    global ack_front, ack_back
    ack_front = Ackermann(pin_left = 27, pin_right = 26, left_zero = 93, right_zero = 90)
    ack_back = Ackermann(pin_left = 15, pin_right = 1, left_zero = 100, right_zero = 97)
    ack_front.zero()
    ack_back.zero()
    
    global IR_front, IR_back
    IR_front = IRs(pin1 = 21, pin2 = 20, pin3 = 19, pin4 = 18, pin5 = 17) #will change
    IR_back = IRs(pin1 = 14, pin2 = 13, pin3 = 12, pin4 = 11, pin5 = 10)
    
    
    global brake
    brake = Servo(pin = 7)
    brake.zero()
    
    global normal_speed, climbing_speed, low_speed, falling_speed
    normal_speed = 5.75
    climbing_speed = 5.90
    low_speed = 5.70
    falling_speed = 6.0
    
    global start_turn_distance, turn_left_distance, mid_turn_distance, end_turn_distance, falling_distance
    start_turn_distance = 100
    turn_left_distance = 530
    mid_turn_distance = 300
    end_turn_distance = 300
    falling_distance = 900

def start():
    while not switch.value():
        print('Waiting to start')
        utime.sleep(0.005)
        continue
    pass


def main():
    
    init()
    # 8th stage
    print('stage 8')
    brake.brake()
    utime.sleep(2)
#     fan.update(falling_speed)
    brake.zero()
    ack_front.zero()
    
    # 9th stage
    print('stage 9')
    
    count_f = 0
    count_b = 0
    timer = time.time()
    photo.zero()
    count = 0
    while True:
        d = photo.count_distance()
#         if d >= end_turn_distance:
#             if sum(IR_f) >= 5:
#                 count_f += 1
#             if count_f >= 1:
#                 break
        utime.sleep(0.5)
        IR_f = IR_front.values()
        IR_b = IR_back.values()
        
        for i, key in enumerate(IR_f):
            count += (i-2)*key
        print(count)
        value = count * 5
        if value >= 30:
            value = 30
        elif value < -30:
            value = -30
        ack_back.turn(value)
#         if sum(IR_b) == 0:
#             
#                 
#             if IR_f[2] == 1 :
#                 continue
#             
#             if IR_f[3] == 1 :
#                 ack_back.turn_left(10)
#                 continue
#             
#             if IR_f[1] == 1 :
#                 ack_back.turn_right(10)
#                 continue
#             
#             if IR_f[4] == 1 :
#                 ack_back.turn_left(20)
#                 continue
#             
#             if IR_f[0] == 1 :
#                 ack_back.turn_right(20)
#                 continue
        
#         if IR_b[2] == 1 :
#             continue
#         
#         if IR_b[3] == 1 :
#             ack_back.turn_right(10)
#             continue
#         
#         if IR_b[1] == 1 :
#             ack_back.turn_left(10)
#             continue
#         
#         if IR_b[4] == 1 :
#             ack_back.turn_right(20)
#             continue
#         
#         if IR_b[0] == 1 :
#             ack_back.turn_left(20)
#             continue
        
    
    # final stage
    print('final stage')
    fan.update(5.7)
    utime.sleep(1.5)
    brake.brake()
    utime.sleep(1)
    ack_front.zero()
    brake.zero()
    init()
    print('Congratulation !!')

main()

