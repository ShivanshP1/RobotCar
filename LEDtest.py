# Import Pin class
import time
from robot_hat import Pin

# Create Pin object with numeric pin numbering and default input pullup enabled
#d4 = Pin(2, Pin.OUT)
d2 = Pin("D2")
#d1 = Pin(1, Pin.OUT)
# Create Pin object with named pin numbering
#d1.low()
for i in range(10):
  d2.high()
  time.sleep(1)
  d2.low()
  time.sleep(1)
