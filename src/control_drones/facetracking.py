# Import the necessary modules
import socket
import threading
import time
import cv2
from djitellopy import tello
from ..pid import PID
from ..networkScan import scan_network

# Uncomment to find Tello drones on the network.
# tello_address = scan_network()

# If you know the IP address of your Tello, you can hardcode it here
tello_address = "192.168.0.167"
#Check your own IP address by clicking into your network settings, then paste it here
local_address = '192.168.0.125'

tello_port = 8889

local_port = 9010

# Create a UDP connection that we'll send the command to
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the local address and port
sock.bind((local_address, local_port))

#Init PID objects
#increase p to make the drone more sensitive, increase d if the drone is overshooting/oscillating, increase i if the drone is not centering the face even after a long time.
#however i is a bit buggy, especially if it loses track of the face, so be careful as the drone can go crazy.
x_pid = PID(p=0.05, i=0, d=0.05, _min=-90, _max=90, margin=10)
y_pid = PID(p=0.15, i=0, d=0.1, _min=-100, _max=100, margin=6)
z_pid = PID(p=0.75, i=0, d=0.1, _min=-100, _max=100, margin=10)

# Send the message to Tello and allow for a delay in seconds
def send(message, delay):
    # Try to send the message otherwise print the exception
    try:
        sock.sendto(message.encode(), (tello_address, tello_port))
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
            try:
                response = sock.recvfrom(128)
                print(f"Received message: from Tello EDU #{0}: {response.decode(encoding='utf-8')}")
            except Exception as e:
                # If there's an error close the socket and break out of the loop
                print("Error receiving: " + str(e))
                sock.close()
                OK = False
                break

def detect_face(frame):
    f = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    gray_img = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face = face_classifier.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

    return face

def main(): 
    # Create and start a listening thread that runs in the background
    # This utilizes our receive functions and will continuously monitor for incoming messages
    receiveThread = threading.Thread(target=receive)
    receiveThread.daemon = True
    receiveThread.start()

    #Create a tello object used to get video stream
    drone = tello.Tello(host=tello_address)
    drone.connect()
    # Put Tello into command mode
    send("command", 3)
    
    #Turn on camera
    send("streamon", 3)

    #Get object to get video frames
    frame_read = drone.get_frame_read()
    time.sleep(0.5)
    H, W, _ = frame_read.frame.shape

    send("takeoff", 3)

    # Keep detecting faces and following them using PID control
    while True:
        # Capture a frame from the Tello video stream
        frame = frame_read.frame

        face = detect_face(frame)

        if len(face) > 0:
            (x, y, w, h) = face[0] #xy is top left corner
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)

            #how much the drone should move in the x, y, and z directions
            x_move = int(x_pid.getAmount(x+w/2 - W/2))
            y_move = int(y_pid.getAmount(y+h/2 - H/2))
            z_move = int(z_pid.getAmount(w-100))

            #minimum move is 20cm. the tello drone will ignore any command less than that.
            if y_move >= 20:
                send(f'down {y_move}', 0.1)
            elif y_move <= -20:
                send(f'up {-y_move}', 0.1)

            #minimum rotation is 1 degree.
            if x_move >= 1:
                send(f"cw {x_move}", 0.1)
            elif x_move <= -1:
                send(f"ccw {-x_move}", 0.1)

            if z_move >= 20:
                send(f'back {z_move}', 0.1)
            elif z_move <= -20:
                send(f'forward {-z_move}', 0.1)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

        # Display the captured frame in a window. 
        # To land the drone and stop the video press 'q' while focused on the window.
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Shutdown
    send("land", 1)
    send("streamoff", 1)
    sock.close() 

if __name__ == "__main__":
    main()