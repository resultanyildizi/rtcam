import cv2
import os
from datetime import datetime, timedelta

# Set the path for storage
path = os.getenv('webcam_storage', '.')
os.makedirs(path, exist_ok=True)

# Open the camera (assuming device index 2)
cam2 = cv2.VideoCapture(2)

# Get the default frame width and height
frame_width = int(cam2.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam2.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# Initialize variables
start_time = datetime.now()
out = None

while True:
    current_time = datetime.now()
    
    # Create a new video file every minute
    if out is None or (current_time - start_time).total_seconds() >= 10:
        if out:
            # Release the current writer object
            out.release()
        
        # Update start_time for the next minute
        start_time = current_time

        # Create a new output filename with the current timestamp
        timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
        output_filename = os.path.join(path, f'output_{timestamp}.mp4')
        
        # Create a new VideoWriter object
        out = cv2.VideoWriter(output_filename, fourcc, 20.0, (frame_width, frame_height))
        print(f"Started new video: {output_filename}")

    # Capture frame-by-frame
    ret, frame = cam2.read()
    if not ret:
        print("Failed to grab frame. Exiting...")
        break

    # Write the frame to the current output file
    out.write(frame)

    # Display the captured frame
    # cv2.imshow('Camera', frame)

    # Press 'q' to exit the loop
    # if cv2.waitKey(1) == ord('q'):
        # break

# Release the capture and writer objects
cam2.release()
if out:
    out.release()
# cv2.destroyAllWindows()
print("Recording stopped.")

