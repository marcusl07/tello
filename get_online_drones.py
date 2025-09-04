from subprocess import Popen, PIPE
from djitellopy import tello

"""
# IP and port of Tellos
tello_ip = "192.168.0.167"

def get_online_drones():
	ip_out = tello_ip[:]

	toping = Popen(['ping', '-c', '1', '-W', '50', tello_ip], stdout=PIPE)
	hostalive = toping.returncode
	if hostalive != 0:
		print(tello_ip + ' not online')

	return ip_out
"""

ips = ["192.168.0.125", "192.168.0.138", "192.168.0.167"]

for ip in ips:
    drone = tello.Tello(host=ip)
    try:
        drone.connect()
        print(f"{ip} is a drone")
    except tello.TelloException as t:
        print(f"{ip} not a drone")
