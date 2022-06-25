import utime

from photo import Photo

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

def start():
    while not switch.value():
        print('Waiting to start')
        utime.sleep(0.005)
        continue
    pass

def brake(brake, ack, time = 0.05):
    brake.brake()
    ack.brake()
    utime.sleep(0.05)
    brake.zero()
    ack.zero()