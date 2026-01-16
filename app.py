# =============================================================
# 💸 Intelligent Forgery Currency Detection System (Multilingual)
# =============================================================

# ----------------- Standard Library -----------------
import os
import base64
import warnings
from typing import Dict, Tuple
from datetime import datetime

# ----------------- Third-Party -----------------
import numpy as np
import cv2
import streamlit as st
from tensorflow.keras.models import load_model
from PIL import Image
import pandas as pd

# =============================================================
# 1) Global App Settings
# =============================================================
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="💸 Intelligent Forgery Currency Detection System",
    layout="centered",
)
# =============================================================
# 2) Global CSS (Enhanced UI + Bigger Language Dropdown)
# =============================================================
st.markdown(
    """
<style>
/* Background with gradient + blur */
.stApp {
    background: linear-gradient(135deg, #141E30, #243B55);
    color: white !important;
}
/* Style the "🌐 Select Language" label */
.stSelectbox label {
    font-size: 35px !important;
    font-weight: bold !important;
    color: #fff !important;   /* white label text */
}

/* Style the selected item and dropdown options */
.stSelectbox div[data-baseweb="select"] span {
    font-size: 35px !important;
    color: #000 !important;   /* black dropdown text */
}



/* Tabs */
div[data-baseweb="tab-list"] {
    display: flex !important;
    justify-content: center !important;
    gap: 20px !important;
    background: rgba(255,255,255,0.1);
    border-radius: 25px;
    padding: 10px 20px;
    margin: 0 auto 25px auto;
    backdrop-filter: blur(8px);
}
div[data-baseweb="tab"] { padding: 10px 18px !important; border-radius: 12px !important; }
[data-baseweb="tab"] * { font-size: 24px !important; font-weight: bold !important; color: white !important; }
div[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #4CAF50, #2E7D32) !important;
    transform: scale(1.08) !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
}

/* Title Banner */
.title-banner {
    text-align: center;
    background: linear-gradient(90deg, #ff512f, #dd2476);
    color: white;
    padding: 20px;
    border-radius: 14px;
    font-size: 34px;
    font-weight: bold;
    margin-bottom: 20px;
    animation: fadeInDown 1s ease;

    width: 100%;         /* ✅ Take full width */
    display: block;      /* ✅ Ensure it behaves like a block element */
    box-sizing: border-box; /* ✅ Include padding in width */
}




/* Upload & Webcam Sections (Glassmorphism) */
.upload-section, .webcam-section {
    background: rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 25px;
    margin-top: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    backdrop-filter: blur(12px);
    color: #fff;
}

/* Result Card */
.result-card {
    text-align:center; 
    padding:20px; 
    border-radius:15px; 
    margin-top: 20px;
    font-weight: 900;
    animation: fadeInUp 0.8s ease;
}
.result-real { background: rgba(46, 204, 113,0.85); color: white; }
.result-fake { background: rgba(231, 76, 60,0.85); color: white; }
.result-invalid { background: rgba(149, 165, 166,0.85); color: white; }

/* Predict Button */
.stButton button {
    font-size: 28px !important;
    font-weight: 900 !important;
    padding: 14px 28px !important;
    border-radius: 12px !important;
    background: linear-gradient(90deg, #00c6ff, #0072ff) !important;
    color: #fff !important;
    cursor: pointer !important;
    border: none !important;
    transition: all 0.3s ease-in-out;
}
.stButton button:hover {
    transform: scale(1.08) !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3) !important;
}

/* Download Button */
.download-btn {
    margin-top:15px;
    padding:12px 24px;
    font-size:20px;
    font-weight:bold;
    border-radius:10px;
    background: linear-gradient(90deg, #2ecc71, #27ae60);
    color:white;
    border:none;
    cursor:pointer;
    transition: 0.3s ease-in-out;
}
.download-btn:hover {
    transform: scale(1.05);
}

/* Bigger Language Dropdown */
label[data-baseweb="select"] > div {
    font-size: 28px !important; 
    font-weight: bold !important;
    color: #fff !important;
}
div[data-baseweb="select"] span {
    font-size: 28px !important;  
    color: #000 !important;
}

/* Footer */
.footer {
    position: fixed;
    bottom: 8px;
    width: 100%;
    text-align: center;
    font-size: 14px;
    color: #ccc;
    font-style: italic;
}
/* Style for the "📷 Take Photo" label in camera input */
.stCameraInput label {
    font-size: 26px !important;
    font-weight: bold !important;
    color: black !important;  /* Change to your desired color */
}


/* Animations */
@keyframes fadeInDown {
    from { opacity:0; transform: translateY(-30px); }
    to { opacity:1; transform: translateY(0); }
}
@keyframes fadeInUp {
    from { opacity:0; transform: translateY(30px); }
    to { opacity:1; transform: translateY(0); }
}
</style>
""",
    unsafe_allow_html=True,
)

# =============================================================
# 3) Multilingual Text
# =============================================================
LANGUAGES = ["English", "हिन्दी"]

TEXT: Dict[str, Dict] = {
    "English": {
        "title": "💸 Intelligent Forgery Currency Detection System",
        "upload_tab": "📁 Upload Image",
        "webcam_tab": "📷 Capture with Webcam",
        "upload_heading": "📤 Upload a Currency Note Image",
        "camera_heading": "📸 Capture a Currency Note Using Your Webcam",
        "predict_button": "🔍 Predict",
        "download_report": "📥 Download Result",
        "confidence": "Confidence",
        "class_labels": {
            "Real Currency": "Real Currency",
            "Fake Currency": "Fake Currency",
            "Invalid Image": "Invalid Image",
        },
        "analyzing": "Analyzing the currency note...",
    },
    "हिन्दी": {
        "title": "💸 बुद्धिमान नकली मुद्रा पहचान प्रणाली",
        "upload_tab": "📁 छवि अपलोड करें",
        "webcam_tab": "📷 वेबकैम से कैप्चर करें",
        "upload_heading": "📤 मुद्रा नोट की छवि अपलोड करें",
        "camera_heading": "📸 वेबकैम से मुद्रा नोट कैप्चर करें",
        "predict_button": "🔍 परिणाम ज्ञात करें",
        "download_report": "📥 परिणाम डाउनलोड करें",
        "confidence": "विश्वास स्तर",
        "class_labels": {
            "Real Currency": "असली मुद्रा",
            "Fake Currency": "नकली मुद्रा",
            "Invalid Image": "अमान्य छवि",
        },
        "analyzing": "मुद्रा नोट का विश्लेषण किया जा रहा है...",
    },
}



# =============================================================
# 4) Load Model
# =============================================================
MODEL_PATH = "model/Fake-currency.keras"

@st.cache_resource(show_spinner=False)
def load_trained_model():
    return load_model(MODEL_PATH)

try:
    model = load_trained_model()
except Exception as e:
    st.error(f"⚠️ Error loading model: {e}")
    st.stop()

CLASS_NAMES = ["Fake Currency", "Invalid Image", "Real Currency"]

# =============================================================
# 5) Preprocess & Predict
# =============================================================
CONFIDENCE_INVALID_THRESHOLD = 60.0

def preprocess(img: np.ndarray) -> np.ndarray:
    img_resized = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
    img_normalized = (img_resized.astype(np.float32) / 255.0)
    return np.expand_dims(img_normalized, axis=0)

def predict(img: np.ndarray) -> Tuple[str, float, np.ndarray]:
    processed = preprocess(img)
    preds = model.predict(processed, verbose=0)
    probs = preds[0]
    top_idx = int(np.argmax(probs))
    top_conf = float(probs[top_idx]) * 100.0
    label = CLASS_NAMES[top_idx]
    if top_conf < CONFIDENCE_INVALID_THRESHOLD:
        label = "Invalid Image"
    return label, top_conf, probs
# =============================================================
# 6) Handle Image
# =============================================================
def handle_image(img_array: np.ndarray) -> None:
    st.image(img_array, use_container_width=True)
    if st.button(lang["predict_button"], use_container_width=True, key="unique_predict_button_1"):
        with st.spinner(lang["analyzing"]):
            label, confidence, _ = predict(img_array)
        display_result(label, confidence)

# =============================================================
# 7) Display Result (with CSV Logging)
# =============================================================
def display_result(label: str, confidence: float) -> None:
    label_translated = lang["class_labels"].get(label, label)

    if label == "Real Currency":
        css_class = "result-real"
    elif label == "Fake Currency":
        css_class = "result-fake"
    else:
        css_class = "result-invalid"

    # Save to history.csv
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_new = pd.DataFrame([[timestamp, label_translated, confidence]], 
                          columns=["Timestamp", "Label", "Confidence %"])
    if not os.path.exists("history.csv"):
        df_new.to_csv("history.csv", index=False)
    else:
        df_new.to_csv("history.csv", mode="a", header=False, index=False)

    # Show Result Card
    st.markdown(
        f"""
        <div class="result-card {css_class}">
            <h2 style="font-size:32px;">{label_translated}</h2>
            <p style="font-size:22px;">{lang['confidence']}: {confidence:.2f}%</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Download Result
    report_txt = f"Prediction: {label_translated}\n{lang['confidence']}: {confidence:.2f}%"
    b64 = base64.b64encode(report_txt.encode()).decode()
    st.markdown(
        f"""<a href="data:file/txt;base64,{b64}" download="result.txt">
            <button class="download-btn">📥 {lang['download_report']}</button>
        </a>""",
        unsafe_allow_html=True,
    )



# =============================================================
# 8) Main App
# =============================================================
st.markdown('<div class="title-banner">💸 Intelligent Forgery Currency Detection System</div>', unsafe_allow_html=True)
selected_lang = st.selectbox("🌐 Select Language", LANGUAGES, index=0)
lang = TEXT[selected_lang]



tab1, tab2 = st.tabs([lang["upload_tab"], lang["webcam_tab"]])

with tab1:
    st.markdown(f"<div class='upload-section'><h3 style='text-align:center'>{lang['upload_heading']}</h3></div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        img_array = np.array(Image.open(uploaded_file).convert("RGB"))
        handle_image(img_array)

with tab2:
    st.markdown(f"<div class='webcam-section'><h3 style='text-align:center'>{lang['camera_heading']}</h3></div>", unsafe_allow_html=True)
    img_file_buffer = st.camera_input("")
    if img_file_buffer is not None:
        img_array = np.array(Image.open(img_file_buffer).convert("RGB"))
        handle_image(img_array)

# =============================================================
# Footer
# =============================================================
