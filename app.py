from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageFilter, ImageEnhance
import io

app = Flask(__name__)

ALLOWED_FILTERS = {
    "blur": lambda img: img.filter(ImageFilter.BLUR),
    "sharpen": lambda img: img.filter(ImageFilter.SHARPEN),
    "grayscale": lambda img: img.convert("L").convert("RGB"),
    "contour": lambda img: img.filter(ImageFilter.CONTOUR),
    "brightness": lambda img: ImageEnhance.Brightness(img).enhance(1.5),
}


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/filters")
def list_filters():
    return jsonify({"filters": list(ALLOWED_FILTERS.keys())})


@app.route("/apply", methods=["POST"])
def apply_filter():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    filter_name = request.args.get("filter", "blur")
    if filter_name not in ALLOWED_FILTERS:
        return jsonify({"error": f"Unknown filter '{filter_name}'"}), 400

    image_file = request.files["image"]
    try:
        img = Image.open(image_file.stream).convert("RGB")
    except Exception:
        return jsonify({"error": "Invalid image"}), 400

    result = ALLOWED_FILTERS[filter_name](img)

    buf = io.BytesIO()
    result.save(buf, format="JPEG")
    buf.seek(0)
    return send_file(buf, mimetype="image/jpeg", download_name="filtered.jpg")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
