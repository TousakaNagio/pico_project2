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
from passline import PassLine

# import os
# os.rename('main.py', 'main6.py')
# os.rename('main5.py', 'main.py')

def init():
    
    global switch
    switch = Pin(0, Pin.IN, Pin.PULL_DOWN)
    
    global fan
    fan = BLDC(pin = 16)
    fan.zero()
    
    global photo
    photo = Photo(pin = 8)
    
    global ack_front, ack_back
    ack_front = Ackermann(pin_left = 27, pin_right = 26, left_zero = 93, right_zero = 90)
    ack_back = Ackermann(pin_left = 15, pin_right = 1, left_zero = 100, right_zero = 97)
    ack_front.zero()
    ack_back.zero()
    
    global IR_front, IR_back
    IR_front = IRs(pin1 = 21, pin2 = 20, pin3 = 19, pin4 = 18, pin5 = 17) #will change
    IR_back = IRs(pin1 = 14, pin2 = 13, pin3 = 12, pin4 = 11, pin5 = 10)
    
    global brake
    brake = Servo(pin = 22)
    brake.zero()
    
    global normal_speed, climbing_speed, low_speed, falling_speed
    normal_speed = 5.78
    climbing_speed = 6.55
    low_speed = 5.70
    falling_speed = climbing_speed
    
    global passline
    passline = PassLine()
    
    global start_turn_distance, turn_left_distance, mid_turn_distance, end_turn_distance, falling_distance
    start_turn_distance = 110
    turn_left_distance = 530
    mid_turn_distance = 300
    end_turn_distance = 600
    falling_distance = 900

def start():
    while not switch.value():
        print('Waiting to start')
        utime.sleep(0.005)
        continue
    pass


def main():
    
    init()
    start()
            
    
    # Stage 1
    print("Stage 1")
    fan.update(normal_speed)
    photo.zero()
    while True:
        d = photo.count_distance()
        utime.sleep(0.005)
        print(d)
        if d >= start_turn_distance:
            break
    
    # Stage 2
    print("Stage 2")
    ack_front.turn_left(beta = 23)
    fan.update(low_speed)
    
    photo.zero()
    while True:
        d = photo.count_distance()
        utime.sleep(0.005)
        print(d)
        if d >= turn_left_distance:
            break
    
    # Stage 3
    print("Stage 3")
    while True:
        utime.sleep(0.05)
        IR_f = IR_front.values()
        if sum(IR_f) == 0:
            print('Not found')
        else:
            print('Start tracking 1')
            break
    ack_front.zero()
    
    
    # Stage 4
    print("Stage 4")
    fan.update(low_speed)
    brake.brake()
    ack_front.zero()
    utime.sleep(4)
    brake.zero()
    fan.update(normal_speed)
    timer = time.time()
    
    while True:
        dt = time.time() - timer
        if dt >= 5:
            fan.update(climbing_speed)
        utime.sleep(0.005)
        IR_f = IR_front.values()
        print(IR_f)
        
        if sum(IR_f) >= 4:
            utime.sleep(0.25)
            print('pass first line')
            break
        
        if IR_f[2] == 1 :
            continue
        
        if IR_f[3] == 1 :
            ack_front.turn_right(10)
            continue
        
        if IR_f[1] == 1 :
            ack_front.turn_left(10)
            continue
        
        if IR_f[4] == 1 :
            ack_front.turn_right(20)
            continue
        
        if IR_f[0] == 1 :
            ack_front.turn_left(20)
            continue
    
#     brake.brake()
    ack_front.zero() 
#     utime.sleep(1)
    
    
    # 5th stage
    print('stage 5')
    fan.update(climbing_speed + 0.05)
    ack_front.turn_left(24)
    brake.zero()
    
    photo.zero()
    while True:
        d = photo.count_distance()
        utime.sleep(0.005)
        print(d)
        if d >= mid_turn_distance:
            break
    
    fan.update(climbing_speed - 0.50)
    brake.brake()
    utime.sleep(1)
    brake.zero()
    ack_front.zero()
    
    # 6th stage
    print('stage 6')
    fan.update(climbing_speed - 0.05)
    
    while True:
        utime.sleep(0.05)
        IR_f = IR_front.values()
        if sum(IR_f[0:3]) >= 1:
            break
        else:
            print('Not found')
    
    ack_front.turn_right(30)
    fan.update(climbing_speed + 0.1)
    photo.zero()
    while True:
        d = photo.count_distance()
        utime.sleep(0.005)
        print(d)
        if d >= mid_turn_distance - 20:
            break

    # 7th stage
    print('stage 7')
    count_b = 0
    fan.update(climbing_speed + 0.15)
    photo.zero()
    while True:
        d = photo.count_distance()
        utime.sleep(0.01)
#         print(d)
#         if d >= end_turn_distance:
#             break
        IR_f = IR_front.values()
        IR_b = IR_back.values()
        
        passline.update(IR_b)
        if passline.check():
            count_b += 1
            print("count ++")
            print(count_b)
            passline.zero()
            utime.sleep(0.1)
            
        if count_b >= 2:
            break
        
        if IR_f[2] == 1 :
            ack_front.zero()
            continue
        
        if IR_f[3] == 1 :
            ack_front.turn_right(10)
            continue
        
        if IR_f[1] == 1 :
            ack_front.turn_left(10)
            continue
        
        if IR_f[4] == 1 :
            ack_front.turn_right(20)
            continue
        
        if IR_f[0] == 1 :
            ack_front.turn_left(20)
            continue
    
    # 8th stage
    print('stage 8')
    brake.brake()
    utime.sleep(2)
    brake.zero()
    ack_front.zero()
    
    # 9th stage
    print('stage 9')
    fan.update(falling_speed)
    count_f = 0
    timer = time.time()
    photo.zero()
    passline.zero()
    while True:
        dt = time.time() - timer
        d = photo.count_distance()
        print(d)
        if d >= end_turn_distance:
            break
        utime.sleep(0.05)
        IR_f = IR_front.values()
        IR_b = IR_back.values()
        passline.update(IR_f)
        
        if passline.check():
            count_f += 1
            print("count ++")
            print(count_f)
            passline.zero()
            utime.sleep(0.1)
            
        if count_f >= 3 or dt >= 10:
            break
        
        if IR_b[2] == 1 :
            continue
        
        if IR_b[3] == 1 :
            ack_back.turn_right(10)
            continue
        
        if IR_b[1] == 1 :
            ack_back.turn_left(10)
            continue
        
        if IR_b[4] == 1 :
            ack_back.turn_right(15)
            continue
        
        if IR_b[0] == 1 :
            ack_back.turn_left(15)
            continue
        
    
    # final stage
    print('final stage')
    fan.update(5.7)
    utime.sleep(1.0)
    brake.brake()
    utime.sleep(1)
    ack_front.zero()
    brake.zero()
    init()
    print('Congratulation !!')

main()
