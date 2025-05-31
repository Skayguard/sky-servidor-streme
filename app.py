from flask import Flask, Response
import cv2
import os
import logging
import numpy as np

# Configure logging: Sets level to INFO and includes timestamp, level, and message in logs.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Default camera URL (can be overridden by CAMERA_URL environment variable)
# The original comment "Substitua isso pelo endereço RTSP ou HTTP da sua câmera IP"
# means "Replace this with the RTSP or HTTP address of your IP camera".
camera_url = os.environ.get('CAMERA_URL', 'rtsp://admin:123456@192.168.0.109:554/stream1')

def create_placeholder_frame():
    """
    Generates a black JPEG image with 'Stream Unavailable' text.
    This is used as a fallback when the actual camera stream is not available.
    """
    width, height = 640, 480
    # Create a black image (3 channels for BGR color)
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    text = "Stream Unavailable"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    # Get text size to center it
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = (width - text_size[0]) // 2
    text_y = (height + text_size[1]) // 2
    # Put text on the image
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness) # White text

    # Encode the frame to JPEG format
    ret, buffer = cv2.imencode('.jpg', frame)
    if not ret:
        logging.error("Failed to encode placeholder frame to JPEG.")
        # Fallback: create a simple black JPEG if encoding text fails
        # This is highly unlikely with a np.zeros generated image.
        frame_gray = np.zeros((height, width, 1), dtype=np.uint8) # Grayscale for simplicity
        ret_gray, buffer = cv2.imencode('.jpg', frame_gray)
        if not ret_gray:
            logging.critical("Failed to encode even a simple grayscale placeholder. Returning empty bytes.")
            return b'' # Return empty bytes if all encoding fails
    return buffer.tobytes()

def generate_frames():
    """
    Connects to the camera, reads frames, encodes them to JPEG, and yields them for streaming.
    If connection or frame reading fails, it yields a placeholder image.
    The output is a multipart HTTP response (video/x-mixed-replace).
    """
    logging.info(f"Attempting to connect to camera: {camera_url}")
    cap = None  # Initialize VideoCapture object to None for release in finally block

    try:
        # Attempt to open the video stream from the camera_url
        cap = cv2.VideoCapture(camera_url)
        # Check if the camera was opened successfully
        if not cap.isOpened():
            logging.error(f"Error: Could not open video stream at {camera_url}. Yielding placeholder.")
            placeholder_bytes = create_placeholder_frame()
            # Yield the placeholder frame once as a complete multipart segment
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + placeholder_bytes + b'\r\n')
            return # Terminate the generator

        logging.info(f"Successfully connected to camera: {camera_url}")

        # Loop to continuously read frames from the camera
        while True:
            # Read a frame from the camera
            success, frame = cap.read()
            if not success:
                logging.error("Failed to read frame from camera. Serving placeholder and closing stream.")
                placeholder_bytes = create_placeholder_frame()
                # Yield the placeholder frame once
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + placeholder_bytes + b'\r\n')
                break # Exit the loop; the 'finally' block will release the camera

            # Encode the captured frame into JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                logging.warning("Failed to encode frame to JPEG. Skipping this frame.")
                continue # Skip this frame and try the next one

            frame_bytes = buffer.tobytes()
            # Yield the frame as part of the multipart HTTP response
            # Each frame is preceded by a boundary and content type header
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    except cv2.error as e:
        # Handle OpenCV specific errors that might occur during streaming
        logging.error(f"OpenCV error during video stream: {e}. Yielding placeholder.")
        placeholder_bytes = create_placeholder_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + placeholder_bytes + b'\r\n')
    except Exception as e:
        # Handle any other unexpected errors
        logging.error(f"Unexpected error during video stream: {e}. Yielding placeholder.")
        placeholder_bytes = create_placeholder_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + placeholder_bytes + b'\r\n')
    finally:
        # Ensure the video capture object is released if it was opened
        if cap and cap.isOpened():
            logging.info("Releasing video capture object.")
            cap.release()

@app.route('/')
def index():
    """Serves a simple welcome page."""
    return "Skyguard Online"

@app.route('/video')
def video():
    """Route for the video stream."""
    # Returns a Flask Response object that streams the video frames.
    # 'mimetype' is set to 'multipart/x-mixed-replace' to tell the browser
    # that parts of the content will be replaced by new data (frames).
    # 'boundary=frame' defines the delimiter between frames.
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    host = '0.0.0.0'  # Listen on all available network interfaces
    # Port for the web server, configurable via PORT environment variable
    port = int(os.environ.get('PORT', 8000))
    logging.info(f"Flask application starting on host {host} port {port}")
    # Run the Flask development server
    app.run(host=host, port=port)
