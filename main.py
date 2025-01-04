import cv2
import os
import argparse
from datetime import datetime, timedelta

def main():
    # get arguments
    # device: int - device index to use for recording
    # headless: True/False - if True, no video will be displayed
    # duration: int - duration of recording in seconds
    # storage: string - path to save the video, if not provided, will save in current directory
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=int, default=0)
    parser.add_argument('--headless', type=bool, default=False)
    parser.add_argument('--duration', type=int, default=60)
    parser.add_argument('--storage', type=str, default='.')

    args = parser.parse_args()

    device= args.device
    headless = args.headless
    duration = args.duration
    storage = args.storage

    # Set the path for storage
    os.makedirs(storage, exist_ok=True)

    # Open the camera (assuming device index 2)
    cam2 = cv2.VideoCapture(device)

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
        if out is None or (current_time - start_time).total_seconds() >= duration:
            if out:
                # Release the current writer object
                out.release()
            
            # Update start_time for the next minute
            start_time = current_time

            # Create a new output filename with the current timestamp
            timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
            output_filename = os.path.join(storage, f'output_{timestamp}.mp4')
            
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
        if not headless:
            cv2.imshow('Camera', frame)

        # Press 'q' to exit the loop
        if not headless and cv2.waitKey(1) == ord('q'):
            break

    # Release the capture and writer objects
    cam2.release()
    if out:
        out.release()
    if not headless:
        cv2.destroyAllWindows()
    print("Recording stopped.")

if __name__ == "__main__":
    main()
