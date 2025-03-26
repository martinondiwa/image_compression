# python code responsible for the image compression

from flask import Flask, render_template, request, jsonify, send_from_directory
import io
import os
from PIL import Image
import zipfile
import cv2
from moviepy import VideoFileClip

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

@app.route('/compression')
def compression():
        return render_template('compression.html')

@app.route('/compression/single')
def single_compression():
    return render_template('single_compression.html')

@app.route('/compression/multiple')
def multiple_compression():
    return render_template('multiple_compression.html')

@app.route('/compression/video')
def video_compression():
    return render_template('video_compression.html')
    
@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
    
@app.route('/compress', methods=['POST'])
def compress_image():
    if 'image' not in request.files or 'quality' not in request.form:
        return "Missing data", 400

    file = request.files['image']
    compression_level = int(request.form['quality'])  # Get user-selected compression level

    try:
        img = Image.open(file)

        # Convert image to RGB mode if it's not in a compressible format (e.g., PNG, TIFF)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Define quality settings based on selection
        quality_mapping = {
            25: 25,  # High compression (smallest size)
            50: 50,  # Medium compression (balanced)
            75: 75   # Low compression (best quality)
        }
        quality = quality_mapping.get(compression_level, 50)  # Default to 50%

        # Save compressed image in memory
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG', quality=quality, optimize=True)
        img_io.seek(0)

        return send_file(img_io, mimetype='image/jpeg', as_attachment=False)
    
    except Exception as e:
        return str(e), 500
        
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
