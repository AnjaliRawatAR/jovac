from flask import Flask, render_template, request, send_file
import os
from audio_processing import process_audio, save_audio

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    modulation_type = request.form.get('modulation')
    param = request.form.get('param')
    param = float(param) if param else None

    audio_file = request.files['audio_data']
    file_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
    audio_file.save(file_path)

    processed_data, sr = process_audio(file_path, modulation_type, param)
    processed_file_path = os.path.join(PROCESSED_FOLDER, 'processed_' + audio_file.filename)
    save_audio(processed_data, processed_file_path)

    return send_file(processed_file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(port=5555 ,debug=True)
