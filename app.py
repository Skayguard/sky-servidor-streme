from flask import Flask, Response
import cv2

app = Flask(__name__)

# Substitua isso pelo endereço RTSP ou HTTP da sua câmera IP
camera_url = "rtsp://admin:123456@192.168.0.109:554/stream1"

def generate_frames():
    cap = cv2.VideoCapture(camera_url)

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Codifica o frame em JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Retorna como multipart HTTP
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return "Skyguard Online"

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
