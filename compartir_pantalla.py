from flask import Flask, render_template, Response
import cv2
import numpy as np
import mss

app = Flask(__name__)

def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        print("Capturando pantalla del monitor:", monitor)
        while True:
            try:
                screen = sct.grab(monitor)
                frame = np.array(screen)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                _, buffer = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            except Exception as e:
                print("Error en capture_screen:", e)
                break


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Responde sin contenido


@app.route('/video_feed')
def video_feed():
    return Response(capture_screen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
