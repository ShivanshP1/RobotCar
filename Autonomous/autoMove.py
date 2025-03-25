from picarx import Picarx
from time import sleep
import readchar
import drivingPath



# Press keys on keyboard to control PiCar-X!
#     w: Forward
#     a: Turn left
#     s: Stop
#     x: Backward
#     d: Turn right
#     i: Accelerate
#     k: Decelerate
#     Current speed: {speed}
#     Current angle: {angle}
#     ctrl+c: Press twice to exit the program



# def show_info(speed, angle):
#     print("\033[H\033[J", end='')  # clear terminal windows
#     print(get_manual(speed, angle))


if __name__ == "__main__":
    try:
        speed = 80
        angle = 0
        px = Picarx()

        #show_info(speed, angle)
        src = [29, 129]  # Starting position (row, column)
        dest = [284, 393]  # Destination position
        initialDirecIndex = 2
        drivingPath.driving(src, dest, initialDirecIndex)
        path = drivingPath.moveList
        print(path)
        key = path.pop(0)
        while True:
            print(key)

            if 'f' == key:
                px.forward(speed)
            elif 'p' == key:
                px.forward(0)
            elif 'x' == key:
                px.forward(-speed)
            elif 'i' == key:
                speed = min(100, speed + 10)  # limit max speed
            elif 'k' == key:
                speed = max(0, speed - 10)  # prevent negative speed
            elif 'l' == key:
                angle = min(25, angle + 10)  # limit right turn
            elif 'r' == key:
                angle = max(-25, angle - 10)  # limit left turn

            key = path.pop(0)
            px.set_dir_servo_angle(angle)
            # show_info(speed, angle)
            sleep(0.5)


    finally:
        px.set_cam_tilt_angle(0)
        px.set_cam_pan_angle(0)
        px.set_dir_servo_angle(0)
        px.stop()
        sleep(.2)
