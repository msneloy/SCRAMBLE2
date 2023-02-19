# Import the necessary modules
import psutil
import time
from datetime import datetime
import cv2
import threading

# Define the sketch function
def sketch(image):
    # Same as before...

# Define a thread function for reading and processing the video feed
def process_video_feed():
    # Open the camera
    cap = cv2.VideoCapture(0)

    # Set the frame size to the maximum values
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Initialize variables for FPS calculation
    prev_frame_time = 0
    new_frame_time = 0

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Apply the sketch effect to the frame
        feed = sketch(frame)

        # Calculate the FPS of the video feed
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time

        # Get the CPU and memory usage
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent

        # Generate strings for the FPS, timestamp, CPU usage, memory usage, and resolution
        FPS = "FPS : " + str(int(fps))
        DT = "Timestamp : " + str(datetime.now())
        CPU = "CPU usage : " + str(cpu_usage) + "%"
        MEM = "Memory usage : " + str(memory_usage) + "%"
        RES = "Resolution : " + str(width) + "x" + str(height)

        # Log the FPS, timestamp, CPU usage, memory usage, and resolution to the console
        print("Console Log | ", DT, " | ", CPU, " | ", MEM, " | ", FPS, " | ", RES)

        # Store the processed frame in a global variable
        global processed_frame
        processed_frame = feed

        # Check if the user pressed the "q" key
        if cv2.waitKey(1) == ord("q"):
            # If the "q" key was pressed, break out of the loop
            break

    # Release the camera
    cap.release()

# Define a thread function for displaying the frames
def display_frames():
    while True:
        # Display the processed frame
        cv2.imshow('CAM FEED', processed_frame)

        # Check if the user pressed the "q" key
        if cv2.waitKey(1) == ord("q"):
            # If the "q" key was pressed, break out of the loop
            break

    # Close the window
    cv2.destroyAllWindows()

# Create a global variable for the processed frame
processed_frame = None

# Create and start the threads
process_thread = threading.Thread(target=process_video_feed)
display_thread = threading.Thread(target=display_frames)
process_thread.start()
display_thread.start()

# Wait for both threads to finish
process_thread.join()
display_thread.join()
