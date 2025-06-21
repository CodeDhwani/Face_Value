import streamlit as st
import requests
from PIL import Image

# Page setup
st.set_page_config(page_title="AI Face Analyzer", layout="centered")

# Custom title style
st.markdown(
    """
    <style>
        .title {
            font-size: 42px;
            color: #4CAF50;
            text-align: center;
        }
        .subtitle {
            font-size: 20px;
            text-align: center;
            color: #888;
        }
        .result-title {
            font-size: 24px;
            font-weight: bold;
            color: #FF6F00;
            margin-top: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">🧠 AI Facial Recognition System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload a photo to detect Age, Gender, Emotion, and Race</div>', unsafe_allow_html=True)
st.markdown("---")

# Upload image
uploaded_file = st.file_uploader("📤 Upload an image file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼️ Uploaded Image", use_column_width=True)

    with st.spinner("🔍 Analyzing face..."):
        try:
            files = {"file": uploaded_file.getvalue()}
            response = requests.post("http://127.0.0.1:8000/analyze/", files=files)

            st.markdown("### 🧾 Raw Response (for debug):")
            st.code(response.text)

            if response.status_code != 200:
                st.error(f"❌ Error {response.status_code}: {response.text}")
            else:
                result = response.json()
                if "error" in result:
                    st.error(f"🚫 Error: {result['error']}")
                else:
                    st.markdown('<div class="result-title">✅ Analysis Results</div>', unsafe_allow_html=True)

                    col1, col2 = st.columns(2)
                    col1.metric("👶 Age", int(result.get("age", 0)))
                    col2.metric("🧑 Dominant Gender", result.get("dominant_gender", "N/A"))

                    col3, col4 = st.columns(2)
                    col3.metric("🌍 Dominant Race", result.get("dominant_race", "N/A"))
                    col4.metric("😊 Dominant Emotion", result.get("dominant_emotion", "N/A"))

                    st.success("Analysis complete!")

        except Exception as e:
            st.error(f"⚠️ Exception occurred: {e}")
