# Tello Talent Drone Face Tracking

This project demonstrates face tracking with the Tello Talent drone using OpenCV (`cv2`) and drone swarm control with [DJITelloPy](https://github.com/damiafuentes/DJITelloPy).

## Features

- **Face Tracking:** Leveraging `cv2` for real-time face detection and tracking.
- **Drone Swarm Control:** Coordinate multiple Tello drones using DJITelloPy for synchronized movement and tasks.

Some code for sending and receiving commands in face tracking and discovering drones on the network is inspired by and adapted from [DroneBlocks-TelloEDU-Python](https://github.com/dbaldwin/DroneBlocks-TelloEDU-Python/tree/master).

## Requirements

- Python 3.x
- [OpenCV (cv2)](https://opencv.org/)
- [DJITelloPy](https://github.com/damiafuentes/DJITelloPy)
- Tello Talent drone(s)

## Usage

1. Install requirements:
    ```bash
    pip install opencv-python djitellopy
    ```
2. Connect your computer to the Tello drone Wi-Fi network.
3. Run the face tracking script to start controlling the drone(s).