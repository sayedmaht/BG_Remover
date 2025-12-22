import streamlit as st
from rembg import remove
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="Background Remover",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Title
st.title("🎯 Background Remover")
st.markdown("Remove image backgrounds automatically using AI")

# File uploader
st.subheader("Upload an Image")
uploaded_file = st.file_uploader(
    "Choose an image file",
    type=["jpg", "jpeg", "png"],
    help="Supported formats: JPG, JPEG, PNG"
)

# Main logic
if uploaded_file is not None:
    try:
        # Load image
        image = Image.open(uploaded_file)
        
        # Display original image
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original Image")
            st.image(image, use_column_width=True)
        
        # Button to remove background
        if st.button("Remove Background", type="primary", use_container_width=True):
            with st.spinner("Processing... This may take a moment"):
                # Convert image to bytes
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                # Remove background
                result_bytes = remove(byte_im)
                
                # Display result
                result_image = Image.open(io.BytesIO(result_bytes))
                
                with col2:
                    st.subheader("Result")
                    st.image(result_image, use_column_width=True)
                
                # Download button
                st.download_button(
                    label="Download Image",
                    data=result_bytes,
                    file_name="no_bg.png",
                    mime="image/png",
                    use_container_width=True
                )
                
                st.success("Background removed successfully!")
    
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        st.info("Please try with a different image or make sure it's a valid image file.")
else:
    st.info("Upload an image to get started!")
    st.markdown("""
    ### How it works:
    1. Upload an image (JPG, JPEG, or PNG)
    2. Click the 'Remove Background' button
    3. Download the result
    
    The app uses AI to automatically detect and remove backgrounds from your images.
    """)
