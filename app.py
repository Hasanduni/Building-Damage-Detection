import streamlit as st
import cv2
import numpy as np
import tempfile
import google.generativeai as genai
from PIL import Image
import os

# ✅ Configure Gemini API
GOOGLE_API_KEY = "AIzaSyABcgB6_ekXpU1FffEt9ANh2fLEMWRbLu8"  
if not GOOGLE_API_KEY:
    st.error("🚨 Please set your GOOGLE_API_KEY as an environment variable in Streamlit Cloud.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-pro")

st.set_page_config(page_title="🏚 Building Damage Detector", layout="centered")

st.title("🏚 Building Damage Identification")
st.write("Upload a building image (post-disaster) to analyze damage severity and get recommendations.")

# ✅ File uploader
uploaded_file = st.file_uploader("📤 Upload Building Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    image.save(temp_file.name)

    if st.button("🔍 Analyze Damage"):
        with st.spinner("Analyzing building damage... ⏳"):
            try:
                # ✅ Send image + prompt to Gemini
                prompt = (
                    "Analyze this image of a building after a disaster. "
                    "Provide:\n"
                    "1. Severity of damage (Low / Moderate / Severe / Collapse)\n"
                    "2. Type of damage (e.g., cracks, roof collapse, broken walls, debris)\n"
                    "3. Suggested emergency action."
                )

                response = model.generate_content([prompt, genai.upload_file(temp_file.name)])
                st.success("✅ Analysis complete!")
                st.subheader("📄 Building Damage Report")
                st.write(response.text)

            except Exception as e:
                st.error(f"❌ Gemini API Error: {e}")
