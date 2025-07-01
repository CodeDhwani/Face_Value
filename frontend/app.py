import streamlit as st
import requests
from PIL import Image
from fpdf import FPDF

# -----------------------------
# 🎨 Page Configuration
# -----------------------------
st.set_page_config(page_title="FaceValue", layout="centered")

# -----------------------------
# 💅 Custom CSS Styling
# -----------------------------
st.markdown(
    """
    <style>
        body {
            background-color: #f2f4f7;
        }
        .title {
            font-size: 48px;
            color: #3B82F6;
            text-align: center;
            font-weight: bold;
            margin-top: 20px;
        }
        .subtitle {
            font-size: 18px;
            text-align: center;
            color: #555;
        }
        .quote {
            font-size: 20px;
            font-style: italic;
            color: #9333EA;
            text-align: center;
            margin-top: 20px;
        }
        .result-header {
            font-size: 36px;
            font-weight: 700;
            text-align: center;
            color: #1F2937;
            margin-bottom: 30px;
        }
        .card {
            background-color: white;
            padding: 40px 20px;
            border-radius: 16px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            text-align: center;
            height: 180px;
        }
        .card-title {
            font-size: 18px;
            color: #6B7280;
            margin-bottom: 10px;
        }
        .card-value {
            font-size: 32px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# 🧠 FaceValue Title
# -----------------------------
st.markdown('<div class="title">FaceValue</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload a photo to detect Age, Gender, Emotion, and Race</div>', unsafe_allow_html=True)
st.markdown("---")

# -----------------------------
# 📤 File Upload
# -----------------------------
uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

# -----------------------------
# 🧾 Quote Generator
# -----------------------------
def get_savage_quote(emotion, gender):
    quotes = {
        "happy": "Keep shining—your smile’s your super-power!",
        "angry": "Grace in chaos is your real flex.",
        "sad": "The storm inside you creates rainbows outside.",
        "neutral": "Unbothered. Unfazed. Unmatched.",
        "fear": "You wear courage like second skin.",
        "disgust": "Sharp eyes. Sharper instincts.",
        "surprise": "Born to break the algorithm.",
    }

    gender_quote = {
        "man": "Power isn't claimed—it's sensed.",
        "woman": "She believed, and now the world adjusts.",
    }

    final_quote = quotes.get(emotion.lower(), "Own your vibe. You’re the standard.")
    if gender.lower() in gender_quote:
        final_quote += f" {gender_quote[gender.lower()]}"
    return final_quote

# -----------------------------
# 📄 PDF CERTIFICATE GENERATOR
# -----------------------------
LATIN1_SAFE = str.maketrans("’–—“”", "'--\"\"")
def latin1(s: str) -> str:
    return s.translate(LATIN1_SAFE)

def build_certificate(name="FaceValue User", age=None, gender=None, race=None, emotion=None):
    pdf = FPDF(orientation='P', unit='pt', format='A4')
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(59, 130, 246)
    pdf.cell(0, 40, "FaceValue Personality Certificate", ln=True, align="C")

    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(80, 80, 80)
    pdf.ln(20)
    pdf.cell(0, 20, f"This is to certify that {name} has been analyzed by FaceValue AI.", ln=True, align="C")

    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(30)
    pdf.cell(0, 24, f"Age: {age}", ln=True, align="C")
    pdf.cell(0, 24, f"Gender: {gender}", ln=True, align="C")
    pdf.cell(0, 24, f"Race: {race}", ln=True, align="C")
    pdf.cell(0, 24, f"Emotion: {emotion}", ln=True, align="C")

    pdf.set_text_color(148, 0, 211)
    pdf.set_font("Helvetica", "I", 13)
    pdf.ln(30)
    quote = get_savage_quote(emotion, gender)

    # Ensure quote is Latin-1 friendly
    quote = quote.encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(0, 20, f'"{quote}"', align="C")

    return pdf.output(dest="S").encode("latin-1", "replace")


# -----------------------------
# ✅ ANALYSIS + UI DISPLAY
# -----------------------------
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼️ Uploaded Image", use_container_width=True)

    with st.spinner("🔍 Analyzing face..."):
        try:
            files = {"file": uploaded_file.getvalue()}
            response = requests.post("http://127.0.0.1:8000/analyze/", files=files)

            if response.status_code != 200:
                st.error(f"❌ Error {response.status_code}: {response.text}")
            else:
                result = response.json()

                if "error" in result:
                    st.error(f"🚫 Error: {result['error']}")
                else:
                    age = result.get("age", "N/A")
                    gender = result.get("dominant_gender", "N/A")
                    race = result.get("dominant_race", "N/A")
                    emotion = result.get("dominant_emotion", "N/A")

                    st.markdown('<div class="result-header">Results</div>', unsafe_allow_html=True)

                    # Display results in cards
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f'<div class="card"><div class="card-title">Age</div><div class="card-value" style="color:#EF4444;">{age}</div></div>', unsafe_allow_html=True)
                    with col2:
                        st.markdown(f'<div class="card"><div class="card-title">Gender</div><div class="card-value" style="color:#0EA5E9;">{gender}</div></div>', unsafe_allow_html=True)

                    col3, col4 = st.columns(2)
                    with col3:
                        st.markdown(f'<div class="card"><div class="card-title">Race</div><div class="card-value" style="color:#10B981;">{race}</div></div>', unsafe_allow_html=True)
                    with col4:
                        st.markdown(f'<div class="card"><div class="card-title">Emotion</div><div class="card-value" style="color:#F59E0B;">{emotion}</div></div>', unsafe_allow_html=True)

                    # Add a savage quote
                    quote = get_savage_quote(emotion, gender)
                    st.markdown(f'<div class="quote">“{quote}”</div>', unsafe_allow_html=True)

                    # Generate PDF certificate
                    pdf_bytes = build_certificate(age=age, gender=gender, race=race, emotion=emotion)
                    st.download_button(
                        label="📥 Download FaceValue Certificate",
                        data=pdf_bytes,
                        file_name="facevalue_certificate.pdf",
                        mime="application/pdf"
                    )

                    # Optional: Raw JSON
                    with st.expander("📦 Raw JSON Response"):
                        st.json(result)

        except Exception as e:
            st.error(f"⚠️ Exception occurred: {e}")
