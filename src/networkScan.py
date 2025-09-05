# A basic script to scan a local network for IP addresses to indentify Tello drones. 
# Uses brute force so it can take a few minutes.

import ipaddress
from subprocess import Popen, PIPE
from djitellopy import tello

def scan_network():
    ip_net = ipaddress.ip_network(u'192.168.0.1/24', strict=False)
    i = 0
    start = 0
    drones = []

    

    for ip in ip_net.hosts():
        i += 1
        if i < start:
            continue

        # Convert the ip to a string so it can be used in the ping method
        ip = str(ip)
        
        # Let's ping the IP to see if it's online
        toping = Popen(['ping', '-c', '1', '-W', '50', ip], stdout=PIPE)
        hostalive = toping.returncode
        
        # Print whether or not device is online
        if hostalive == 0:
            drone = tello.Tello(host=ip)
            
            try:
                drone.connect()
                drones.append(ip)
                drone.end()
            except tello.TelloException:
                pass

    return drones