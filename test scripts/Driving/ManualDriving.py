from picarx import Picarx
from time import sleep
import readchar

manual = '''
Press keys on keyboard to control PiCar-X!
    w: Forward
    a: Turn left
    s: Backward
    d: Turn right
    i: Accelerate
    k: Decelerate
    speed: {speed}
    ctrl+c: Press twice to exit the program
'''

def leftTurnS():
    px.set_dir_servo_angle(-10)

def leftTurnM():
    px.set_dir_servo_angle(-30)

def rightTurnS():
    px.set_dir_servo_angle(10)

def rightTurnM():
    px.set_dir_servo_angle(30)


def straight():
    px.set_dir_servo_angle(0)

def forward():
     px.forward(speed)

def accelerate():
     speed = speed + 10

def decelerate():
     speed = speed + 10

def stop():
    px.forward(0)

def show_info():
    print("\033[H\033[J",end='')  # clear terminal windows
    print(manual)


if __name__ == "__main__":
    try:
        speed = 80
        px = Picarx()
        
        show_info()
        while True:
            key = readchar.readkey()
            key = key.lower()
            if key in('wsadikjl'): 
                if 'w' == key:
                    forward()
                if 's' == key:   
                    stop()
                if 'j' == key:
                    accelerate()
                if 'k' == key:
                    decelerate()
                if 'd' == key:
                    rightTurnS()
                elif 'a' == key:
                    leftTurnM()
                else:
                    straight()
     
                show_info()                     
                sleep(0.5)
                px.forward(0)
          
            elif key == readchar.key.CTRL_C:
                print("\n Quit")
                break

    finally:
        px.set_cam_tilt_angle(0)
        px.set_cam_pan_angle(0)  
        px.set_dir_servo_angle(0)  
        px.stop()
        sleep(.2)