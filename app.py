from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
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
        return jsonify({"error": "Missing image or quality parameter"}), 400

    file = request.files['image']
    compression_level = int(request.form['quality'])  # Get user-selected compression level

    try:
        img = Image.open(file)

        # Convert PNG, TIFF, and other non-JPEG formats to RGB mode
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Define compression quality mapping
        quality_mapping = {25: 25, 50: 50, 75: 75}
        quality = quality_mapping.get(compression_level, 50)  # Default 50%

        # Save the compressed image
        compressed_filename = "compressed_image.jpg"
        compressed_path = os.path.join(COMPRESSED_FOLDER, compressed_filename)
        img.save(compressed_path, "JPEG", quality=quality, optimize=True)

        return jsonify({"compressed_url": f"/download/{compressed_filename}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Renamed function to avoid conflict
@app.route('/download')
def download_static_file():
    filename = request.args.get('filename')
    if not filename:
        return "No file specified", 400
    file_path = os.path.join(COMPRESSED_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

# ✅ Keeps dynamic filename handling
@app.route('/download/<filename>')
def download_dynamic_file(filename):
    return send_from_directory(COMPRESSED_FOLDER, filename, as_attachment=True)

@app.route("/compress/multiple", methods=["POST"])
def compress_multiple():
    files = request.files.getlist("images")
    compression_level = int(request.form.get("quality", 50))  # Default to 50%

    quality_mapping = {25: 25, 50: 50, 75: 75}
    quality = quality_mapping.get(compression_level, 50)

    compressed_image_urls = []

    for file in files:
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        compressed_path = os.path.join(COMPRESSED_FOLDER, filename)

        file.save(file_path)
        image = Image.open(file_path)
        image.save(compressed_path, "JPEG", quality=quality, optimize=True)

        compressed_image_urls.append(f"/compressed/{filename}")

    return jsonify({"success": True, "images": compressed_image_urls})

@app.route("/compressed/<filename>")
def get_compressed_image(filename):
    return send_from_directory(COMPRESSED_FOLDER, filename)
    
@app.route('/compress/video', methods=['POST'])
def compress_video():
    file = request.files['video']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    compressed_path = os.path.join(COMPRESSED_FOLDER, file.filename)

    file.save(file_path)
    clip = VideoFileClip(file_path)
    clip.write_videofile(compressed_path, bitrate="500k")

    return jsonify({"success": True, "url": f"/download/{file.filename}"})

if __name__ == '__main__':
    app.run(debug=True)
