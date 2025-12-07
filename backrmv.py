from flask import Flask, request, send_file, render_template_string
import cv2
import numpy as np
from rembg import remove
import io

app = Flask(__name__)

# Simple HTML form for upload
HTML_FORM = """
<!doctype html>
<title>Background Remover</title>
<h1>Upload an image to remove background</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
"""

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if not file:
            return "No file uploaded", 400

        # Read image into numpy array
        file_bytes = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Remove background
        result = remove(image)

        # Encode result as PNG in memory
        _, buffer = cv2.imencode(".png", result)
        return send_file(
            io.BytesIO(buffer),
            mimetype="image/png",
            as_attachment=True,
            download_name="output_image.png"
        )

    return render_template_string(HTML_FORM)

if __name__ == "__main__":
    app.run(debug=True)

# --- File Upload ---
uploaded_file = st.file_uploader(
    "📤 Upload an image file",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.subheader("Original Image")
    st.image(image, width=400)

    with st.spinner("Removing background..."):
        result = remove(image)  # directly use PIL image

    st.subheader("Background Removed")
    st.image(result, width=400)

    buf = io.BytesIO()
    result.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="⬇️ Download background‑removed image",
        data=byte_im,
        file_name="output_image.png",
        mime="image/png"
    )




