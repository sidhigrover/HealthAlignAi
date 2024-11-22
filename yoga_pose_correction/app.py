from flask import Flask, render_template, Response
import pose_detection

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')  # Serve the index.html page

# Route for the video feed
@app.route('/video_feed')
def video_feed():
    return Response(pose_detection.gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')  # Stream video frames


if __name__ == '__main__':
    app.run(debug=True)
