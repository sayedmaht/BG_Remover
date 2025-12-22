import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="Background Remover", layout="centered")

st.title("🎯 Background Remover")
st.markdown("Remove backgrounds from images using advanced AI")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload Image")
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    try:
        image = Image.open(uploaded_file)
        with col1:
            st.image(image, caption="Original", use_column_width=True)
        
        if st.button("Remove Background", type="primary", use_container_width=True):
            with st.spinner("Processing..."):
                try:
                    from rembg import remove
                    input_bytes = io.BytesIO()
                    image.save(input_bytes, format="PNG")
                    output_bytes = remove(input_bytes.getvalue())
                    output_image = Image.open(io.BytesIO(output_bytes))
                    
                    with col2:
                        st.subheader("Result")
                        st.image(output_image, caption="Background Removed", use_column_width=True)
                    
                    st.download_button(
                        "Download",
                        data=output_bytes,
                        file_name="no_bg.png",
                        mime="image/png",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Processing failed: {str(e)[:100]}")
                    st.info("Try a different image")
    except Exception as e:
        st.error("Invalid image file")
else:
    st.info("📤 Upload an image to start")
