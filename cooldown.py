from djitellopy import tello
from time import sleep

# Use this when the drone is overheating to cool it down.

drone = tello.Tello(host='192.168.0.167')
drone.connect()
sleep(1)
drone.turn_motor_on()
sleep(30)
print(drone.get_battery())
drone.turn_motor_off()
