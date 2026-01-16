# 🛠️ Admin Panel for Intelligent Forgery Currency Detection System
# ================================================================

import os
import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px
import subprocess

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="🛠️ Admin Panel - Currency Detection",
    layout="wide"
)

# ---------------------------
# Initialize Session State
# ---------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------------------
# Custom CSS for Styling
# ---------------------------
st.markdown("""
    <style>
        /* Page background */
        .stApp {
            background-color: #141E30 !important;
        }
       
        .custom-admin-title {
            color:white !important;       /* Set any color you want */
            font-weight: 900 !important;
            font-size: 40px !important;
        }


        /* Headings */
        h3 {
            color: white !important;
            font-weight: 700;
        }
        h1 {
            font-size: 36px !important;
            text-align: center;
            color: black;
            font-weight: 800 !important;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
        }
         h2 {
            color: white !important;
            font-weight: 700;
        }

        /* KPI cards */
        div[data-testid="metric-container"] {
            background: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            text-align: center;
        }
        div[data-testid="metric-container"] > label {
            color: white !important;
            font-size: 16px !important;
        }
        div[data-testid="metric-container"] > div {
            font-size: 22px !important;
            font-weight: bold !important;
            color: white !important;
        }

        /* ✅ Download CSV button */
        div[data-testid="stDownloadButton"] button {
            font-size: 22px !important;
            font-weight: bold !important;
            color: black !important;
            background-color: #e0f7fa !important;
            border: 2px solid #26a69a !important;
            border-radius: 10px !important;
            padding: 14px 40px !important;
        }
        div[data-testid="stDownloadButton"] button:hover {
            background-color: #b2ebf2 !important;
            color: black !important;
        }

        /* Form / Buttons */
        .stDownloadButton button, .stForm button {
            font-size: 24px !important;
            font-weight: bold !important;
            text-transform: uppercase !important;
            padding: 14px 45px !important;
            border-radius: 10px !important;
            background-color: #e0f7fa !important;
            color: black !important;
            border: 2px solid #26a69a !important;
        }

        .stFormSubmitButton {
        display: flex !important;
        justify-content: center !important;
       }

    /* Style the button itself */
        .stFormSubmitButton button {
            font-size: 22px !important;
            font-weight: 700 !important;
            padding: 14px 36px !important;
            border-radius: 10px !important;
        }

    /* Style the text inside the button (inside <p>) */
        .stFormSubmitButton button p {
            font-size: 22px !important;
            font-weight: 700 !important;
        }
        /* Center the whole download button */
        .stDownloadButton {
            display: flex !important;
            justify-content: center !important;
        }

        /* Make button bigger and bold */
        .stDownloadButton button {
            font-size: 22px !important;
            font-weight: 800 !important;
            padding: 14px 40px !important;
            border-radius: 10px !important;
        }

        /* Style text inside <p> of the button */
        .stDownloadButton button p {
            font-size: 22px !important;
            font-weight: 800 !important;
        }
        .stDataFrame {
            border: 1px solid #dee2e6;
            border-radius: 12px;
            overflow: hidden;
        }

        /* Login inputs */
        div[data-testid="stTextInput"] label {
            font-size: 22px !important;
            font-weight: bold !important;
            color: white !important;
        }
        div[data-testid="stTextInput"] input {
            font-size: 20px !important;
            font-weight: 600 !important;
            color: black !important;
        }

        /* Delete buttons styling */
        div.stButton > button {
            font-size:18px !important;
            font-weight:bold !important;
            color: white !important;
            border-radius: 10px !important;
            padding: 8px 20px !important;
        }
        div.stButton > button:nth-child(1) {
            background-color: #e74c3c !important; /* Red */
        }
        div[role='radiogroup'] label div:first-child {
            color: #FFFFFF !important;      /* Change to any color */
            font-size: 24px !important;
            font-weight: bold !important;
        }
        div.stButton > button:nth-child(2) {
            background-color: #c0392b !important; /* Dark Red */
        }
        div[data-testid="stSelectbox"] label {
            color: white !important;      /* Change color here */
            font-size: 24px !important;
            font-weight: bold !important;
        }
        .stFileUploader label {
            color: white !important;
            font-size: 20px !important;
            font-weight: 600 !important;
        }
        .stRadio > label {
            color: white !important;      /* change color */
            font-size: 22px !important;     /* optional size change */
            font-weight: 600 !important;
        }
        hr {
            border: 1px solid #dee2e6;
            margin: 20px 0;
        }
      /* Targets the text content inside the success notification */
        div[data-testid="stNotification"] .st-bd p { 
            font-size: 24px !important; 
            font-weight: bold !important; 
            color: #0d1b2a !important; 
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="custom-admin-title">🛠️ Admin Panel - Currency Detection</h1>', unsafe_allow_html=True)

# ---------------------------
# Basic Authentication
# ---------------------------
USERNAME = "admin"
PASSWORD = "1234"

if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            """
            <div style="background-color: #ffffff; padding: 30px; 
                        border-radius: 15px; box-shadow: 0px 4px 15px rgba(0,0,0,0.2);">
                <h1 style='text-align: center; color:black;'>🔑 Secure Admin Login</h1>
            """,
            unsafe_allow_html=True,
        )

        with st.form("login_form", clear_on_submit=True):
            user = st.text_input("👤 Username", placeholder="Enter username")
            pwd = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            login = st.form_submit_button("➡️ Login")

            if login:
                if user == USERNAME and pwd == PASSWORD:
                    st.session_state.authenticated = True
                    st.session_state.username = user
                    st.markdown("""
                        <div style='background-color:#00b300; 
                                    color:white; 
                                    font-weight:600;
                                    text-align:center; 
                                    padding:10px; 
                                    border-radius:8px; 
                                    margin-top:10px;
                                    box-shadow:0 0 10px rgba(0,255,0,0.4);'>
                            ✅ Login successful! Redirecting...
                        </div>
                    """, unsafe_allow_html=True)

                    st.rerun()
                else:
                   
                    st.markdown("""
                        <style>
                        @keyframes fadeIn {
                            from {opacity: 0;}
                            to {opacity: 1;}
                        }
                        .error-box {
                            background-color: #ff4b4b;
                            color: white;
                            font-weight: 600;
                            text-align: center;
                            padding: 10px;
                            border-radius: 8px;
                            margin-top: 10px;
                            box-shadow: 0 0 10px rgba(255,0,0,0.5);
                            animation: fadeIn 0.6s ease-in;
                        }
                        </style>
                        <div class="error-box">❌ Invalid username or password</div>
                    """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

# ---------------------------
# Load History
# ---------------------------
HISTORY_FILE = "history.csv"

if not os.path.exists(HISTORY_FILE):
    st.warning("⚠️ No prediction history found yet.")
    st.stop()

df = pd.read_csv(HISTORY_FILE)

if df.empty:
    st.warning("⚠️ Prediction history is empty.")
    st.stop()

if "Timestamp" in df.columns:
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

# ---------------------------
# KPI CARDS
# ---------------------------
total_preds = len(df)
real_count = (df["Label"] == "Real Currency").sum()
fake_count = (df["Label"] == "Fake Currency").sum()
invalid_count = (df["Label"] == "Invalid Image").sum()

col1, col2, col3, col4 = st.columns(4)

col1.markdown(
    f"""
    <div style='background-color:#1E3A8A; padding:15px; border-radius:12px; text-align:center;'>
        <p style='font-size:20px; color:#E5E7EB; margin:0;'>📊 Total Predictions</p>
        <p style='font-size:28px; font-weight:bold; color:#4ADE80; margin:0;'>{total_preds}</p>
    </div>
    """, unsafe_allow_html=True
)

col2.markdown(
    f"""
    <div style='background-color:#065F46; padding:15px; border-radius:12px; text-align:center;'>
        <p style='font-size:20px; color:#D1FAE5; margin:0;'>✅ Real Currency</p>
        <p style='font-size:28px; font-weight:bold; color:#10B981; margin:0;'>{real_count}</p>
    </div>
    """, unsafe_allow_html=True
)

col3.markdown(
    f"""
    <div style='background-color:#92400E; padding:15px; border-radius:12px; text-align:center;'>
        <p style='font-size:20px; color:#FEF3C7; margin:0;'>⚠️ Fake Currency</p>
        <p style='font-size:28px; font-weight:bold; color:#FBBF24; margin:0;'>{fake_count}</p>
    </div>
    """, unsafe_allow_html=True
)

col4.markdown(
    f"""
    <div style='background-color:#7F1D1D; padding:15px; border-radius:12px; text-align:center;'>
        <p style='font-size:20px; color:#FECACA; margin:0;'>❌ Invalid Image</p>
        <p style='font-size:28px; font-weight:bold; color:#F87171; margin:0;'>{invalid_count}</p>
    </div>
    """, unsafe_allow_html=True
)

st.divider()

# ---------------------------
# Prediction History Table
# ---------------------------
st.markdown("<h2 style='color:white;'>📋 Prediction History</h2>", unsafe_allow_html=True)
st.dataframe(df.sort_values("Timestamp", ascending=False), use_container_width=True, height=400)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.download_button(
        label="📥 Download History (CSV)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="history.csv",
        mime="text/csv"
    )

st.divider()

# ---------------------------
# Charts
# ---------------------------
st.markdown("<h2 style='color:white; text-align:center;'>📊 Visual Insights</h2>", unsafe_allow_html=True)

count_df = df["Label"].value_counts().reset_index()
count_df.columns = ["Label", "Count"]

col1, col2 = st.columns(2)

with col1:
    fig_bar = px.bar(
        count_df,
        x="Label",
        y="Count",
        color="Label",
        text="Count",
        title="Prediction Count per Class"
    )
    fig_bar.update_traces(textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    fig_pie = px.pie(
        count_df,
        names="Label",
        values="Count",
        title="Prediction Distribution",
        hole=0.3
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# --- 🧠 Auto-generated Description ---
total = count_df["Count"].sum()
dominant = count_df.iloc[count_df["Count"].idxmax()]
minor = count_df.iloc[count_df["Count"].idxmin()]
dominant_pct = (dominant["Count"] / total) * 100
minor_pct = (minor["Count"] / total) * 100

insight_text = f"""
<div style='
    background-color:#0D1B2A;
    color:white;
    padding:15px;
    border-radius:10px;
    margin-top:20px;
    border:1px solid #00B4D8;
'>
    <h4 style='color:#80FFDB;'>📈 Automated Insight</h4>
    <p style='font-size:16px;'>
        The majority of predictions belong to <b>{dominant["Label"]}</b> class, 
        accounting for approximately <b>{dominant_pct:.1f}%</b> of total detections.
        Meanwhile, <b>{minor["Label"]}</b> occurrences are lower at about 
        <b>{minor_pct:.1f}%</b>.
    </p>
</div>
"""
st.markdown(insight_text, unsafe_allow_html=True)


st.divider()

st.markdown("<h2 style='color:white; text-align:center;'>📈 Prediction Trends Over Time</h2>", unsafe_allow_html=True)

if "Timestamp" in df.columns and df["Timestamp"].notna().sum() > 0:
    trend_df = df.groupby([df["Timestamp"].dt.date, "Label"]).size().reset_index(name="Count")

    if len(trend_df) > 1:
        # --- Create the Line Chart ---
        fig_line = px.line(
            trend_df,
            x="Timestamp",
            y="Count",
            color="Label",
            markers=True,
            title="Daily Prediction Trends"
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # --- 🧠 Auto-Insight Analysis ---
        insight_html = "<div style='background-color:#0D1B2A; color:white; padding:15px; border-radius:10px; border:1px solid #00B4D8;'>"
        insight_html += "<h4 style='color:#80FFDB;'>📊 Automated Trend Insights</h4>"

        for label in trend_df["Label"].unique():
            label_data = trend_df[trend_df["Label"] == label].sort_values("Timestamp")
            counts = label_data["Count"].values

            if len(counts) > 2:
                # Compute direction changes
                diffs = [counts[i+1] - counts[i] for i in range(len(counts)-1)]
                pos = sum(1 for d in diffs if d > 0)
                neg = sum(1 for d in diffs if d < 0)

                start_val = counts[0]
                end_val = counts[-1]
                net_change = end_val - start_val
                change_percent = (net_change / start_val * 100) if start_val != 0 else 0

                if pos > 0 and neg == 0:
                    trend = "📈 increasing steadily"
                    insight_html += f"<p style='font-size:16px;'>Predictions for <b>{label}</b> are {trend}, up by about <b>{change_percent:.1f}%</b> overall.</p>"
                elif neg > 0 and pos == 0:
                    trend = "📉 decreasing continuously"
                    insight_html += f"<p style='font-size:16px;'>Predictions for <b>{label}</b> are {trend}, falling by roughly <b>{abs(change_percent):.1f}%</b> since the start.</p>"
                elif pos > 0 and neg > 0:
                    trend = "⚖️ fluctuating over time"
                    insight_html += f"<p style='font-size:16px;'>Predictions for <b>{label}</b> show {trend}, with ups and downs across the timeline.</p>"
                else:
                    trend = "stable"
                    insight_html += f"<p style='font-size:16px;'>Predictions for <b>{label}</b> remain relatively stable.</p>"
            else:
                insight_html += f"<p style='font-size:16px;'>Insufficient data to detect a trend for <b>{label}</b>.</p>"

        insight_html += "</div>"
        st.markdown(insight_html, unsafe_allow_html=True)




st.divider()

# ---------------------------
# Admin Controls
# ---------------------------
st.markdown("""
    <div style="background-color:white; padding:25px; border-radius:15px; 
                box-shadow:0px 4px 15px rgba(0,0,0,0.3); margin-bottom:20px;">
        <h1 style="font-size:28px; color:#FF980; font-weight:900; text-align:center;">
            ⚙️ Admin Controls
        </h1>
    </div>
""", unsafe_allow_html=True)

# ---------------------------
# Dataset / Model Management
# ---------------------------
st.subheader("🗂️ Manage Currency Image Dataset")

task = st.radio("", ["📤 Upload Image", "🗑️ Delete Image", "🔄 Retrain Model"])

# ✅ Upload Image
if task == "📤 Upload Image":
    split = st.selectbox("Select Dataset Split", ["train", "test"])
    label = st.selectbox("Select Class", ["real", "fake", "invalid"])
    new_img = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])


    if new_img:
        st.image(Image.open(new_img), caption="Uploaded Image Preview", width=250)
        if st.button("✅ Save Image"):
            save_dir = os.path.join("dataset", split, label)
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, new_img.name)
            with open(save_path, "wb") as f:
                f.write(new_img.read())
            st.success(f"✅ {new_img.name} saved in {split}/{label}")

# ✅ Delete Image
elif task == "🗑️ Delete Image":
    split = st.selectbox("Select Split", ["train", "test"])
    label = st.selectbox("Select Class", ["real", "fake", "invalid"])
    target_dir = os.path.join("dataset", split, label)
    os.makedirs(target_dir, exist_ok=True)

    files = os.listdir(target_dir)
    if files:
        file_to_delete = st.selectbox("Select Image", files)
        img_path = os.path.join(target_dir, file_to_delete)

        st.image(Image.open(img_path), caption=file_to_delete, width=250)

        if st.button("🗑️ Delete Selected Image"):
            os.remove(img_path)
            st.success(f"✅ Deleted {file_to_delete}")
            st.rerun()

        if st.button("⚠️ Delete ALL Images"):
            for f in files:
                os.remove(os.path.join(target_dir, f))
            st.success(f"✅ Deleted all images in {split}/{label}")
            st.rerun()
    else:
        st.info("No images found in folder.")

# ✅ Retrain Model
elif task == "🔄 Retrain Model":
    st.subheader("🔄 Retrain Model")
    retrain_mode = st.radio("Retrain Mode", ["⚡ Quick Retrain", "🧠 Full Retrain"])

    if st.button("🚀 Start Retraining"):
        cmd = ["python", "train.py", "--mode", "quick"] if retrain_mode == "⚡ Quick Retrain" else ["python", "train.py", "--mode", "full"]
        
        st.info("⏳ Training started... Please wait.")
        progress = st.progress(0)
        log_area = st.empty()

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        logs = ""
        for line in iter(process.stdout.readline, ''):
            logs += line
            log_area.text_area("📝 Logs", logs, height=600)
            if "PROGRESS:" in line:
                try:
                    percent = int(line.strip().split(":")[1])
                    progress.progress(percent)
                except:
                    pass

        process.stdout.close()
        process.wait()
        progress.progress(100)
        st.success("✅ Training Complete! Model updated.")

