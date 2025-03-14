from flask import Flask, render_template, request, send_from_directory
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
COMPRESSED_FOLDER = "compressed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["COMPRESSED_FOLDER"] = COMPRESSED_FOLDER


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "image" not in request.files:
        return "No file uploaded", 400

    file = request.files["image"]
    if file.filename == "":
        return "No file selected", 400

    compression_level = int(request.form.get("quality", 40))
    output_format = request.form.get("format", "JPEG")

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    filename, ext = os.path.splitext(file.filename)
    compressed_filename = f"{filename}_compressed.{output_format.lower()}"
    compressed_path = os.path.join(app.config["COMPRESSED_FOLDER"], compressed_filename)

    try:
        image = Image.open(filepath)

        if output_format == "JPEG":
            image = image.convert("RGB")  # Ensure JPEG compatibility
            image.save(compressed_path, "JPEG", quality=compression_level)
        elif output_format == "PNG":
            image.save(compressed_path, "PNG", optimize=True, compress_level=int((100 - compression_level) / 10))
        elif output_format == "WEBP":
            image.save(compressed_path, "WEBP", quality=compression_level)
        else:
            return "Invalid format selected", 400

        return send_from_directory(app.config["COMPRESSED_FOLDER"], compressed_filename, as_attachment=True)

    except Exception as e:
        return f"Compression error: {str(e)}", 500


if __name__ == "__main__":
    app.run(debug=True)
