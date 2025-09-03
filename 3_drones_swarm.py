from djitellopy import TelloSwarm, Tello
from time import sleep

import subprocess
from subprocess import Popen, PIPE

# IP and port of Tellos
tello_addresses_og = [   
    "192.168.0.152",
    "192.168.0.167",
    "192.168.0.177"]

tello_addresses = tello_addresses_og[:]

for ip in tello_addresses_og:
    toping = Popen(['ping', '-c', '1', '-W', '50', ip], stdout=PIPE)
    output = toping.communicate()[0]
    hostalive = toping.returncode
    if hostalive != 0:
        tello_addresses.remove(ip)
        print(ip + ' not online')


# swarm = TelloSwarm.fromIps(tello_addresses)

# swarm.connect()

# # swarm.sequential(lambda i, tello: tello.turn_motor_on())
# # sleep(60)
# # swarm.sequential(lambda i, tello: tello.turn_motor_off())
# swarm.takeoff()

# swarm.parallel(lambda i, tello: tello.move_up(50))
# swarm.parallel(lambda i, tello: tello.flip('f'))
# swarm.land()
# swarm.end()