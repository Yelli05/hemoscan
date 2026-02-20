import streamlit as st
import numpy as np
from PIL import Image
import cv2
import time

st.set_page_config(page_title="HemoScan AI", layout="wide", page_icon="🩺")

st.title("🩺 **HemoScan AI**")
st.markdown("***Non-invasive Anemia Detection & Risk Analysis***")

tab1, tab2 = st.tabs(["📸 **Photo Scan**", "📋 **Risk Test**"])

with tab1:
    st.subheader("👁️ **Step 1: Capture Inner Eyelid (Flash ON)**")
    
    def predict_hb(image):
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        h, w = img_cv.shape[:2]
        center = img_cv[h//4:3*h//4, w//4:3*w//4]
        mean_rgb = np.mean(center, axis=(0,1))[::-1]
        r, g, b = mean_rgb
        hb = 8.5 + (r - 140) * 0.08 + (g - 130) * 0.07
        return round(hb, 1), mean_rgb
    
    col1, col2 = st.columns([1,3])
    with col1:
        st.info("📱 **Instructions:**\n• Turn flash ON\n• Open lower eyelid\n• Take close-up photo")
    with col2:
        uploaded_file = st.file_uploader("Upload photo...", type=['png','jpg','jpeg'])
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Your Photo", use_column_width=True)
            
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
                st.metric("Redness", f"{rgb[0]:.0f}")

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
st.markdown("*College Hackathon 2026 | Conjunctiva color analysis*")
