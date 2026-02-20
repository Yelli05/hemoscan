import streamlit as st
import numpy as np
from PIL import Image
import cv2
import time
import cnn_model  # Your ML model
if 'live_scan' not in st.session_state:
    st.session_state.live_scan = False
if 'hb_result' not in st.session_state:
    st.session_state.hb_result = None
if 'scan_mode' not in st.session_state:
    st.session_state.scan_mode = None

st.set_page_config(page_title="HemoScan AI", layout="wide", page_icon="🩺")

st.title("🩺 **HemoScan AI**")
st.markdown("***Non-invasive Anemia Detection & Risk Analysis***")

tab1, tab2 = st.tabs(["📸 **Photo Scan**", "📋 **Risk Test**"])

with tab1:
    st.subheader("👁️ **Step 1: Live Conjunctiva Scan**")
    
    def predict_hb(image):
        return cnn_model.predict_with_ml(image)
    
    col1, col2 = st.columns([1,3])
    with col1:
        st.info("📱 **Live Camera Instructions:**\n• Turn FLASH ON\n• Open lower eyelid\n• Hold steady 2 seconds")
        if st.button("🎥 **START LIVE SCAN**", use_container_width=True, type="primary"):
            st.session_state.live_scan = True
    
    with col2:
        # BUTTON CONTROLLED CAMERA (NEW!)
        if st.button("📸 **START LIVE SCAN**", use_container_width=True, type="primary"):
            st.session_state.scan_mode = "live"
            st.rerun()  # Refresh to show camera
        
        if st.session_state.get('scan_mode') == "live":
            st.markdown("### 🎥 **Camera Active - Take Photo**")
            camera_image = st.camera_input("📷 Flash ON - Hold steady...")
            
            if camera_image:
                st.session_state.scan_mode = None  # Hide camera after capture
                image = Image.open(camera_image)
                st.image(image, caption="✅ LIVE SCAN CAPTURED", use_column_width=True)
                
                # Analysis
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress.progress(i + 1)
                
                hb, rgb = predict_hb(image)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Hemoglobin", f"{hb:.1f} g/dL")
                with col2:
                    status = "🟡 ANEMIC" if hb < 12 else "🟢 NORMAL"
                    st.metric("Status", status)
                with col3:
                    st.metric("Redness", f"{rgb[0]}")
        
        else:
            # File upload fallback
            st.markdown("### 📎 **OR Upload Saved Photo**")
            uploaded_file = st.file_uploader("Choose photo...", type=['png','jpg','jpeg'])
            
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="✅ PHOTO UPLOADED", use_column_width=True)
                
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress.progress(i + 1)
                
                hb, rgb = predict_hb(image)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Hemoglobin", f"{hb:.1f} g/dL")
                with col2:
                    status = "🟡 ANEMIC" if hb < 12 else "🟢 NORMAL"
                    st.metric("Status", status)
                with col3:
                    st.metric("Redness", f"{rgb[0]}")


with tab2:
    st.subheader("📊 **Step 2: Complete Risk Assessment**")
    
    with st.form("risk_assessment"):
        col1, col2 = st.columns(2)
        age = col1.number_input("👴 Age", 16, 80, 25)
        gender = col2.selectbox("⚥ Gender", ["Male", "Female"])
        
        col1, col2 = st.columns(2)
        fatigue = col1.slider("😴 Daily tiredness (0-10)", 0, 10, 3)
        meat_intake = col2.selectbox("🍖 Meat consumption", ["Never", "1-2x/week", "Daily"])
        
        col1, col2 = st.columns(2)
        dizzy = col1.checkbox("😵 Frequent dizziness")
        pale_skin = col2.checkbox("🤍 Notice pale skin/nails")
        
        if st.form_submit_button("🎯 **Calculate My Risk**", use_container_width=True):
            risk_score = 0
            if age > 50: risk_score += 15
            if gender == "Female": risk_score += 20
            if fatigue > 6: risk_score += 25
            if meat_intake == "Never": risk_score += 30
            if dizzy: risk_score += 20
            if pale_skin: risk_score += 15
            
            progress_bar = st.progress(0)
            for i in range(101):
                progress_bar.progress(i)
                time.sleep(0.02)
            
            col1, col2 = st.columns([3,1])
            with col1:
                if risk_score < 30:
                    st.success("🟢 **LOW RISK** - You're healthy!")
                elif risk_score < 60:
                    st.warning("🟡 **MEDIUM RISK** - Monitor diet")
                else:
                    st.error("🔴 **HIGH RISK** - See doctor NOW")
            
            with col2:
                st.metric("Risk Score", f"{risk_score}%")
            
            st.balloons()

st.markdown("---")
st.markdown("*College Hackathon 2026 | Neural Network + Conjunctiva Analysis*")
