from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import whisper
import os

app = Flask(__name__)
CORS(app)

# HTML को सीधा यहीं रख देते हैं Replit के लिए
HTML = '''
<!DOCTYPE html>
<html>
<head><title>Video Caption Generator</title></head>
<body style="font-family: Arial; padding: 20px; max-width: 600px; margin: auto;">
    <h2>Video Upload करके English Captions पाओ</h2>
    <form id="uploadForm">
        <input type="file" id="videoFile" accept="video/*" required><br><br>
        <button type="submit">Generate Captions</button>
    </form>
    <h3>Captions:</h3>
    <div id="captions" style="border:1px solid #ccc; padding:15px; min-height:100px;"></div>
    <p id="status"></p>

    <script>
        document.getElementById('uploadForm').onsubmit = async (e) => {
            e.preventDefault();
            const status = document.getElementById('status');
            const captionsDiv = document.getElementById('captions');
            status.innerText = "Uploading... 1-2 min लगेगा, Whisper चल रहा है";
            captionsDiv.innerText = "";

            let formData = new FormData();
            formData.append('video', document.getElementById('videoFile').files[0]);

            let response = await fetch('/upload', { method: 'POST', body: formData });
            let data = await response.json();
            captionsDiv.innerText = data.captions || data.error;
            status.innerText = "हो गया ✅";
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/upload', methods=['POST'])
def upload_video():
    video = request.files['video']
    video_path = "temp.mp4"
    video.save(video_path)

    model = whisper.load_model("base")
    result = model.transcribe(video_path)
    os.remove(video_path)

    return jsonify({"captions": result["text"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
