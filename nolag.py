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
from pid import PID
from face import Face




tello_addresses = get_online_drones()

tello_port = 8889

NUM_TELLOS = len(tello_addresses)

# IP and port of local computer
local_ports = []
for x in range(NUM_TELLOS):
	local_ports.append(9010+x)

# local_address = '192.168.0.138' 
local_address = '192.168.0.125'


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
    if NUM_TELLOS == 0:
        print("No Tello drones found.")
        return
    
    #Init PID objects
    x_pid = PID(p=0.05, i=0, d=0.05, _min=-180, _max=180, margin=10)
    y_pid = PID(p=0.05, i=0, d=0.05, _min=-200, _max=200, margin=10)

    #init Face
    face_obj = Face()

    # Create and start a listening thread that runs in the background
    # This utilizes our receive functions and will continuously monitor for incoming messages
    receiveThread = threading.Thread(target=receive)
    receiveThread.daemon = True
    receiveThread.start()

    drone = tello.Tello(host=tello_addresses[0])
    drone.connect()
    # Put Tello into command mode
    send("command", 3)
    
    send("streamon", 3)

    frame_read = drone.get_frame_read()
    time.sleep(0.5)
    H, W, _ = frame_read.frame.shape

    # send("takeoff", 3)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        # Capture a frame from the Tello video stream
        frame = frame_read.frame

        # face_obj.update(frame)

        # face = []

        # if face_obj.inited:
        #     if len(face_obj.face_avg) > 0:
        #         face = face_obj.face_avg
        #     elif len(face_obj.face_predict) > 0:
        #         face = face_obj.face_predict
        #     if len(face_obj.faces[face_obj.i]) == 0 and len(face) > 0:
        #         print('no face fixed')

        # print(face_obj.get_face())
        # print(face)
        # print()

        face = record_tello.detect_face(frame)

        if len(face) > 0:
            (x, y, w, h) = face[0]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)

            x_move = int(x_pid.getAmount(x+w/2 - W/2) )
            y_move = int(y_pid.getAmount(y+h/2 - H/2))

            # if x_move >= 1:
            #     send(f"cw {x_move}", 0)
            # elif x_move <= -1:
            #     send(f"ccw {-x_move}", 0)

            # if y_move >= 20:
            #     send(f'down {y_move}', 0)
            # elif y_move <= -20:
            #     send(f'up {-y_move}', 0)

        time.sleep(0.05)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

        # Display the captured frame in a window
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