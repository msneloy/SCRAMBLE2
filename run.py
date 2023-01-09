# Import the psutil and time modules for CPU and memory usage and FPS calculation
import psutil
import time

# Import the datetime module for timestamp generation
from datetime import datetime

# Import the cv2 module for image processing
import cv2

# Define the sketch function that takes an image and applies a "sketch" effect to it
def sketch(image):
    # Convert the image to grayscale
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a Gaussian blur to the grayscale image to reduce high-frequency noise
    img_gray_blur = cv2.GaussianBlur(img_gray, (5,5), 0)

    # Detect edges in the image using the Canny edge detector
    canny_edges = cv2.Canny(img_gray_blur, 10, 70)

    # Apply a binary inverse threshold to the edge image
    ret, mask = cv2.threshold(canny_edges, 70, 255, cv2.THRESH_BINARY_INV)

    # Return the thresholded image
    return mask

# Open the default camera using cv2.VideoCapture
cap = cv2.VideoCapture(0)

# Initialize variables for FPS calculation
prev_frame_time = 0
new_frame_time = 0

# Set the width and height of the frames to their maximum values
cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap.get(cv2.CAP_PROP_FRAME_WIDTH))
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Get the width and height of the frames
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Check if the camera was successfully opened
if not cap.isOpened():
    # If the camera could not be opened, print an error message and exit
    print("Failed to launch camera")
    exit()

# Enter a loop to process and display the video feed
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

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

    # Apply the sketch effect to the frame
    feed = sketch(frame)

    # Display the frame with the sketch effect applied
    cv2.imshow('CAM FEED', feed)

    # Check if the user pressed the "q" key
    if cv2.waitKey(1) == ord("q"):
        # If the "q" key was pressed, break out of the loop
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()

