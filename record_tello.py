# OpenCV (cv2) for video processing, datetime for timestamping, tello for our drone object.
import cv2
from djitellopy import tello
from datetime import datetime
from time import sleep
from pid import PID

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
<<<<<<< HEAD
        
=======

def track_face(frame_read: tello.BackgroundFrameRead, drone: tello.Tello, H: int, W: int):
    while True:
        # Capture a frame from the Tello video stream
        frame = frame_read.frame

        face = detect_face(frame)
        if len(face) > 0:
            (x, y, w, h) = face[0]
            print(x, y, w, h)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)
            if x+w/2 > W/2+10:
                drone.rotate_clockwise(20)
            elif x+w/2 < W/2-10:
                drone.rotate_counter_clockwise(20)

            if y+h/2 > H/2+10:
                drone.move('down', 25)
            elif y+h/2 < W/2-10:
                drone.move('up', 25)


        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

        # Display the captured frame in a window
        cv2.imshow("Frame", frame)

        # Check for the 'q' key press to exit the loop and stop recording
        if cv2.waitKey(33) & 0xFF == ord('q'):  # Change 33 to 1 for 30fps
            break
>>>>>>> 9b24329e77a760cb7cf8c81caa4ecf1a64c56c67

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Initialize Tello drone and establish connection
    drone = tello.Tello(host='192.168.0.167')
    drone.connect()
    drone.streamon()

    # Obtain frame reader from Tello and get frame dimensions
    frame_read = drone.get_frame_read()
    sleep(0.5)
    H, W, _ = frame_read.frame.shape

    drone.takeoff()

    # Run video recording function
<<<<<<< HEAD
    # record_tello_video_stream(frame_read, out)
    while True:
        # Capture a frame from the Tello video stream
        frame = frame_read.frame

        face = detect_face(frame)
        if len(face) > 0:
            (x, y, w, h) = face[0]
            print(x, y, w, h)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)
            if x+w/2 > W/2+10:
                drone.rotate_clockwise(20)
            elif x+w/2 < W/2-10:
                drone.rotate_counter_clockwise(20)

            if y+h/2 > H/2+10:
                drone.move('down', 25)
            elif y+h/2 < W/2-10:
                drone.move('up', 25)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

        # Display the captured frame in a window
        cv2.imshow("Frame", frame)

        # Check for the 'q' key press to exit the loop and stop recording
        if cv2.waitKey(33) & 0xFF == ord('q'):  # Change 33 to 1 for 30fps
            break
=======
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    out = cv2.VideoWriter(f'{timestamp}_output.mp4', fourcc, fps=30, frameSize=(W, H))
    record_tello_video_stream(frame_read, out)
    track_face(frame_read, drone, H, W)
>>>>>>> 9b24329e77a760cb7cf8c81caa4ecf1a64c56c67

    drone.land() 
    
    cv2.destroyAllWindows()
    out.release()
    # Display end-of-main message and reboot the drone
    print('end of main, calling drone.reboot')
    drone.reboot()


if __name__ == "__main__":
    main()
