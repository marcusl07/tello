from subprocess import Popen, PIPE

# IP and port of Tellos
tello_addresses_og = [   
	"192.168.0.138",
    "192.168.0.167",
    "192.168.0.177"]

def get_online_drones():
	tello_addresses = tello_addresses_og[:]

	for ip in tello_addresses_og:
		toping = Popen(['ping', '-c', '1', '-W', '50', ip], stdout=PIPE)
		output = toping.communicate()[0]
		hostalive = toping.returncode
		if hostalive != 0:
			tello_addresses.remove(ip)
			print(ip + ' not online')

	return tello_addresses