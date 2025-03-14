from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from PIL import Image
import zipfile
import cv2
from moviepy.editor import VideoFileClip

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/compression/single')
def single_compression():
    return render_template('single_compression.html')

@app.route('/compression/multiple')
def multiple_compression():
    return render_template('multiple_compression.html')

@app.route('/compression/video')
def video_compression():
    return render_template('video_compression.html')

@app.route('/compress/single', methods=['POST'])
def compress_single():
    file = request.files['image']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    compressed_path = os.path.join(COMPRESSED_FOLDER, file.filename)

    file.save(file_path)
    image = Image.open(file_path)
    image.save(compressed_path, "JPEG", quality=50)

    return jsonify({"success": True, "url": f"/download/{file.filename}"})

@app.route('/compress/multiple', methods=['POST'])
def compress_multiple():
    files = request.files.getlist('images')
    zip_path = os.path.join(COMPRESSED_FOLDER, "compressed_images.zip")

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in files:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            compressed_path = os.path.join(COMPRESSED_FOLDER, file.filename)

            file.save(file_path)
            image = Image.open(file_path)
            image.save(compressed_path, "JPEG", quality=50)
            zipf.write(compressed_path, file.filename)

    return jsonify({"success": True, "url": "/download/compressed_images.zip"})

@app.route('/compress/video', methods=['POST'])
def compress_video():
    file = request.files['video']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    compressed_path = os.path.join(COMPRESSED_FOLDER, file.filename)

    file.save(file_path)
    clip = VideoFileClip(file_path)
    clip.write_videofile(compressed_path, bitrate="500k")

    return jsonify({"success": True, "url": f"/download/{file.filename}"})

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(COMPRESSED_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
