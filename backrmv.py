import streamlit as st
import requests
from PIL import Image
import io
import os

st.set_page_config(page_title="Background Remover", layout="centered")
st.title("🎯 Background Remover")

st.markdown("""
Upload an image and remove its background instantly using AI!
""")

upload = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if upload:
    img = Image.open(upload)
    st.image(img, caption="Original", use_column_width=True)
    
    if st.button("Remove Background"):
        st.info("Processing with AI... This may take a moment.")
        
        try:
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)
            
HF_TOKEN = os.getenv("HF_TOKEN", "")            API_URL = "https://api-inference.huggingface.co/models/briaai/BRIA-2.0-RMBG-ViT-B"
            
            headers = {"Authorization": f"Bearer {HF_TOKEN}"}
            response = requests.post(API_URL, headers=headers, data=img_bytes.getvalue())
            
            if response.status_code == 200:
                result = Image.open(io.BytesIO(response.content))
                st.image(result, caption="Background Removed", use_column_width=True)
                
                result_bytes = io.BytesIO()
                result.save(result_bytes, format="PNG")
                result_bytes.seek(0)
                
                st.download_button(
                    "Download Result",
                    data=result_bytes.getvalue(),
                    file_name="no_bg.png",
                    mime="image/png"
                )
                st.success("Done!")
            else:
                st.error(f"API Error: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {str(e)[:100]}")
else:
    st.info("Upload an image to start")
