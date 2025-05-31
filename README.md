# IP Camera Video Streamer

A simple Flask application that serves a video stream from an IP camera. It uses OpenCV to capture the video feed and streams it over HTTP using a multipart response.

## Prerequisites

- Python 3.x

## Installation

1.  **Clone the repository** (or download the files):
    ```bash
    git clone <repository_url> # Replace <repository_url> with the actual URL
    cd <repository_directory>
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    -   Linux/macOS:
        ```bash
        source venv/bin/activate
        ```
    -   Windows:
        ```bash
        venv\Scripts\activate
        ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Server

1.  **Set the `CAMERA_URL` environment variable** (optional):
    This variable specifies the RTSP or HTTP URL of your IP camera. If not set, the application will use a default placeholder URL (which may not correspond to a live camera, resulting in a "Stream Unavailable" placeholder image being shown).

    -   Linux/macOS:
        ```bash
        export CAMERA_URL="rtsp://username:password@your_camera_ip:port/stream_path"
        ```
    -   Windows (Command Prompt):
        ```bash
        set CAMERA_URL="rtsp://username:password@your_camera_ip:port/stream_path"
        ```
    -   Windows (PowerShell):
        ```powershell
        $env:CAMERA_URL="rtsp://username:password@your_camera_ip:port/stream_path"
        ```
    Replace `"rtsp://username:password@your_camera_ip:port/stream_path"` with the actual URL of your camera.

2.  **Run the application**:
    ```bash
    python app.py
    ```

3.  The server will start, and you should see logging output similar to:
    ```
    YYYY-MM-DD HH:MM:SS - INFO - Flask application starting on host 0.0.0.0 port 8000
    ```
    You can access the server at `http://0.0.0.0:8000` or `http://localhost:8000`.

## Endpoints

-   **`/`**:
    -   Displays a simple message: "Skyguard Online".
-   **`/video`**:
    -   Provides the MJPEG video stream from the camera. You can view this in a web browser that supports MJPEG streams (most modern browsers do) or use it as a source in video players like VLC.

## Configuration

-   **`CAMERA_URL`**:
    -   Environment variable to set the RTSP or HTTP(S) URL of the IP camera.
    -   **Example**: `rtsp://admin:123456@192.168.1.100:554/stream1`
    -   If this variable is not set, the application defaults to `rtsp://admin:123456@192.168.0.109:554/stream1`. If this default camera is not accessible, the video stream will show a placeholder image indicating "Stream Unavailable".

## Error Handling

-   If the camera stream cannot be opened or frames cannot be read, the application will log errors and attempt to serve a placeholder image ("Stream Unavailable") on the `/video` endpoint.
-   Logging is configured to output messages at the INFO level, including timestamps, severity, and the message itself. This helps in diagnosing connection issues or other problems.
