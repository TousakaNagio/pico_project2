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

def core1_thread():
    
    global run_core1
    global dis_l
    global dis_r
    
    from photo import Photo
    photo_l = Photo(pin = 8)
    photo_r = Photo(pin = 9)
    while True:
        while not run_core1:
            utime.sleep(0.005)
            pass
        
        print("start core1")
        dis_l = 0
        dis_r = 0
        while True:
            dis_l = photo_l.count_distance()
            dis_r = photo_r.count_distance()
            utime.sleep(0.005)
            if run_core1 == False:
                break
        photo_l.zero()
        photo_r.zero()

def init():
    
    global switch
    switch = Pin(0, Pin.IN, Pin.PULL_DOWN)
    
    global fan
    fan = BLDC(pin = 16)
    fan.zero()
    
    global ack_front, ack_back
    ack_front = Ackermann(pin_left = 27, pin_right = 26, left_zero = 90, right_zero = 93)
    ack_back = Ackermann(pin_left = 15, pin_right = 1, left_zero = 102, right_zero = 95)
    ack_front.zero()
    ack_back.zero()
    
    global IR_front, IR_back
    IR_front = IRs(pin1 = 21, pin2 = 20, pin3 = 19, pin4 = 18, pin5 = 17) #will change
    IR_back = IRs(pin1 = 10, pin2 = 11, pin3 = 12, pin4 = 13, pin5 = 14)
    
    
    global brake
    brake = Servo(pin = 7)
    brake.zero()
    
    global normal_speed, climbing_speed, low_speed, falling_speed
    normal_speed = 5.75
    climbing_speed = 6.1
    low_speed = 5.65
    falling_speed = 5.77
    
    global start_turn_distance, turn_left_distance, mid_turn_distance, end_turn_distance, falling_distance
    start_turn_distance = 120
    turn_left_distance = 500
    mid_turn_distance = 200
    end_turn_distance = 500
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
    
    global run_core1
    global dis_l
    global dis_r
    dis_l = 0
    dis_r = 0
    run_core1=False
    
    # Stage 1
    print("Stage 1")
    second_thread = _thread.start_new_thread(core1_thread, ())
    fan.update(normal_speed)
    run_core1 = True
    odo = Odometry()
    
    
    while True:
        print("core0: dis_l =", dis_l)
        print("core0: dis_r =", dis_r)
        odo.update(dis_l, dis_r)
        print("Odo: ", odo.x, " ", odo.y, " ", odo.theta)
        sleep(0.05)
        if odo.x > start_turn_distance:
            run_core1 = False
            odo.zero()
            break
    utime.sleep(0.005)
    
    # Stage 2
    print("Stage 2")
    ack_front.turn_left(beta = 20)
    fan.update(normal_speed - 0.05)
    run_core1 = True
    dis_l = 0
    dis_r = 0
    
    while True:
#         print("core0: dis_l =", dis_l)
#         print("core0: dis_r =", dis_r)
        odo.update(dis_l, dis_r)
        print("Odo: ", odo.x, " ", odo.y, " ", odo.theta)
        sleep(0.05)
        if odo.x > turn_left_distance:
            run_core1 = False
            odo.zero()
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
    brake.brake()
    ack_front.brake()
    utime.sleep(4)
    
    # Stage 4
    print("Stage 4")
    ack_front.zero()
    brake.zero()
    fan.update(normal_speed)
    timer = time.time()
    
    while True:
        dt = time.time() - timer
        if dt >= 2:
            fan.update(climbing_speed - 0.05)
        utime.sleep(0.005)
        IR_f = IR_front.values()
        print(IR_f)
        
        if sum(IR_f) == 5:
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
            ack_front.turn_left(15)
            continue
        
        if IR_f[0] == 1 :
            ack_front.turn_right(15)
            continue
    
    ack_front.zero() 
    brake.brake()
    ack_front.brake()
    utime.sleep(1)
    brake.zero()
    ack_front.zero()
    
    # 5th stage
    print('stage 5')
    fan.update(climbing_speed)
    ack_front.turn_left(20)
    
    run_core1 = True
    dis_l = 0
    dis_r = 0
    
    while True:
        odo.update(dis_l, dis_r)
        print("Odo: ", odo.x, " ", odo.y, " ", odo.theta)
        sleep(0.05)
        if odo.x > mid_turn_distance:
            run_core1 = False
            odo.zero()
            break
    brake.brake()
    ack_front.brake()
    utime.sleep(0.5)
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
    ack_front.turn_right(20)
    utime.sleep(1.0)
    ack_front.zero()

    # 7th stage
    print('stage 7')
    count_f = 0
    count_b = 0
    fan.update(climbing_speed)
    run_core1 = True
    dis_l = 0
    dis_r = 0
    while True:
        odo.update(dis_l, dis_r)
        print("Odo: ", odo.x, " ", odo.y, " ", odo.theta)
        if odo.x > mid_turn_distance:
            run_core1 = False
            odo.zero()
            break
        utime.sleep(0.05)
        run_core1 = True
        IR_f = IR_front.values()
        IR_b = IR_back.values()
        
        if sum(IR_f) >= 3:
            count_f += 1
            
        if IR_b[1] == 1 and IR_b[3] == 1:
            count_b += 1
            utime.sleep(0.5)
            
        if count_b >= 2:
            break
        
        if IR_f[2] == 1 :
            ack_front.zero()
            continue
        
        if IR_f[3] == 1 :
            ack_front.turn_right(5)
            continue
        
        if IR_f[1] == 1 :
            ack_front.turn_left(5)
            continue
        
        if IR_f[4] == 1 :
            ack_front.turn_right(15)
            continue
        
        if IR_f[0] == 1 :
            ack_front.turn_left(15)
            continue
    
    # 8th stage
    print('stage 8')
    brake.brake()
    ack_front.brake()
    utime.sleep(2)
    brake.zero()
    ack_front.zero()
    
    # 9th stage
    print('stage 9')
    fan.update(falling_speed)
    count_f = 0
    count_b = 0
    timer = time.time()
    run_core1 = True
    dis_l = 0
    dis_r = 0
    while True:
        odo.update(dis_l, dis_r)
        print("Odo: ", odo.x, " ", odo.y, " ", odo.theta)
        if odo.x > mid_turn_distance:
            run_core1 = False
            odo.zero()
            break
        utime.sleep(0.03)
        IR_f = IR_front.values()
        IR_b = IR_back.values()
        
        if (d > 250 and sum(IR_f) >= 2) or dt > 7:
            brake.brake()
            ack_front.brake()
            utime.sleep(0.5)
            ack_front.zero()
            brake.zero()
            break
        
        if IR_b[2] == 1:
            ack_front.zero()
            continue
        if IR_f[2] == 1:
            ack_front.zero()
            continue
        
        if IR_f[0] == 1:
            ack_front.turn_left(10)
        if IR_f[4] == 1:
            ack_front.turn_right(10)
        if IR_f[1] == 1:
            ack_front.turn_left(5)
        if IR_f[3] == 1:
            ack_front.turn_right(10)
        if IR_b[1] == 1:
            ack_front.turn_right(10)
        if IR_b[3] == 1:
            ack_front.turn_left(5)
        if IR_b[3] == 1 and IR_b[1] == 1:
            ack_front.zero()
        
    
    # final stage
    print('final stage')
    fan.update(5.5)
    utime.sleep(1.5)
    brake.brake()
    utime.sleep(1)
    ack_front.zero()
    brake.zero()
    init()
    print('Congratulation !!')

main()
    


