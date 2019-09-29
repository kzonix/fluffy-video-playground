import cv2
import numpy as np
from flask import Response
from flask import Flask
from flask import render_template
import imutils
from imutils.video import VideoStream
import threading
import time

app = Flask(__name__)

globalFrame = None
lock = threading.Lock()
vs = VideoStream(src=0).start()
time.sleep(2.0)


@app.route("/stream")
def video_stream():
    global globalFrame, lock

    def streaming_fn():
        global globalFrame, lock

        while True:
            with lock:
                # Capture frame-by-frame
                if globalFrame is None:
                    continue
                frame = imutils.resize(globalFrame, width=400)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (7, 7), 0)
                (flag, encoded_image) = cv2.imencode(".jpg", gray)
                if not flag:
                    continue
            yield (b'--frame\r\n' +
                   b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(encoded_image) +
                   b'\r\n')

    return Response(streaming_fn(), mimetype='multipart/x-mixed-replace; boundary=frame')


def read_image():
    global vs, globalFrame, lock
    while True:
        frame = vs.read()
        with lock:
            globalFrame = frame.copy()


if __name__ == "__main__":
    t = threading.Thread(target=read_image)
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', port=9890, debug=True,
            threaded=True, use_reloader=False)

vs.stop()
