# A basic script to scan a local network for IP addresses to indentify Tello EDU drones

# Import modules
import subprocess
import ipaddress
from subprocess import Popen, PIPE
import asyncio

# Create the network
# The IP below is associated with the TP-Link wireless router
# https://amzn.to/2TR1r56
ip_net = ipaddress.ip_network(u'192.168.0.1/24', strict=False)

i = 0

start = 0
for ip in ip_net.hosts():
    i += 1
    if i < start:
        continue
    # Convert the ip to a string so it can be used in the ping method
    ip = str(ip)
    
    # Let's ping the IP to see if it's online
    toping = Popen(['ping', '-c', '1', '-W', '50', ip], stdout=PIPE)
    output = toping.communicate()[0]
    hostalive = toping.returncode
    
    # Print whether or not device is online
    if hostalive ==0:
        # return True
        print(ip, "is online")
    else:
        # return False
        # print(ip, "is offline")
        pass

    # tasks.append(checkIp(ip))

# async def main():
#     # for task in tasks:
#     #     await asyncio.run(task)
#     await asyncio.gather(*tasks)

# asyncio.run(main())
# # print(res)