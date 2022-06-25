import machine
from time import sleep
import _thread
from photo import Photo
from odometry import Odometry
import utime

def core1_thread(distance):
    global run_core1
    #global counter
    global dis_l
    global dis_r
    from photo import Photo
    while not run_core1:
        pass
    
    print("start core1")
    #counter = 0
    dis_l = 0
    dis_r = 0
    photo_l = Photo(pin = 8)
    photo_r = Photo(pin = 9)
    while True:
        dis_l = photo_l.count_distance()
        dis_r = photo_r.count_distance()
        utime.sleep(0.005)
        #counter += 1
        if dis_l > distance and dis_r > distance:
            break
 
global run_core1
global counter
global dis_l
global dis_r

run_core1=False 
print("start core0")


second_thread = _thread.start_new_thread(core1_thread, (200,))
odo = Odometry()
#counter = 0
#output = 0
dis_l = 0
dis_r = 0
while True:
    #output = counter+1
    #print("core0: ",output)
    print("core0: dis_l =",dis_l)
    print("core0: dis_r =",dis_r)
    odo.update(dis_l, dis_r)
    print("Odo: ", odo.x, " ", odo.y, " ", odo.theta)
    run_core1=True
    sleep(0.05)
    if dis_l > 200:
        break
    

