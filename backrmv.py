import streamlit as st
from rembg import remove
from PIL import Image
import io

# Page configuration
st.set_page_config(page_title="Background Remover", page_icon="Ħ", layout="centered")

# Title and description
st.title("Ħ Background Remover")
st.markdown("""
Remove image backgrounds effortlessly using AI. Upload a photo and get instant results!
""")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], help="Upload a JPG, JPEG, or PNG image")

if uploaded_file is not None:
    try:
        # Load and display original image
        image = Image.open(uploaded_file)
        st.image(image, caption='Original Image', use_column_width=True)
        
        # Button to remove background
        if st.button('Remove Background', type="primary", use_container_width=True):
            with st.spinner('Processing your image... This may take a moment.'):
                # Convert image to bytes
                buf = io.BytesIO()
                image.save(buf, format='PNG')
                byte_im = buf.getvalue()
                
                # Remove background using rembg
                result_bytes = remove(byte_im)
                
                # Convert back to image for display
                result_image = Image.open(io.BytesIO(result_bytes))
                st.image(result_image, caption='Background Removed', use_column_width=True)
                
                # Download button
                st.download_button(
                    label="Download Image",
                    data=result_bytes,
                    file_name="no_bg.png",
                    mime="image/png",
                    use_container_width=True
                )
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please try uploading a different image.")
else:
    st.info("📄 Please upload an image to get started!")
