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

2.  **Run the application** (locally using Flask's development server):
    ```bash
    python app.py
    ```
    For production, Gunicorn is recommended (see Deployment section).

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
-   **`PORT`**:
    - Environment variable to set the port for the application. Defaults to `8000` if not set. Gunicorn will also respect this when run via `gunicorn app:app --bind 0.0.0.0:$PORT`.

## Error Handling

-   If the camera stream cannot be opened or frames cannot be read, the application will log errors and attempt to serve a placeholder image ("Stream Unavailable") on the `/video` endpoint.
-   Logging is configured to output messages at the INFO level, including timestamps, severity, and the message itself. This helps in diagnosing connection issues or other problems.

## Deploying to Render

Render is a cloud platform for building and running applications. This project includes a `render.yaml` file, which will automatically configure the service on Render, making deployment straightforward.

**Steps for Deployment**:

1.  **Sign up or log in** to your [Render account](https://render.com/).
2.  On the Render Dashboard, click **New +** and select **Web Service**.
3.  **Connect your GitHub repository** where this project is hosted (or GitLab/Bitbucket).
4.  Render will detect the `render.yaml` file. **Review the settings** that are pre-filled from this file.
5.  Ensure the **Build Command** is `pip install -r requirements.txt` and the **Start Command** is `gunicorn app:app`. These should be automatically populated from your `render.yaml`.
6.  **Crucial Step: Configure Environment Variables.**
    -   Under the 'Environment' section for your new Web Service:
        -   Find the `CAMERA_URL` variable. Click 'Edit' (or add it if it wasn't automatically picked up from `render.yaml`'s `envVars` for some reason, though it should be). Change its value to the **actual RTSP or HTTP URL of your IP camera**. The default value in `render.yaml` is a placeholder and likely won't work for you.
        -   Optionally, you can set the `PORT` variable if you need the service to run on a specific port internally (Render handles external port mapping). Gunicorn will use this. However, Render typically injects its own `PORT` environment variable that Gunicorn should pick up automatically.
7.  **Choose your instance type**. The free tier might be sufficient for testing, but consider a paid tier for more demanding use or production.
8.  Click **Create Web Service**.
9.  Render will start building and deploying your application. You can monitor the progress in the **Deploy Logs**.

**Post-Deployment**:

-   Once deployed, Render will provide you with a unique `.onrender.com` URL for your service (e.g., `https://your-service-name.onrender.com`).
-   Access the `/video` path on this URL to see your video stream (e.g., `https://your-service-name.onrender.com/video`).

**Checking Logs**:

-   You can view your application's live and historical logs in the **Logs** tab for your service in the Render dashboard. This is essential for troubleshooting any issues with your camera connection or application behavior.
