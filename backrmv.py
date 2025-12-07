import numpy as np
from rembg import remove
import streamlit as st
from PIL import Image
import io

# --- Page Config ---
st.set_page_config(
    page_title="AI Background Remover",
    page_icon="🖼️",
    layout="centered"
)

# --- Header ---
st.title("🖼️ AI Background Remover")
st.markdown(
    """
    Upload any image and instantly remove its background.  
    Download the processed image as a PNG with transparency.
    """
)

# --- File Upload ---
uploaded_file = st.file_uploader(
    "📤 Upload an image file",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    # Show original image
    image = Image.open(uploaded_file)
    st.subheader("Original Image")
    st.image(image, width=400)

    # Convert to numpy
    image_np = np.array(image)

    # Remove background
    with st.spinner("Removing background..."):
        result = remove(image_np)

    # Show result
    st.subheader("Background Removed")
    st.image(result, width=400)

    # Convert result to PNG bytes
    result_pil = Image.fromarray(result)
    buf = io.BytesIO()
    result_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()

    # Download button
    st.download_button(
        label="⬇️ Download background‑removed image",
        data=byte_im,
        file_name="output_image.png",
        mime="image/png"
    )

# --- Footer ---
st.markdown("---")
st.caption("Built with ❤️ using Streamlit + rembg + OpenCV")

