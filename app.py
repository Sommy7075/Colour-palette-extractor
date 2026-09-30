import numpy as np
from flask import Flask, render_template, request
from PIL import Image, UnidentifiedImageError
from werkzeug.exceptions import RequestEntityTooLarge
import base64
import io

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB limit


def get_top_colors(img, n=10):
    img = img.convert("RGB")           # handles PNG alpha / palette modes
    img.thumbnail((200, 200))          # shrink for speed
    pixels = np.array(img).reshape(-1, 3)
    pixels = (pixels // 8) * 8 + 4     # bucket similar shades, centred
    colors, counts = np.unique(pixels, axis=0, return_counts=True)
    top = np.argsort(counts)[::-1][:n]
    return ["#{:02x}{:02x}{:02x}".format(*colors[i]) for i in top]


@app.route("/", methods=["GET", "POST"])
def home():
    colors, error, image_data = None, None, None
    if request.method == "POST":
        file = request.files.get("image")
        if file and file.filename:
            try:
                img = Image.open(file.stream)
                colors = get_top_colors(img)

                preview = img.convert("RGB")
                preview.thumbnail((400, 400))
                buf = io.BytesIO()
                preview.save(buf, format="JPEG")
                image_data = base64.b64encode(buf.getvalue()).decode()
            except UnidentifiedImageError:
                error = "That doesn't look like a valid image."
    return render_template("index.html", colors=colors, error=error, image_data=image_data)


@app.errorhandler(RequestEntityTooLarge)
def too_large(e):
    return render_template("index.html", colors=None, error="File too large (max 5 MB)."), 413


if __name__ == "__main__":
    app.run(debug=True)