import streamlit as st
from rembg import remove
from PIL import Image
import io

st.title("Background Remover")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Original Image', use_column_width=True)
    
    if st.button('Remove Background'):
        with st.spinner('Processing...'):
            # Convert image to bytes
            buf = io.BytesIO()
            image.save(buf, format='PNG')
            byte_im = buf.getvalue()
            
            # Remove background
            result_bytes = remove(byte_im)
            
            # Convert back to image for display
            result_image = Image.open(io.BytesIO(result_bytes))
            st.image(result_image, caption='Background Removed', use_column_width=True)
            
            # Download button
            st.download_button(
                label="Download Image",
                data=result_bytes,
                file_name="no_bg.png",
                mime="image/png"
            )
