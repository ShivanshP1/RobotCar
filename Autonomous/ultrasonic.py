from picarx import Picarx
import time

px = Picarx()

while True:
    distance = px.ultrasonic.read()
    print(f"Distance: {distance} cm")
    time.sleep(1)
