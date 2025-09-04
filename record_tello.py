# OpenCV (cv2) for video processing, datetime for timestamping, tello for our drone object.
import cv2
from djitellopy import tello
from datetime import datetime
from time import sleep
from pid import PID
from get_online_drones import get_online_drones

def detect_face(frame):
    f = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    gray_img = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face = face_classifier.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

    return face


def record_tello_video_stream(frame_read: tello.BackgroundFrameRead, out: cv2.VideoWriter):
    try:
        i = 0
        while True:
            # i += 1
            # if i > 100:
            #     break
            # Capture a frame from the Tello video stream
            frame = frame_read.frame

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

            # Write the captured frame to the output video file
            out.write(frame)

            # Display the captured frame in a window
            cv2.imshow("Frame", frame)

            # Check for the 'q' key press to exit the loop and stop recording
            if cv2.waitKey(33) & 0xFF == ord('q'):  # Change 33 to 1 for 30fps
                break
    except Exception as e:
        print(f'An exception occurred in recording tellos video stream {e}')
    finally:
        # Close the window and release the video writer
        cv2.destroyAllWindows()
        out.release()

def track_face(frame_read: tello.BackgroundFrameRead, drone: tello.Tello, H: int, W: int):
    #Init PID objects
    x_pid = PID(0.1, 0, 0.2, -180, 180, 10)
    y_pid = PID(0.2, 0, 0.1, -200, 200, 10)

    while True:
        # Capture a frame from the Tello video stream
        frame = frame_read.frame

        face = detect_face(frame)
        if len(face) > 0:
            (x, y, w, h) = face[0]
            print(x, y, w, h)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)

            x_move = int( x_pid.getAmount(x+w/2 - W/2) )

            if x_move >= 1:
                drone.rotate_clockwise(x_move)
            elif x_move <= -1:
                drone.rotate_counter_clockwise(-x_move)

            print('y--')
            y_move = int(y_pid.getAmount(y+h/2 - H/2))

            if y_move >= 20:
                drone.move('down', y_move)
            elif y_move <= -20:
                drone.move('up', -y_move)


        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

        # Display the captured frame in a window
        # cv2.imshow("Frame", frame)

        # Check for the 'q' key press to exit the loop and stop recording
        if cv2.waitKey(33) & 0xFF == ord('q'):  # Change 33 to 1 for 30fps
            break