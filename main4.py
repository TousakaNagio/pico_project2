from machine import Pin, PWM
import utime, time
from servo2 import Servo2
from bldc import BLDC
from photo import Photo
from IR import IRs
        
    
def init():
    
    global switch
    switch = Pin(0, Pin.IN, Pin.PULL_DOWN)
    
    global photo
    photo = Photo(pin = 2)
    
    global fan
    fan = BLDC(pin = 16)
    
    global normal_speed, climbing_speed, low_speed, falling_speed
    normal_speed = 5.70+0.05
    climbing_speed = 6.15
    low_speed = 5.65+0.05
    falling_speed = 5.77+0.1
    
    global start_turn_distance, turn_left_distance, mid_turn_distance, end_turn_distance, falling_distance
    start_turn_distance = 180 #180
    turn_left_distance = 530
    mid_turn_distance = 200
    end_turn_distance = 500
    falling_distance = 900
    
    global steering
    steering = Servo2(pin = 6)
    steering.zero()
    
    global brake_l, brake_r, r_ang, l_ang, r_fall, l_fall, r_rel #left #right
    r_rel = 110
    brake_l = Servo2(pin = 3)
    brake_l.release()
    brake_r = Servo2(pin = 4)
    brake_r.release(ang = r_rel)
    r_ang = 150
    l_ang = 60
    r_fall = 110
    l_fall = 65
    
    global IR_front, IR_back
    IR_front = IRs(pin1 = 11, pin2 = 12, pin3 = 13, pin4 = 14, pin5 = 15) #will change
    IR_back = IRs(pin1 = 22, pin2 = 20, pin3 = 19, pin4 = 21, pin5 = 25)


# fan.test_mode()
    
    

def start():
    while not switch.value():
        print('Waiting to start')
        utime.sleep(0.005)
        continue
    pass

def main():
    
    init()
    start()
    
    # First step: Go ahead
    print('Stage 1')
    fan.update(normal_speed)
    photo.zero()
    while True:
        d = photo.count_distance()
        utime.sleep(0.005)
        print(d)
        if d >= start_turn_distance:
            break
    
    # Second step: Turn left
    print('Stage 2')
    fan.update(low_speed)
    for i in range(1):
        steering.turn_left(ang = 23)
    photo.zero()
    while True:
        d = photo.count_distance()
        utime.sleep(0.005)
        print(d)
        if d >= turn_left_distance:
            break
    
    # Third step: before track
    print('Stage 3')
    fan.update(normal_speed)
    
    while True:
        utime.sleep(0.05)
        IR_f = IR_front.values()
        if sum(IR_f) == 0:
            print('Not found')
        else:
            print('Start tracking 1')
            break
    steering.zero()
    
    # Forth step: track
    print('stage 4')
    
    fan.update(low_speed)
    brake_r.brake(ang = r_ang)
    brake_l.brake(ang = l_ang)
    steering.zero()
    utime.sleep(4.0)
    brake_r.release(ang = r_rel)
    brake_l.release()
    fan.update(normal_speed)
    
    timer = time.time()
    
    while True:
        dt = time.time() - timer
        if dt >= 2:
            fan.update(climbing_speed - 0.05)
        utime.sleep(0.005)
        
        IR_f = IR_front.values()
        
        if sum(IR_f) >= 3:
            utime.sleep(0.25)
            print('pass first line')
            break
        
        if IR_f[2] == 1 :
            continue
        
        if IR_f[3] == 1 :
            steering.right(5)
            continue
        
        if IR_f[1] == 1 :
            steering.left(5)
            continue
        
        if IR_f[4] == 1 :
            steering.right(10)
#             steering.right()
            continue
        
        if IR_f[0] == 1 :
            steering.left(10)
#             steering.left()
            continue
    
    steering.zero()
    fan.update(climbing_speed)
    brake_r.brake(ang = r_ang)
    brake_l.brake(ang = l_ang)
    utime.sleep(0.5)
#     utime.sleep(1)
    brake_r.release(ang = r_rel)
    brake_l.release()
        
    # 5th stage
    print('stage 5')
    fan.update(climbing_speed)
    steering.left(35)
#         utime.sleep(1)
    photo.zero()
    while True:
        d = photo.count_distance()
        utime.sleep(0.005)
        print(d)
        if d >= mid_turn_distance:
            break
    
    brake_r.brake(ang = r_ang)
    brake_l.brake(ang = l_ang)
    utime.sleep(0.5)
#     utime.sleep(1)
    brake_r.release(ang = r_rel)
    brake_l.release()
    steering.zero()
    
    
    # 6th stage
    print('stage 6')
    fan.update(climbing_speed - 0.05)
    
    while True:
        utime.sleep(0.05)
        IR_f = IR_front.values()
#         if IR_f[0] == 1:
#             break
        if sum(IR_f[0:3]) >= 1:
            break
        else:
            print('Not found')
    
    steering.right(35)
    utime.sleep(1.0)
    steering.zero()
    
    # 7th stage
    print('stage 7')
    count_f = 0
    count_b = 0
    fan.update(climbing_speed)
    photo.zero()
    while True:
        utime.sleep(0.05)
        IR_f = IR_front.values()
        IR_b = IR_back.values()
        d = photo.count_distance()
        print(d)
        
        if sum(IR_f) >= 3:
            count_f += 1
        if IR_b[1] == 1 and IR_b[3] == 1:
            count_b += 1
            utime.sleep(0.5)
#         if sum(IR_b) == 2:
#             count_b += 1
#             utime.sleep(0.5)
        if count_b >= 2:
            break
        
        if IR_f[2] == 1 :
            steering.zero()
#             utime.sleep(0.001)
            continue
        
        if IR_f[3] == 1 :
            steering.right(5)
            continue
        
        if IR_f[1] == 1 :
            steering.left(5)
            continue
        
        if IR_f[4] == 1 :
            steering.right(15)
            continue
        
        if IR_f[0] == 1 :
            steering.left(15)
            continue
    
    
    
    # 8th stage
    print('stage 8')
    brake_r.brake(ang = r_ang)
    brake_l.brake(ang = l_ang)
    utime.sleep(2)
    brake_r.release(ang = r_rel)
    brake_l.release()
    steering.zero()
    
    # 9th stage
    print('stage 9')
    fan.update(falling_speed)
    photo.zero()
    count_f = 0
    count_b = 0
    timer = time.time()
    while True:
        utime.sleep(0.03) #0.05
        IR_f = IR_front.values()
        IR_b = IR_back.values()
        d = photo.count_distance()
        print(d)

        if (d > 250 and sum(IR_f) >= 2) or dt > 7:
            brake_r.brake(ang = r_ang)
            brake_l.brake(ang = l_ang)
            utime.sleep(0.5)
            steering.zero()
            brake_r.release(ang = r_rel)
            brake_l.release()
            break
        
        if IR_b[2] == 1:
            steering.zero()
            continue
        if IR_f[2] == 1:
            steering.zero()
            continue
        
        if IR_f[0] == 1:
            steering.left(add = 10)
        if IR_f[4] == 1:
            steering.right(add = 10)
        if IR_f[1] == 1:
            steering.left(add = 5)
        if IR_f[3] == 1:
            steering.right(add = 10)
        if IR_b[1] == 1:
            steering.right(add = 10)
        if IR_b[3] == 1:
            steering.left(add = 5)
        if IR_b[3] == 1 and IR_b[1] == 1:
            steering.zero()
        
    
    # final stage
    print('final stage')
    fan.update(5.5)
    utime.sleep(1.5)
    brake_r.brake(ang = r_ang)
    brake_l.brake(ang = l_ang)
    utime.sleep(1)
    steering.zero()
    brake_r.release(ang = r_rel)
    brake_l.release()
    init()
    print('Congratulation !!')
     

     
main()

