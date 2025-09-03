# Import the necessary modules
import socket
import threading
import time
import subprocess
from subprocess import Popen, PIPE
import record_tello
import cv2
from djitellopy import tello
from get_online_drones import get_online_drones

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


tello_port = 8889

NUM_TELLOS = len(tello_addresses)

# IP and port of local computer
local_ports = []
for x in range(NUM_TELLOS):
	local_ports.append(9010+x)

local_address = '192.168.0.138'


socks = []
for x in range(NUM_TELLOS):
    # Create a UDP connection that we'll send the command to
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind to the local address and port
    sock.bind((local_address, local_ports[x]))

    # Save the UDP connection to socks array
    socks.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))

    

# Send the message to Tello and allow for a delay in seconds
def send(message, delay):
    # Try to send the message otherwise print the exception
    try:
        for x in range(NUM_TELLOS):
            socks[x].sendto(message.encode(), (tello_addresses[x], tello_port))
            print("Sending message: " + message)
    except Exception as e:
        print("Error sending: " + str(e))

    # Delay for a user-defined period of time
    time.sleep(delay)

# Receive the message from Tello
def receive():
    # Continuously loop and listen for incoming messages
    OK = True
    while OK:
        # Try to receive the message otherwise print the exception
        for x in range(NUM_TELLOS):
            try:
                response, ip_address = socks[x].recvfrom(128)
                print(f"Received message: from Tello EDU #{x}: {response.decode(encoding='utf-8')}")
            except Exception as e:
                # If there's an error close the socket and break out of the loop
                print("Error receiving: " + str(e))
                socks[x].close()
                OK = False
                break

def main():
    # Create and start a listening thread that runs in the background
    # This utilizes our receive functions and will continuously monitor for incoming messages
    receiveThread = threading.Thread(target=receive)
    receiveThread.daemon = True
    receiveThread.start()

    ips = get_online_drones()
    if len(ips) == 0:
        print('No drones online')
        return

    drone = tello.Tello(host=ips[0])
    drone.connect()
    # Put Tello into command mode
    send("command", 3)
    
    send("streamon", 3)

    frame_read = drone.get_frame_read()
    sleep(0.5)
    H, W, _ = frame_read.frame.shape

    send("takeoff", 3)

    while True:

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        # Capture a frame from the Tello video stream
        frame = frame_read.frame

        face = record_tello.detect_face(frame)
        if len(face) > 0:
            (x, y, w, h) = face[0]
            print(x, y, w, h)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)
            if x+w/2 > W/2+10:
                send("cw 20", 3)
            elif x+w/2 < W/2-10:
                send("ccw 20", 3)

            if y+h/2 > H/2+10:
                send("down 20", 3)
            elif y+h/2 < W/2-10:
                send("up 20", 3)


        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

        # Display the captured frame in a window
        print("framejak")
        cv2.imshow("Frame", frame)

        # Check for the 'q' key press to exit the loop and stop recording
        if cv2.waitKey(33) & 0xFF == ord('q'):  # Change 33 to 1 for 30fps
            break
    # # Send the takeoff command
    # send("takeoff", 3)

    # send("flip b", 3)

    # # Land
    # send("land", 3)

    send("streamoff", 3)

    # Print message
    print("Mission completed successfully!")

    # Close the sockets
    for sock in socks:
        sock.close()


if __name__ == "__main__":
    main()